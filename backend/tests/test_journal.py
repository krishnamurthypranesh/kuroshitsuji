import uuid
from datetime import datetime

import pytest
from authn.models import User, UserSession
from django.test import Client
from django.urls import reverse
from journal.models import Collection


@pytest.mark.django_db
class TestCreateCollection:
    @pytest.fixture(scope="class", autouse=True)
    def setUp(self, request):
        request.cls.client = Client()

    def test_raises_400_if_body_is_not_correct_json(self, create_user_session):
        token = create_user_session
        response = self.client.post(
            reverse("dispatch_collections"),
            content_type="application/json",
            data="<html></html>",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response is not None
        assert response.status_code == 400
        assert response.json() == {"detail": "improper data"}

    def test_returns_401_if_authentication_fails(self):
        response = self.client.post(
            reverse("dispatch_collections"),
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
            reverse("dispatch_collections"),
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
                reverse("dispatch_collections"),
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
                reverse("dispatch_collections"),
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
            reverse("dispatch_collections"),
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


@pytest.mark.django_db
class TestGetCollectionById:
    @pytest.fixture(scope="class", autouse=True)
    def setUp(self, request):
        request.cls.client = Client()

    def test_returns_401_if_authentication_fails(self):
        response = self.client.get(
            reverse(
                viewname="get_collection_by_id", kwargs={"collection_id": "random_id"}
            ),
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}

    def test_returns_404_if_collection_not_found(self, create_user_session):
        token = create_user_session
        response = self.client.get(
            reverse(
                viewname="get_collection_by_id", kwargs={"collection_id": "gibberish"}
            ),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response is not None
        assert response.status_code == 404
        assert response.json() == {"detail": "collection not found"}

    def test_returns_200_if_collection_is_found(self, create_user_session):
        token = create_user_session

        create_response = self.client.post(
            reverse("dispatch_collections"),
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

        collection_id = create_response.json()["collection_id"]

        response = self.client.get(
            reverse(
                viewname="get_collection_by_id", kwargs={"collection_id": collection_id}
            ),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response is not None
        assert response.status_code == 200
        assert response.json() == create_response.json()


@pytest.mark.django_db
class TestListCollections:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, create_user_session):
        self.client = Client()

        token = create_user_session

        user = User.objects.get(
            id=UserSession.objects.get(session_id=token).user_id,
        )

        collection_ids = []

        for i in range(20):
            is_active = False
            if i < 10:
                is_active = True
            name = str(uuid.uuid1())

            response = self.client.post(
                reverse("dispatch_collections"),
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

            collection_ids.append(response.json()["collection_id"])

        collections = Collection.objects.filter(
            gid__in=collection_ids, user_id=user.id
        ).order_by("-gid")

        self.user = user
        self.token = token
        self.collections = collections

        yield

        Collection.objects.filter(user_id=user.id).delete()

    def test_returns_401_if_unauthenticated(self):
        response = self.client.get(
            reverse(viewname="dispatch_collections"),
            data={
                "limit": 10,
            },
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 401

        assert response.json() == {"detail": "Unauthorized"}

    def test_returns_empty_list_if_no_collections_present(self):
        Collection.objects.filter(user_id=self.user.id).delete()

        response = self.client.get(
            reverse(viewname="dispatch_collections"),
            data={
                "limit": 10,
            },
            headers={"Authorization": f"Bearer {self.token}"},
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 200

        assert response.json()["records"] == []

    def test_applies_starting_after_filter_correctly(self):
        for idx, col in enumerate(self.collections):
            response = self.client.get(
                reverse(viewname="dispatch_collections"),
                data={
                    "limit": 20,
                    "starting_after": col.gid,
                },
                headers={"Authorization": f"Bearer {self.token}"},
                content_type="application/json",
            )

            assert response is not None
            assert response.status_code == 200

            actual_map = {r["collection_id"]: r for r in response.json()["records"]}

            for e in self.collections[:idx]:
                actual = actual_map[e.gid]

                assert e.gid == actual["collection_id"]
                assert e.name == actual["name"]
                assert e.template == actual["template"]
                assert e.active == actual["active"]
                assert (
                    e.created_at.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
                    == actual["created_at"]
                )


@pytest.mark.django_db
class TestCreateEntry:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        pass

    def test_returns_404_if_collection_not_found(self, create_user_session):
        assert 1 == 0

    def test_returns_400_if_entry_content_does_not_contain_all_required_fields_from_collection_template(
        self, create_user_session
    ):
        assert 1 == 0

    def test_saves_entry_with_correct_status_based_on_value_of_publish(self):
        assert 1 == 0

    def test_returns_401_if_unauthorized_request(self):
        assert 1 == 0
