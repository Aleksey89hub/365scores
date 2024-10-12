from typing import Callable
import pytest

from framework.api.base import ApiClient
from framework.api.endpoints.user_endpoint import UserEndpoint
from framework.api.payloads import UserData


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    """Provide an api_client to make requests with"""
    return ApiClient()


@pytest.fixture(scope='session')
def fetch_user_data(api_client: ApiClient) -> Callable:
    """Fixture to retrieve random user data."""

    def _get_user_data() -> UserData:
        return UserEndpoint(api_client).get_random_user()

    return _get_user_data
