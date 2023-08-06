"""Declares :class:`ResourceEndpointTestCase`."""
import copy
import unittest

import ioc
from fastapi.testclient import TestClient

import frf


class ResourceEndpointTestCase(unittest.TestCase):
    """Provides boilerplate to test :class:`~frf.Resource` objects."""
    endpoints = []

    def setUp(self):
        self.encoder = ioc.provide('BearerTokenDecoder',
            frf.BearerTokenDecoder(), force=True)

        self.asgi = self.get_asgi_application()
        for path, cls in self.endpoints:
            self.asgi.add_resource(cls, base_path=path)
        self.client = TestClient(self.asgi)

    def request(self, func, *args, **kwargs):
        headers = kwargs.pop('headers', None) or {}
        return func(*args, headers={**headers, **copy.deepcopy(self.headers)},
            **kwargs)

    def get_headers(self):
        """Return the default headers."""
        return {}

    def get_asgi_application(self):
        """Return the :class:`~frf.ASGIApplication` instance that is used
        during this test. Subclasses must override this method.
        """
        raise NotImplementedError


class ProtectedResourceTestCase(ResourceEndpointTestCase):
    audience = None
    scopes = None

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {self.token}"
        }

    def setUp(self):
        super().setUp()
        self.token = self.encoder.encode(self.audience, 'foo', None)

    def refresh_token(self, aud=None, claims=None, scopes=None, **kwargs):
        claims = claims or {}
        if scopes is not None:
            claims['scopes'] = scopes
        self.token = self.encoder.encode(aud or self.audience,
            'foo', None, claims=claims, **kwargs)
