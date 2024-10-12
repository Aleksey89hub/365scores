from typing import Callable

import allure
import pytest

from framework.api.base import ApiClient
from framework.api.endpoints.user_post_endpoint import UserPostEndpoint
from framework.api.payloads import UserData
from helpers.tools import faker, log_email, get_parametrized_data, read_data


@allure.feature("User Information")
@allure.story("Retrieve User and Validate Posts")
class TestUserAPI:

    @allure.step("Retrieve a random user and verify user's post ids")
    def test_user_associated_post(self, api_client: ApiClient, fetch_user_data: Callable):
        random_user_data = fetch_user_data()
        user_id = random_user_data.userId
        log_email(email=random_user_data.user_email, user_id=user_id)
        user_posts = UserPostEndpoint(api_client).get_user_associated_post(user_id=user_id)
        invalid_post_ids = [post for post in user_posts if not 1 <= post['id'] <= 100]

        assert not invalid_post_ids, f"All post IDs should be between 1 and 100, but got {invalid_post_ids}"

    @allure.step("Verify a new user post creation")
    def test_post_creation(self, api_client: ApiClient, fetch_user_data: Callable):
        random_user_data = fetch_user_data()
        user_id = random_user_data.userId
        response = UserPostEndpoint(api_client).create_user_post(user_data=UserData(
            userId=user_id,
            title=faker.word(),
            body=faker.word(),
        ))

        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}."

    @pytest.mark.parametrize("title, body", get_parametrized_data(read_data()))
    @allure.step("Verify user creation from csv data provider")
    def test_user_post_creation_with_data(self,
                                    api_client: ApiClient,
                                    fetch_user_data: Callable,
                                    title: str,
                                    body: str, ):
        random_user_data = fetch_user_data()
        user_id = random_user_data.userId
        response = UserPostEndpoint(api_client).create_user_post(user_data=UserData(
            userId=user_id,
            title=title,
            body=body,
        ))

        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}."
