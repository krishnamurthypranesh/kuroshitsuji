import uuid
from datetime import datetime, timedelta, timezone
from unittest import mock

import pytest
from authn.models import User, UserSession
from django.test import Client, TestCase
from django.urls import reverse


@pytest.mark.django_db
class TestCreateUserSession:
    @pytest.fixture(scope="class", autouse=True)
    def setUp(self, request):
        request.cls.client = Client()

    def test_raises_400_if_body_is_not_correct_json(self):
        response = self.client.post(
            reverse("create_session"),
            content_type="application/json",
            data="<html></html>",
        )

        assert response is not None
        assert response.status_code == 400
        assert response.json() == {"detail": "improper data"}

    def test_returns_401_if_authentication_fails(self):
        with mock.patch("authn.views.authenticate") as _mock:
            _mock.return_value = None
            response = self.client.post(
                reverse("create_session"),
                content_type="application/json",
                data={
                    "username": "test-username",
                    "password": "test-password",
                },
            )

            assert response is not None
            assert response.status_code == 401
            assert response.json() == {"detail": "failure"}

    def test_returns_correct_session_id_on_successful_authentication(
        self, setup_user_account
    ):
        username, password = setup_user_account

        mock_session_id = str(uuid.uuid1())
        mock_datetime = datetime.now().replace(tzinfo=timezone.utc)

        with mock.patch("authn.views.generate_session_id") as _gen_mock:
            with mock.patch("authn.views.get_current_datetime") as _dt_mock:

                _dt_mock.return_value = mock_datetime
                _gen_mock.return_value = mock_session_id

                response = self.client.post(
                    reverse("create_session"),
                    content_type="application/json",
                    data={
                        "username": username,
                        "password": password,
                    },
                )

                assert response is not None
                assert response.status_code == 201
                assert response.json() == {"token": mock_session_id}

        user = User.objects.get(username=username)
        user_session = UserSession.objects.get(session_id=mock_session_id)

        assert user_session.expires_at == mock_datetime + timedelta(days=3)
        assert user_session.user_id == user.id
