import allure
from requests import Response
from framework.api.base import ApiClient
from framework.api.endpoint import AbstractEndpoint
from framework.api.payloads import UserData


class UserPostEndpoint(AbstractEndpoint):
    """
    An object that represents user post endpoint, defined in the "path" attribute
    """

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client=api_client)

    @property
    def path(self) -> str:
        """Returns the fixed API endpoint path"""
        return "/posts"

    @allure.step("Get a user associated post")
    def get_user_associated_post(self, user_id: str) -> list:
        """Retrieve a user’s associated posts"""
        resp = self._get().json()
        self.api_client.logger.info("Users associated post are retrieved")
        return [entry for entry in resp if entry['userId'] == int(user_id)]

    @allure.step("Create user post")
    def create_user_post(self, user_data: UserData) -> Response:
        """Creates a new user post by sending a POST request with the provided user data."""
        self.api_client.logger.info("Create user pos")
        return self._post(json=user_data)
