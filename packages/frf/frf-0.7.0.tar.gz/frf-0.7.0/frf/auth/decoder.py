"""Declares :class:`BearerTokenDecoder`."""
import time

from unimatrix.conf import settings

from .token import BaseToken
from .token import NOT_PROVIDED


class BearerTokenDecoder:
    """Provides an interface to decrypt and verify Bearer tokens."""
    default_ttl = 300

    def encode(self, aud, sub, exp, claims=None, signing_key=None, secret=None):
        """Encode a :term:`Bearer Token` using the default secret key."""
        if exp is None:
            exp = int(time.time() + self.default_ttl)
        claims = claims or  {}
        return BaseToken.create(aud, sub, exp, **claims).encode(
            secret or settings.SECRET_KEY, signing_key=signing_key)

    def decode(self, bearer, csrf_token=None, audience=None):
        """Decodes :term:`Bearer Token` `bearer` using the default secret
        key.
        """
        return BaseToken.parse(bearer, audience, settings.SECRET_KEY,
            csrf_token=csrf_token or NOT_PROVIDED)
