import argparse
import random

import requests


def main(username, password):
    base_url = "http://localhost:8000"

    auth_endpoint = f"{base_url}/v1/authn/user-sessions/"
    create_collection_endpoint = f"{base_url}/v1/journal/collections/"

    response = requests.post(
        url=auth_endpoint,
        json={
            "username": username,
            "password": password,
        },
        headers={
            "Content-Type": "application/json",
        },
    )

    response.raise_for_status()

    token = response.json()["token"]

    def get_slug():
        return "".join(
            random.choices(list("abcdefghijklmnopqrstuvwxyz0123456789"), k=4)
        )

    for i in range(10):
        data = {
            "name": f"test_{get_slug()}",
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
            "active": True,
        }

        response = requests.post(
            url=create_collection_endpoint,
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        response.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--username")
    parser.add_argument("--password")

    args = parser.parse_args()

    main(username=args.username, password=args.password)
