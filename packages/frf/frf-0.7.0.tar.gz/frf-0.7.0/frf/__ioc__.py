# pylint: skip-file
import ioc

from .auth import BearerSubjectResolver
from .auth import BearerTokenDecoder
from .services import APIMetadataService
from .services import HealthCheckService


def setup_ioc():
    ioc.provide('APIMetadataService', APIMetadataService())
    ioc.provide('BearerSubjectResolver', BearerSubjectResolver())
    ioc.provide('BearerTokenDecoder', BearerTokenDecoder())
    ioc.provide('HealthCheckService', HealthCheckService())
