"""Provides the functions to create the ASGI application."""
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from unimatrix.conf import settings


class FastAPI(fastapi.FastAPI):
    """A :class:`fastapi.FastAPI` subclass that provides integration with
    the Unimatrix Framework.
    """

    def add_resource_router(self, router):
        """Add a :class:`~frf.FastAPIRouter` to the ASGI application."""
        router.add_to_app(self)


def get_asgi_application():
    """Return a :class:`fastapi.FastAPI` instance. This is the main ASGI
    application.

    The :func:`get_asgi_application()` gathers configuration from various
    sources in order to configure a basic :class:`fastapi.FastAPI` instance. The
    order is as defined below:

    - :attr:`unimatrix.conf.settings`
    - :mod:`unimatrix.environ`

    All common environment variables specified by the Unimatrix Framework are
    detected by :func:`get_asgi_application()`. Additional configuration may
    be provided by setting the environment variable `UNIMATRIX_SETTINGS_MODULE`,
    holding the qualified name of a Python module.
    """
    app = FastAPI(
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL
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
        allowed_hosts=settings.HTTP_ALLOWED_HOSTS
    )

    return app
