class EnvFileNotFoundError(Exception):
    pass


class AccessTokenNotFoundError(Exception):
    pass


class VKAPIError(Exception):
    def __init__(self, message: str):
        super().__init__(f"VK API Error: {message}")


class EmptyAPIResponseError(Exception):
    def __init__(self, endpoint: str, response: str):
        super().__init__(f"Empty or unexpected response from VK API for {endpoint}.\nResponse: {response}")
