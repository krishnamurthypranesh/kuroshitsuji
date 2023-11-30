from unittest import mock

import pytest
from authn import models
from authn.models import User
from backends import FirebaseAuthenticationBackend
from django.http import HttpRequest
from exc import ApplicationBaseException, IncorrectAuthenticationCredentialsException

from yurucamp.settings import __env


@pytest.mark.django_db
class TestFirebaseAuthenticationBackendAuthenticate:
    @pytest.fixture(scope="class", autouse=True)
    def setUp(self, request):
        with mock.patch("backends.requests") as _mock_request:
            with mock.patch("backends.get_env") as _mock_env:
                request.cls.mock_request = _mock_request

                env_vals = {
                    "app_firebase_auth_url": "http://test.url",
                    "app_firebase_api_key": "test-key",
                }

                _mock_env.return_value.get_env_val.side_effect = lambda x: env_vals.get(
                    x.lower()
                )

                yield

                request.cls.mock_request.reset_mock()

    def test_makes_correct_request_when_authenticating_users(self, setup_user_account):
        username, password = setup_user_account
        self.mock_request.post.return_value = mock.MagicMock()

        u = FirebaseAuthenticationBackend().authenticate(
            HttpRequest(), username, password
        )

        self.mock_request.post.assert_called_with(
            **{
                "url": "http://test.url:signInWithPassword",
                "params": {"key": "test-key"},
                "json": {"email": username, "password": password},
                "headers": {"Content-Type": "application/json"},
            }
        )

    def test_raises_correct_error_when_firebase_returns_400(self, setup_user_account):
        username, password = setup_user_account
        _mock = mock.MagicMock()
        _mock.status_code = 400

        self.mock_request.post.return_value = _mock

        with pytest.raises(IncorrectAuthenticationCredentialsException):
            FirebaseAuthenticationBackend().authenticate(
                HttpRequest(), username, password
            )

    def test_raises_correct_error_when_firebase_returns_non_200_response(
        self, setup_user_account
    ):
        username, password = setup_user_account
        _mock = mock.MagicMock()
        _mock.status_code = 500
        _mock.raise_for_status.side_effect = Exception("expected error")

        self.mock_request.post.return_value = _mock

        with pytest.raises(ApplicationBaseException):
            FirebaseAuthenticationBackend().authenticate(
                HttpRequest(), username, password
            )

    def test_returns_NONE_if_user_does_not_exist(self):
        # this should not exist in the db
        username = "test"
        password = "test"

        user = FirebaseAuthenticationBackend().authenticate(
            HttpRequest(), username, password
        )

        assert user is None

    def test_returns_correct_user_object_if_authentication_works(
        self, setup_user_account
    ):
        username, password = setup_user_account
        _mock = mock.MagicMock()
        _mock.status_code = 200

        self.mock_request.post.return_value = _mock

        expected_user = User.objects.get(username=username)

        user = FirebaseAuthenticationBackend().authenticate(
            HttpRequest(), username, password
        )

        assert user is not None
        assert user.id == expected_user.id
        assert user.username == username
        assert user.last_login_at == expected_user.last_login_at
        assert user.joined_at == expected_user.joined_at
