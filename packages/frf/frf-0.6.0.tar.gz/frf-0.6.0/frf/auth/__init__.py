# pylint: skip-file
from fastapi import Depends
from fastapi import Request

from ..dependency import Injected
from .subjectresolver import BearerSubjectResolver
from .claims import RequestClaimSet
from .decoder import BearerTokenDecoder


__all__ = [
    'BearerClaims',
    'BearerSubjectResolver',
    'BearerTokenDecoder',
    'CurrentSubject',
    'RequestClaimSet',
]


def _get_bearer_claimset(request: Request):
    return RequestClaimSet.fromrequest(request)


#: The :class:`~frf.RequestClaimSet` asserted by the :term:`Bearer Token`
#: of the current request.
BearerClaims = Depends(_get_bearer_claimset)


async def _resolve_claims(
    request: Request,
    resolver=Injected('BearerSubjectResolver'),
    claims=BearerClaims
):
    return await resolver.resolve(claims)


#: The :term:`Subject` identified by the verified claims asserted by the
#: :term:`Bearer Token`.
CurrentSubject = Depends(_resolve_claims)
