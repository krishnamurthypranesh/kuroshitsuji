import uuid
from datetime import datetime, timedelta, timezone
from unittest import mock

import pytest
from authn.models import User, UserSession
from django.test import Client, TestCase
from django.urls import reverse


@pytest.mark.django_db
class TestCreateCollection:
    @pytest.fixture(scope="class", autouse=True)
    def setUp(self, request):
        request.cls.client = Client()

    def test_raises_400_if_body_is_not_correct_json(self, create_user_session):
        token = create_user_session
        response = self.client.post(
            reverse("create_collection"),
            content_type="application/json",
            data="<html></html>",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response is not None
        assert response.status_code == 400
        assert response.json() == {"detail": "improper data"}

    def test_returns_401_if_authentication_fails(self):
        response = self.client.post(
            reverse("create_collection"),
            content_type="application/json",
            data={},
        )

        assert response is not None
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    def test_returns_400_if_collection_template_has_wrong_format(
        self, create_user_session
    ):
        token = create_user_session

        response = self.client.post(
            reverse("create_collection"),
            data={
                "name": "test_template",
                "template": "<html></html>",
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response is not None
        assert response.status_code == 400

    def test_returns_409_if_active_collection_with_same_name_already_exists(
        self, setup_user_account
    ):
        assert 1 == 0

    def test_returns_409_if_inactive_collection_with_same_name_already_exists(
        self, setup_user_account
    ):
        assert 1 == 0

    def test_returns_201_if_collection_is_created_successfully(
        self, setup_user_account
    ):
        assert 1 == 0
