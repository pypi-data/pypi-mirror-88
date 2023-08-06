"""Declares :class:`BaseToken`."""
import hashlib
import time

import authlib.jose.errors
import jwt
import jwt.exceptions
import cryptography.exceptions
from authlib.jose import JsonWebEncryption
from unimatrix.conf import settings
from unimatrix.ext.model.exc import CrossSiteRequestForgeryTokenExpired
from unimatrix.ext.model.exc import CrossSiteRequestForgeryTokenInvalid
from unimatrix.ext.model.exc import CrossSiteRequestForgeryTokenMissing
from unimatrix.ext.model.exc import ExpiredSignatureError
from unimatrix.ext.model.exc import InvalidAudience
from unimatrix.ext.model.exc import InvalidScope
from unimatrix.ext.model.exc import InvalidSignatureError
from unimatrix.ext.model.exc import InvalidToken

from frf.lib import constant_time_compare


NOT_PROVIDED = object()


class BaseToken:
    """Represents a token that a :term:`Subject` can exchange for a short-lived
    session token.
    """

    @classmethod
    def create(cls, aud, sub, exp, **claims):
        claims = {'sub': sub, 'exp': int(exp), **claims}
        if aud:
            claims['aud'] = aud
        return cls(claims, None)

    @classmethod
    def parse(cls, token, aud, secret, scope=None, csrf_token=NOT_PROVIDED,
        _csrf_exp=None, scopes=None, signing_key=None):
        """Parse a token into into a (subclass of) :class:`BaseToken` object.

        Args:
            token (:class:`str`): the :term:`Bearer Token` encrypted with
                JSON Web Encryption (JWE).
            secret (:class:`str`): the secret to decrypt `token`. Also verifies
                the signature of the enclosed claimset (using JSON Web
                Signature), if `signing_key` is not provided.

        Raises:
            :exc:`~unimatrix.ext.model.exc.InvalidToken`: `secret` is not
                valid to decrypt `token`.

        Returns:
            :class:`BaseToken`
        """
        jwe = JsonWebEncryption()
        try:
            data = jwe.deserialize_compact(token,
                hashlib.sha256(str.encode(secret)).digest())
            bearer = data['payload']
            claims = jwt.decode(bearer, secret, verify=False)
            obj = cls(claims, bearer)
        except (
            cryptography.exceptions.InvalidTag,
            authlib.jose.errors.DecodeError
        ):
            raise InvalidToken
        if scopes is not None:
            obj.validate_scopes(scopes)
        if csrf_token != NOT_PROVIDED:
            obj.verify_csrf(csrf_token, exp=_csrf_exp)
        return obj

    @property
    def audience(self):
        return self.claims['aud']

    @property
    def csrf_token(self):
        return self.claims.get('csrfToken')

    @property
    def scopes(self):
        value = self.claims.get('scopes')
        if isinstance(value, str):
            value = str.split(value, ' ')
        elif value is None:
            value = []
        return set(value)

    @property
    def subject(self):
        return self.claims['sub']

    def __init__(self, claims, bearer):
        self.claims = claims
        self.bearer = bearer

    def as_dict(self):
        """Return a dictionary containing the claims."""
        return dict(self.claims)

    def encode(self, secret: str, signing_key: str = None):
        """Encrypt the token using the given string `secret` and optional
        signing key `signing_key`. If `signing_key` is ``None``, then `secret`
        is also used to sign the enclosed data.
        """
        jwe = JsonWebEncryption()
        jws = jwt.encode(self.claims, signing_key or secret, algorithm='HS256')
        token = jwe.serialize_compact({'alg': 'A256GCMKW', 'enc': 'A256GCM'},
            jws, hashlib.sha256(str.encode(secret)).digest())
        return bytes.decode(token, 'ascii')

    def verify_audience(self, aud):
        """Verifies that the `aud` claim is correct."""
        if 'aud' not in self.claims or not bool(self.claims.get('aud')):
            raise InvalidAudience(
                token=self,
                detail="The bearer token did not specify an audience.",
                hint=f"This resource requires a bearer token with the audience "
                      "{aud}"
            )
        claimed_audiences = self.claims['aud']
        if isinstance(claimed_audiences, str):
            claimed_audiences = [claimed_audiences]
        is_valid = False
        for claimed in claimed_audiences:
            if not constant_time_compare(claimed, aud):
                continue
            is_valid = True
            break

        detail = "The Bearer token specified an invalid `aud` claim: "
        detail += str.join(',', claimed_audiences)
        if not is_valid:
            raise InvalidAudience(token=self)

    def verify_csrf(self, csrf_token, exp=None):
        """Verifies the CSRF token."""
        if csrf_token is None:
            raise CrossSiteRequestForgeryTokenMissing(token=self)
        if (exp or self.claims['csrfExp']) <= int(time.time()):
            raise CrossSiteRequestForgeryTokenExpired(token=self)
        if not constant_time_compare(self.csrf_token or '', csrf_token):
            raise CrossSiteRequestForgeryTokenInvalid(token=self)

    def validate_scopes(self, scopes):
        """Validate that the token has the required `scopes`."""
        if not set(self.scopes) >= set(scopes)\
        and ('*' not in self.scopes):
            detail = f"The Bearer token has invalid scope(s): {self.scopes}"
            hint = "Present a token with at least the following scopes: "
            hint += str.join(', ', scopes)
            raise InvalidScope(token=self, hint=hint, detail=detail)

    def verify_signature(self, signing_key=None):
        """Verifies the signature of the bearer token."""
        try:
            jwt.decode(self.bearer, signing_key or settings.SECRET_KEY,
                algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise InvalidSignatureError(token=self)
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredSignatureError(token=self)

    def get(self, claim):
        """Return the `claim` or ``None``."""
        return self.claims.get(key)

    def __getitem__(self, key):
        return self.claims[key]
