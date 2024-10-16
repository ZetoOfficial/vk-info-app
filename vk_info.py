import argparse
import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

VK_API_VERSION = "5.131"
DEFAULT_OUTPUT_FILE = "vk_user_info.json"
DEFAULT_ENV_FILE = ".env"


class EnvFileNotFoundError(Exception):
    """Raised when the .env file is not found."""

    pass


class AccessTokenNotFoundError(Exception):
    """Raised when VK_ACCESS_TOKEN is not set in the .env file."""

    pass


class VKAPIError(Exception):
    """Raised when an error is returned by the VK API."""

    def __init__(self, message: str):
        super().__init__(f"VK API Error: {message}")


class EmptyAPIResponseError(Exception):
    """Raised when the VK API returns an empty or unexpected response."""

    def __init__(self, endpoint: str, response: str):
        super().__init__(f"Empty or unexpected response from VK API for {endpoint}.\nResponse: {response}")


def load_environment(env_path: str = DEFAULT_ENV_FILE) -> None:
    """
    Loads environment variables from a .env file.
    """
    if not os.path.exists(env_path):
        raise EnvFileNotFoundError(f"The file {env_path} was not found. Please create it and add VK_ACCESS_TOKEN.")
    load_dotenv(env_path)


def get_access_token() -> str:
    """
    Retrieves the access token from the environment variable.
    """
    token = os.getenv("VK_ACCESS_TOKEN")
    if not token:
        raise AccessTokenNotFoundError("The VK_ACCESS_TOKEN environment variable is not set in the .env file.")
    return token


def fetch_vk_data(user_id: str, token: str) -> Dict[str, Any]:
    """
    Fetches user info, followers, subscriptions, and groups.
    """
    base_url = "https://api.vk.com/method/"

    user_params = {"user_ids": user_id, "fields": "followers_count", "access_token": token, "v": VK_API_VERSION}
    user_resp = requests.get(base_url + "users.get", params=user_params)
    user_data = user_resp.json()

    if "error" in user_data:
        raise VKAPIError(user_data['error']['error_msg'])

    if "response" not in user_data or not user_data["response"]:
        raise EmptyAPIResponseError("users.get", json.dumps(user_data, ensure_ascii=False, indent=4))

    user_info = user_data["response"][0]

    followers_count = user_info.get("followers_count", 0)
    if followers_count == 0:
        print("Warning: The user has zero followers or this information is unavailable.")

    subscriptions_params = {
        "user_id": user_id,
        "access_token": token,
        "v": VK_API_VERSION,
        "extended": 1,
        "count": 200,
    }
    subscriptions_resp = requests.get(base_url + "users.getSubscriptions", params=subscriptions_params)
    subscriptions_data = subscriptions_resp.json()

    if "error" in subscriptions_data:
        raise VKAPIError(subscriptions_data['error']['error_msg'])

    if "response" not in subscriptions_data:
        raise EmptyAPIResponseError(
            "users.getSubscriptions", json.dumps(subscriptions_data, ensure_ascii=False, indent=4)
        )

    subscriptions = subscriptions_data["response"].get("items", [])
    subscriptions_count = len(subscriptions)
    if subscriptions_count == 0:
        print("Warning: The user has zero subscriptions.")

    # Getting groups from subscriptions
    groups = []
    for group in subscriptions:
        if "id" in group:
            group_info = {"id": group["id"], "name": group.get("name", ""), "screen_name": group.get("screen_name", "")}
            groups.append(group_info)

    return {
        "user": {
            "id": user_info.get("id"),
            "first_name": user_info.get("first_name"),
            "last_name": user_info.get("last_name"),
            "followers_count": followers_count,
        },
        "followers_count": followers_count,
        "subscriptions_count": subscriptions_count,
        "groups": groups,
    }


def save_to_json(data: Dict[str, Any], filepath: str):
    """
    Saves data to a JSON file with indentations and UTF-8 encoding.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Fetch information about a VK user.")
    parser.add_argument("user_id", nargs="?", default="self", help="VK user ID (default is the current user).")
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Path to the output file (default is {DEFAULT_OUTPUT_FILE}).",
    )
    return parser.parse_args()


def get_current_user_id(token: str) -> str:
    """
    Retrieves the current user ID using the access token.
    """
    base_url = "https://api.vk.com/method/"
    user_params = {"fields": "id", "access_token": token, "v": VK_API_VERSION}
    user_resp = requests.get(base_url + "users.get", params=user_params)
    user_data = user_resp.json()

    if "error" in user_data:
        raise VKAPIError(user_data['error']['error_msg'])

    if "response" not in user_data or not user_data["response"]:
        raise EmptyAPIResponseError("users.get", json.dumps(user_data, ensure_ascii=False, indent=4))

    user_info = user_data["response"][0]
    return str(user_info.get("id"))


def main():
    args = parse_arguments()
    load_environment()

    token = get_access_token()

    user_id = args.user_id
    if user_id.lower() == "self":
        user_id = get_current_user_id(token)

    data = fetch_vk_data(user_id, token)
    save_to_json(data, args.output)
    print(f"Data successfully saved to {args.output}")


if __name__ == "__main__":
    main()
