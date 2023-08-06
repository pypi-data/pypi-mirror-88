"""Declares :class:`RequestClaimSet`."""
import ioc
from unimatrix.ext.model.exc import MissingToken


class RequestClaimSet:
    """Provides an interface to the claims specified in an incoming request
    with the ``Authorization`` header.
    """
    __module__ = 'frf'
    cookie_name = 'debug.bearer-token'

    @staticmethod
    def get_authorization_scheme_param(authorization_header_value: str):
        scheme, _, param = authorization_header_value.partition(" ")
        return scheme, param

    @classmethod
    def fromrequest(cls, request, cookie_name=None, allow_cookie=False,
        audience=None):
        """Create a new :class:`RequestClaimSet` from a :class:`fastapi.Request`
        instance.
        """
        cookie_name = cookie_name or cls.cookie_name
        bearer = None
        if request.headers.get('Authorization'):
            scheme, bearer = cls.get_authorization_scheme_param(
                request.headers['Authorization'])
            if scheme != 'Bearer':
                bearer = None
        elif allow_cookie and request.cookies.get(cookie_name):
            bearer = request.cookies.get(cookie_name)
        return cls(bearer, csrf_token=request.headers.get('X-Csrf-Token'),
            audience=audience)

    @property
    def claims(self):
        """Return the claims specified in the bearer token."""
        if self._claims is None:
            self._claims = self._decode()
        return self._claims

    def __init__(self, bearer, audience=None, csrf_token=None):
        self._bearer = bearer
        self._claims = None
        self._audience = audience
        self._csrf_token = csrf_token

    def as_dict(self):
        """Return the claims as a dictionary."""
        return self.claims.as_dict()

    def verify_audience(self, audience):
        """Verifies the ``aud`` claim."""
        return self.claims.verify_audience(audience)

    def verify_scopes(self, scopes):
        """Verify that the required scopes are present on the claim."""
        return self.claims.validate_scopes(scopes)

    def verify_signature(self, signing_key=None):
        """Verifies the signature over the claims asserted by the bearer
        token. Use the `signing_key` parameter to specify the signing key
        against which the signature must be validated.
        """
        self.claims.verify_signature(signing_key=signing_key)

    def verify_token(self):
        """Verify that the token can be decoded."""
        self._decode()

    @ioc.inject('decoder', 'BearerTokenDecoder')
    def _decode(self, decoder):
        if self._bearer is None:
            raise MissingToken(token=self._bearer)
        return decoder.decode(self._bearer, csrf_token=self._csrf_token,
            audience=self._audience)

    def get(self, claim):
        """Return the `claim` or ``None``."""
        return self.claims.get(key)

    def __getitem__(self, key):
        return self.claims[key]
