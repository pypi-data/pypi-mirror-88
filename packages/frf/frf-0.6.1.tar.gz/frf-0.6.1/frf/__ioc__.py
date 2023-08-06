# pylint: skip-file
import ioc

from .auth import BearerSubjectResolver
from .auth import BearerTokenDecoder


def setup_ioc():
    ioc.provide('BearerSubjectResolver', BearerSubjectResolver())
    ioc.provide('BearerTokenDecoder', BearerTokenDecoder())
