import random
import allure
from framework.api.base import ApiClient
from framework.api.endpoint import AbstractEndpoint
from framework.api.payloads import UserData


class UserEndpoint(AbstractEndpoint):
    """
    An object that represents user endpoint, defined in the "path" attribute
    """

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__(api_client=api_client)

    @property
    def path(self) -> str:
        """
        Returns the fixed API endpoint path
        """
        return "/users"

    @allure.step("Get a random user")
    def get_random_user(self) -> UserData:
        """Retrieve a random user data"""
        resp = self._get().json()
        random_user = random.choice(resp)
        self.api_client.logger.info("Users are retrieved")

        return UserData(
            userId=random_user["id"],
            user_email=random_user["email"],
        )
