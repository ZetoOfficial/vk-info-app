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
