"""Declares :class:`ExchangeToken`."""
import hashlib

import jwt
import cryptography.exceptions
import jwt.exceptions
from authlib.jose import JsonWebEncryption
from unimatrix.conf import settings
from unimatrix.lib import timezone

from dccp.lib import constant_time_compare
from .exc import CrossSiteRequestForgeryTokenExpired
from .exc import CrossSiteRequestForgeryTokenInvalid
from .exc import CrossSiteRequestForgeryTokenMissing
from .exc import ExpiredSignatureError
from .exc import InvalidAudience
from .exc import InvalidScope
from .exc import InvalidToken


NOT_PROVIDED = object()


class ExchangeToken:
    """Represents a token that a :term:`Subject` can exchange for a short-lived
    session token.
    """

    @classmethod
    def create(cls, rlm, aud, sub, exp, **claims):
        return cls({
            'rlm': rlm,
            'aud': aud,
            'sub': sub,
            'exp': exp,
            **claims
        })

    @classmethod
    def parse(cls, token, aud, secret=None, scope=None, csrf_token=NOT_PROVIDED,
        _csrf_exp=None, scopes=None):
        """Parse a JSON Web Token (JWT) into a :class:`ExchangeToken` object."""
        jwe = JsonWebEncryption()
        secret = secret or settings.SECRET_KEY
        try:
            data = jwe.deserialize_compact(token,
                hashlib.sha256(str.encode(secret)).digest())
            obj = cls(jwt.decode(
                data['payload'], secret or settings.SECRET_KEY,
                algorithms=['HS256'],
                audience=aud
            ))
        except cryptography.exceptions.InvalidTag:
            raise InvalidToken
        except jwt.exceptions.PyJWTError as e:
            token = cls(jwt.decode(data['payload'], verify=False))
            if isinstance(e, jwt.exceptions.InvalidAudienceError):
                raise InvalidAudience(token=token)
            elif isinstance(e, jwt.exceptions.ExpiredSignatureError):
                raise ExpiredSignatureError(token=token)
            else:
                raise

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
        return set(self.claims.get('scopes') or [])

    @property
    def realm(self):
        return self.claims['rlm']

    @property
    def subject(self):
        return self.claims['sub']

    def __init__(self, claims):
        self.claims = claims

    def validate_scopes(self, scopes):
        """Validate that the token has the required `scopes`."""
        if not set(self.scopes) >= set(scopes):
            raise InvalidScope(token=self)

    def verify_csrf(self, csrf_token, exp=None):
        """Verifies the CSRF token."""
        if csrf_token is None:
            raise CrossSiteRequestForgeryTokenMissing(token=self)
        if (exp or self.claims['csrfExp']) <= timezone.now():
            raise CrossSiteRequestForgeryTokenExpired(token=self)
        if not constant_time_compare(self.csrf_token or '', csrf_token):
            raise CrossSiteRequestForgeryTokenInvalid(token=self)

    def __str__(self):
        jwe = JsonWebEncryption()
        jws = jwt.encode(self.claims, settings.SECRET_KEY, algorithm='HS256')
        token = jwe.serialize_compact({'alg': 'A256GCMKW', 'enc': 'A256GCM'},
            jws, hashlib.sha256(str.encode(settings.SECRET_KEY)).digest())
        return bytes.decode(token, 'ascii')
