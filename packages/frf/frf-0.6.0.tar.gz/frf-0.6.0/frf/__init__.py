# pylint: skip-file
from ioc import provide
from ioc import inject

from .asgi import get_asgi_application
from .auth import *
from .decorators import *
from .dependency import ContextualInjected
from .dependency import Injected
from .routers import FastAPIRouter
from .viewsets import GenericViewSet
from .views import AnonymousResource
from .views import Resource


__all__ = [
    'action',
    'get_asgi_application',
    'inject',
    'provide',
    'response_model',
    'BearerClaims',
    'BearerSubjectResolver',
    'BearerTokenDecoder',
    'CurrentSubject',
    'Resource',
    'RequestClaimSet',
]


provide('BearerTokenDecoder', BearerTokenDecoder())
