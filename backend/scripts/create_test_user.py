import random
import sys

import django

django.setup()

import constants
import requests
from django.contrib.auth import get_user_model
from helpers import generate_id
from kuroshitsuji.settings import get_env

env = get_env()

if (
    env.get_env_val("APP_ENVIRONMENT").upper()
    == constants.APP_ENVIRONMENT_PRODUCTION.upper()
):
    sys.exit(1)


def get_slug() -> str:
    return "".join(random.choices(list("abcdefghijklmnopqrstuvwxyz0123456789"), k=4))


slug = get_slug()
username = f"test_{slug}@test.com"
password = f"pass{slug}"

endpoint = f"{env.get_env_val('APP_FIREBASE_AUTH_URL')}:signUp"

# curl -iX POST http://localhost:9099/identitytoolkit.googleapis.com/v1/accounts:signUp?key=fake-api-key -H 'Content-Type: application/json' --data-raw '{"email": "test@test.com", "password": "pass1234"}'
response = requests.post(
    url=endpoint,
    params={"key": env.get_env_val("APP_FIREBASE_API_KEY")},
    json={
        "email": username,
        "password": password,
    },
    headers={
        "Content-Type": "application/json",
    },
)
response.raise_for_status()

# insert user into db

user = get_user_model()(username=username, gid=generate_id(constants.USER_PREFIX))
user.save()

assert user.id is not None

# print creds
print(f"created user with username: {username} and password: {password}")
