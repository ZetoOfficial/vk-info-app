import json
import os
from typing import Any, Dict

import requests

from config import VK_API_VERSION
from exceptions import AccessTokenNotFoundError, EmptyAPIResponseError, VKAPIError


def get_access_token() -> str:
    token = os.getenv("VK_ACCESS_TOKEN")
    if not token:
        raise AccessTokenNotFoundError("The VK_ACCESS_TOKEN environment variable is not set in the .env file.")
    return token


def fetch_vk_data(user_id: str, token: str) -> Dict[str, Any]:
    base_url = "https://api.vk.com/method/"
    # Fetch user data
    user_params = {"user_ids": user_id, "fields": "followers_count", "access_token": token, "v": VK_API_VERSION}
    user_resp = requests.get(base_url + "users.get", params=user_params)
    user_data = user_resp.json()
    if "error" in user_data:
        raise VKAPIError(user_data['error']['error_msg'])
    if "response" not in user_data or not user_data["response"]:
        raise EmptyAPIResponseError("users.get", json.dumps(user_data, ensure_ascii=False, indent=4))
    user_info = user_data["response"][0]
    # Fetch subscriptions data
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
    groups = [
        {"id": group["id"], "name": group.get("name", ""), "screen_name": group.get("screen_name", "")}
        for group in subscriptions
        if "id" in group
    ]
    return {
        "user": {
            "id": user_info.get("id"),
            "first_name": user_info.get("first_name"),
            "last_name": user_info.get("last_name"),
            "followers_count": user_info.get("followers_count", 0),
        },
        "followers_count": user_info.get("followers_count", 0),
        "subscriptions_count": len(subscriptions),
        "groups": groups,
    }


def get_current_user_id(token: str) -> str:
    base_url = "https://api.vk.com/method/"
    user_params = {"fields": "id", "access_token": token, "v": VK_API_VERSION}
    user_resp = requests.get(base_url + "users.get", params=user_params)
    user_data = user_resp.json()
    if "error" in user_data:
        raise VKAPIError(user_data['error']['error_msg'])
    if "response" not in user_data or not user_data["response"]:
        raise EmptyAPIResponseError("users.get", json.dumps(user_data, ensure_ascii=False, indent=4))
    return str(user_data["response"][0].get("id"))
