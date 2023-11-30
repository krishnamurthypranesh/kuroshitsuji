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

    def test_returns_409_if_collection_with_same_name_already_exists(
        self, create_user_session
    ):
        token = create_user_session

        for is_active in [True, False]:
            name = str(uuid.uuid1())

            response = self.client.post(
                reverse("create_collection"),
                data={
                    "name": name,
                    "template": {
                        "fields": [
                            {
                                "key": "title",
                                "display_name": "Title",
                            },
                            {
                                "key": "content",
                                "display_name": "Content",
                            },
                        ],
                    },
                    "active": is_active,
                },
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response is not None
            assert response.status_code == 201

            response = self.client.post(
                reverse("create_collection"),
                data={
                    "name": name,
                    "template": {
                        "fields": [
                            {
                                "key": "title",
                                "display_name": "Title",
                            },
                            {
                                "key": "content",
                                "display_name": "Content",
                            },
                        ],
                    },
                    "active": is_active,
                },
                content_type="application/json",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response is not None
            assert response.status_code == 409

            assert response.json() == {
                "detail": f"collection with name: {name} already exists!"
            }

    def test_returns_201_if_collection_is_created_successfully(
        self, create_user_session
    ):
        token = create_user_session

        response = self.client.post(
            reverse("create_collection"),
            data={
                "name": str(uuid.uuid1()),
                "template": {
                    "fields": [
                        {
                            "key": "title",
                            "display_name": "Title",
                        },
                        {
                            "key": "content",
                            "display_name": "Content",
                        },
                    ],
                },
                "active": False,
            },
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response is not None
        assert response.status_code == 201
