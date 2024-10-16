import os

from dotenv import load_dotenv

from exceptions import EnvFileNotFoundError


class EnvLoader:
    def __init__(self, env_file: str = "config.DEFAULT_ENV_FILE"):
        self.env_file = env_file

    def load(self):
        if not os.path.exists(self.env_file):
            raise EnvFileNotFoundError(
                f"The file {self.env_file} was not found. Please create it and add VK_ACCESS_TOKEN."
            )
        load_dotenv(self.env_file)
