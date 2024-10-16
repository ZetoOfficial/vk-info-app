import os

from dotenv import load_dotenv

from exceptions import EnvFileNotFoundError


def load_environment(env_path: str = "config.DEFAULT_ENV_FILE") -> None:
    if not os.path.exists(env_path):
        raise EnvFileNotFoundError(f"The file {env_path} was not found. Please create it and add VK_ACCESS_TOKEN.")
    load_dotenv(env_path)
