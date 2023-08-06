"""Provides the functions to create the ASGI application."""
import inspect

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from unimatrix.conf import settings

from .routers import FastAPIRouter


DEFAULT_ROUTER = FastAPIRouter()


class FastAPI(fastapi.FastAPI):
    """A :class:`fastapi.FastAPI` subclass that provides integration with
    the Unimatrix Framework.
    """
    endpoints = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.endpoints is None:
            self.endpoints = DEFAULT_ROUTER

    def add_resource_router(self, router):
        """Add a :class:`~frf.FastAPIRouter` to the ASGI application."""
        router.add_to_app(self)

    def add_resource(self, cls):
        """Add a RESTFUL API resource `cls` to the default router."""
        app = self
        base_path = f'/{cls.get_resource_name()}'

        # Iterate over all members of the class and find actions.
        for _, func in inspect.getmembers(cls):
            if not hasattr(func, 'action'):
                continue
            func.action.add_to_app(app, base_path, cls)

        if hasattr(cls, 'create'):
            cls.as_method_handler(
                app, f'{base_path}', 'POST', 'create')
        if hasattr(cls, 'retrieve'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'GET', 'retrieve')
        if hasattr(cls, 'list'):
            cls.as_method_handler(
                app, f'{base_path}', 'GET', 'list')
        if hasattr(cls, 'update'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'PATCH', 'update')
        if hasattr(cls, 'delete'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'DELETE', 'delete')
        if hasattr(cls, 'replace'):
            cls.as_method_handler(
                app, f'{base_path}/{{resource_id}}', 'PUT', 'replace')

        self.include_router(cls.router,
            tags=[cls.resource_name or cls.__name__])


def get_asgi_application(allowed_hosts=None):
    """Return a :class:`fastapi.FastAPI` instance. This is the main ASGI
    application.

    The :func:`get_asgi_application()` gathers configuration from various
    sources in order to configure a basic :class:`fastapi.FastAPI` instance. The
    order is as defined below:

    - :attr:`unimatrix.conf.settings` - this module loads all uppercased
      variables in the Python module (or package) indicated by the environment
      variable ``UNIMATRIX_SETTINGS_MODULE`` (see below).
    - :mod:`unimatrix.environ`

    All common environment variables specified by the Unimatrix Framework are
    detected by :func:`get_asgi_application()`. Additional configuration may
    be provided by setting the environment variable
    ``UNIMATRIX_SETTINGS_MODULE``, holding the qualified name of a Python
    module.
    """
    app = FastAPI(
        openapi_url=getattr(settings, 'OPENAPI_URL', '/openapi.json'),
        docs_url=getattr(settings, 'DOCS_URL', '/')
    )
    if settings.HTTP_CORS_ENABLED:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.HTTP_CORS_ALLOW_ORIGINS,
            allow_credentials=settings.HTTP_CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.HTTP_CORS_ALLOW_METHODS,
            allow_headers=settings.HTTP_CORS_ALLOW_HEADERS,
            expose_headers=settings.HTTP_CORS_EXPOSE_HEADERS,
            max_age=settings.HTTP_CORS_TTL
        )

    # Always enable the TrustedHostMiddleware.
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=(
            allowed_hosts or getattr(settings, 'HTTP_ALLOWED_HOSTS', [])
        )
    )

    return app
