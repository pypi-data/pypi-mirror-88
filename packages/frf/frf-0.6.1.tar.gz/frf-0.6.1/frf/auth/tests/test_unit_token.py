# pylint: skip-file
import time
import unittest

import ioc
from unimatrix.ext.model.exc import CrossSiteRequestForgeryTokenMissing
from unimatrix.ext.model.exc import CrossSiteRequestForgeryTokenExpired
from unimatrix.ext.model.exc import CrossSiteRequestForgeryTokenInvalid
from unimatrix.ext.model.exc import ExpiredSignatureError
from unimatrix.ext.model.exc import InvalidAudience
from unimatrix.ext.model.exc import InvalidScope
from unimatrix.ext.model.exc import InvalidToken

from ..token import BaseToken as Token


class GenerateTokenTestCase(unittest.TestCase):
    valid_scopes = ['auth.exchange']

    def setUp(self):
        self.aud = 'audience'
        self.secret = 'secret'
        self.signing_key = 'signing_key'
        self.csrf_token = 'csrf_token'
        self.domain = 'domain'
        self.subject = 'subject'
        self.token = self.generate_token()

    def generate_token(self, *args, **kwargs):
        kwargs.setdefault('exp', int(time.time() + 3600))
        kwargs.setdefault('csrfExp', int(time.time() + 3600))
        kwargs.setdefault('scopes', self.valid_scopes)
        return Token.create(
            aud=self.aud,
            sub=self.subject,
            rlm=self.domain,
            **kwargs
        )

    def test_parse_invalid_raises_invalid(self):
        with self.assertRaises(InvalidToken):
            Token.parse('foo', 'bar', 'baz')

    def test_verify_csrf(self):
        t1 = self.generate_token()
        t2 = t1.parse(t1.encode(secret=self.secret),
            csrf_token=t1.csrf_token, aud=t1.audience)

    def test_validate_scopes(self):
        self.token.validate_scopes(['auth.exchange'])

    def test_token_with_invalid_scopes_raises(self):
        with self.assertRaises(InvalidScope):
            self.token.validate_scopes(['foo'])

    def test_token_has_sub(self):
        self.assertEqual(self.token.subject, self.subject)

    def test_generate_exchange_token(self):
        t1 = self.generate_token()

    def test_parse_exchange_token(self):
        t1 = self.generate_token()
        t2 = Token.parse(t1.encode(secret=self.secret),
            aud=t1.audience, secret=self.secret)

    def test_parse_exchange_token_invalid_audience(self):
        t1 = self.generate_token()
        with self.assertRaises(InvalidAudience):
            t2 = Token.parse(t1.encode(secret=self.secret),
                aud='foo', secret=self.secret)
            t2.verify_audience('foo')

    def test_parse_exchange_token_missing_audience(self):
        t1 = self.generate_token()
        with self.assertRaises(InvalidAudience):
            t2 = Token.parse(t1.encode(secret=self.secret),
                aud=None, secret=self.secret)
            t2.verify_audience(aud='bar')

    def test_parse_exchange_token_expired(self):
        t1 = self.generate_token(exp=1)
        with self.assertRaises(ExpiredSignatureError):
            t2 = Token.parse(t1.encode(secret=self.secret), aud=t1.audience, secret=self.secret)
            t2.verify_signature(signing_key=self.secret)

    def test_parse_exchange_token_invalid_secret(self): # nosec
        t1 = self.generate_token()
        with self.assertRaises(InvalidToken):
            t2 = Token.parse(t1.encode(secret=self.secret),
                aud=t1.audience, secret='foo')

    def test_parse_with_valid_scopes(self):
        t1 = self.generate_token(scopes=self.valid_scopes)
        t2 = Token.parse(t1.encode(secret=self.secret),
            aud=t1.audience, scopes=self.valid_scopes, secret=self.secret)

    def test_parse_with_invalid_scopes(self):
        t1 = self.generate_token()
        with self.assertRaises(InvalidScope):
            t2 = Token.parse(
                t1.encode(secret=self.secret),
                    aud=t1.audience, scopes=['foo'], secret=self.secret)

    def test_verify_csrf(self):
        t1 = self.generate_token(csrfToken=self.csrf_token)
        t2 = Token.parse(t1.encode(secret=self.secret),
            aud=t1.audience, csrf_token=t1.csrf_token, secret=self.secret)

    def test_verify_csrf_missing_raises(self):
        t1 = self.generate_token()
        with self.assertRaises(CrossSiteRequestForgeryTokenMissing):
            Token.parse(t1.encode(secret=self.secret),
                aud=t1.audience, csrf_token=None, secret=self.secret)

    def test_verify_csrf_expired_raises(self):
        t1 = self.generate_token(csrfToken=self.csrf_token)
        with self.assertRaises(CrossSiteRequestForgeryTokenExpired):
            Token.parse(t1.encode(secret=self.secret),
                aud=t1.audience, csrf_token=t1.csrf_token,
                    _csrf_exp=1, secret=self.secret)

    def test_verify_csrf_invalid_raises(self): # nosec
        t1 = self.generate_token(csrfToken=self.csrf_token)
        with self.assertRaises(CrossSiteRequestForgeryTokenInvalid):
            Token.parse(t1.encode(secret=self.secret),
                aud=t1.audience, csrf_token='foo', secret=self.secret) # nosec
