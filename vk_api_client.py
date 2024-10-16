import json
import os
from typing import Any, Dict

import requests

from config import VK_API_VERSION
from exceptions import AccessTokenNotFoundError, EmptyAPIResponseError, VKAPIError


class VKAPIClient:
    def __init__(self):
        self.base_url = "https://api.vk.com/method/"
        self.token = self._get_access_token()

    def _get_access_token(self) -> str:
        token = os.getenv("VK_ACCESS_TOKEN")
        if not token:
            raise AccessTokenNotFoundError("The VK_ACCESS_TOKEN environment variable is not set in the .env file.")
        return token

    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        user_params = {
            "user_ids": user_id,
            "fields": "followers_count",
            "access_token": self.token,
            "v": VK_API_VERSION,
        }
        user_resp = requests.get(self.base_url + "users.get", params=user_params)
        user_data = user_resp.json()
        self._check_for_errors(user_data, "users.get")
        user_info = user_data["response"][0]
        return user_info

    def get_subscriptions(self, user_id: str) -> Dict[str, Any]:
        subscriptions_params = {
            "user_id": user_id,
            "access_token": self.token,
            "v": VK_API_VERSION,
            "extended": 1,
            "count": 200,
        }
        subscriptions_resp = requests.get(self.base_url + "users.getSubscriptions", params=subscriptions_params)
        subscriptions_data = subscriptions_resp.json()
        self._check_for_errors(subscriptions_data, "users.getSubscriptions")
        subscriptions = subscriptions_data["response"].get("items", [])
        return subscriptions

    def get_current_user_id(self) -> str:
        user_params = {"fields": "id", "access_token": self.token, "v": VK_API_VERSION}
        user_resp = requests.get(self.base_url + "users.get", params=user_params)
        user_data = user_resp.json()
        self._check_for_errors(user_data, "users.get")
        return str(user_data["response"][0].get("id"))

    def _check_for_errors(self, data: Dict[str, Any], endpoint: str):
        if "error" in data:
            raise VKAPIError(data['error']['error_msg'])
        if "response" not in data or not data["response"]:
            raise EmptyAPIResponseError(endpoint, json.dumps(data, ensure_ascii=False, indent=4))
