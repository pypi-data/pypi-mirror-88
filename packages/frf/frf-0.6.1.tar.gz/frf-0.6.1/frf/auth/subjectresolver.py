"""Declares :class:`BearerSubjectResolver`."""
from unimatrix.lib.datastructures import ImmutableDTO


class BearerSubjectResolver:
    """The base class for all subject resolvers. A subject resolver constructs
    an implementation-specific :term:`Subject` instance from the claims
    provided in a :term:`Bearer Token`.
    """

    async def resolve(self, claims):
        """Resolve to a concrete implementation of :term:`Subject` based
        on the asserted claims.
        """
        sub = await self.get_subject(claims)
        await self.verify_signature(claims, sub)
        return sub

    async def verify_signature(self, claims, sub):
        """Verifies the signature of bearer token that was used to create
        :class:`~frf.RequestClaimSet` `claims`.
        """
        claims.verify_signature()

    async def get_subject(self, claims):
        """Lookup a :term:`Subject` implementation from the persistent
        storage backend. This method must be overridden by subclasses.
        """
        return ImmutableDTO(
            subject_id=claims['sub'],
            realm=claims.get('rlm')
        )
