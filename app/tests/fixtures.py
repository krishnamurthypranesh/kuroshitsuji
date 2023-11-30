import random

import pytest
import requests
from authn.models import User

from yurucamp.settings import get_env

env = get_env()


@pytest.fixture(scope="function")
def setup_firebase_user():
    rand = random.choices("0123456789", k=4)
    username = f"test-{''.join(rand)}@test.com"
    passwd = username

    response = requests.post(
        f'{env.get_env_val("APP_FIREBASE_AUTH_URL")}:signUp',
        params={
            "key": env.get_env_val("APP_FIREBASE_API_KEY"),
        },
        json={
            "email": username,
            "password": passwd,
        },
    )

    assert response is not None
    assert response.status_code == 200

    return username, passwd


@pytest.fixture(scope="function")
def setup_user_account(setup_firebase_user):
    username, password = setup_firebase_user

    user = User.objects.create_user(username=username)

    return username, password
