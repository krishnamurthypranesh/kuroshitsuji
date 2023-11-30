from authn import models
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthenticationMiddleware(TestCase):
    def setUp(self):
        pass

    def test_assert_does_not_raise_error_if_not_auth_header_and_whitelisted_url(self):
        assert 1 == 0

    def test_returns_401_if_not_auth_header_and_not_whitelisted_url(self):
        assert 1 == 0

    def test_returns_400_if_session_id_not_found(self):
        assert 1 == 0

    def test_returns_440_if_session_expired(self):
        assert 1 == 0
