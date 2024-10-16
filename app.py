import json

from cli_handler import CLIHandler
from config import DEFAULT_ENV_FILE
from env_loader import EnvLoader
from vk_api_client import VKAPIClient


class App:
    def __init__(self):
        self.env_loader = EnvLoader(DEFAULT_ENV_FILE)
        self.cli_handler = CLIHandler()
        self.vk_client = VKAPIClient()

    def run(self):
        self.env_loader.load()

        args = self.cli_handler.parse_args()

        user_id = self._resolve_user_id(args.user_id)
        user_data = self.vk_client.get_user_data(user_id)
        subscriptions = self.vk_client.get_subscriptions(user_id)

        data = self._prepare_data(user_data, subscriptions)
        self._save_to_file(data, args.output)
        print(f"Data successfully saved to {args.output}")

    def _resolve_user_id(self, user_id: str) -> str:
        if user_id.lower() == "self":
            return self.vk_client.get_current_user_id()
        return user_id

    def _prepare_data(self, user_info: dict, subscriptions: list) -> dict:
        groups = [
            {"id": group["id"], "name": group.get("name", ""), "screen_name": group.get("screen_name", "")}
            for group in subscriptions
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

    def _save_to_file(self, data: dict, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
