from typing import Any
import requests
from framework.api.base import ApiClient
from framework.api.common.request import RetryModel, HttpGet, HttpPost
from framework.api.payloads import RequestPayload


class AbstractEndpoint:
    """An object that represents an endpoint under test"""

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client
        self._path: str = ""
        self._json = None
        self._data = None
        self._params = None
        self._url = self._generate_url()

    @property
    def path(self) -> str:
        """
        The path to reach this endpoint on.
        """
        return self._path

    @property
    def url(self) -> str:
        """
        The fully qualified URL to reach this endpoint on (including host, path and parameters).
        """
        return self._generate_url()

    def _generate_url(self) -> str:
        return f"{self.api_client.base_url.rstrip('/')}/{self.path.lstrip('/')}"

    def _get(
            self,
            params: RequestPayload | dict | None = None,
            retry_model: RetryModel | None = None,
            **kwargs,
    ) -> requests.Response:
        """
        Send a GET request to an endpoint.
        """
        request_model = HttpGet(url=self.url, params=params)
        return self.api_client.send_request(request_model=request_model, retry_model=retry_model, **kwargs)

    def _post(
            self,
            data: RequestPayload | None = None,
            json: RequestPayload | dict[str, Any] | None = None,
            retry_model: RetryModel | None = None,
            **kwargs,
    ) -> requests.Response:
        """
        Send a POST request to an endpoint.
        """
        request_model = HttpPost(url=self.url, data=data, json=json)
        return self.api_client.send_request(request_model=request_model, retry_model=retry_model, **kwargs)
