import inspect
import logging
from dataclasses import asdict
from time import sleep
from typing import Callable
from tenacity import retry, retry_if_exception_type, stop_after_attempt
import requests
from config import API_TIMEOUT
from framework.api.common.request import RequestModel, RetryModel
from framework.api.exceptions import APIException


class ApiClient:
    """
    A generic client for sending requests to an API using "requests" library.
    """

    def __init__(self):
        """
        Initialize the ApiClient instance.
        """
        self.base_url = "https://jsonplaceholder.typicode.com/"
        self.logger = logging.getLogger()

    def __base_request(
            self, request_model: RequestModel, retry_model: RetryModel | None = None, **kwargs
    ) -> requests.Response:
        """
        Send a request to the API.
        Send retry request if retry argument provided
        """
        if retry_model:
            response = self.send_retry_request(retry_model=retry_model)(request_model=request_model)
        else:
            try:
                response = requests.request(**asdict(request_model), timeout=API_TIMEOUT, **kwargs)
            except requests.ConnectionError as ec:
                raise APIException("Connection Error:", ec)
            except requests.HTTPError as eh:
                raise APIException("Http Error:", eh)
        return response

    def send_request(
            self,
            request_model: RequestModel,
            retry_model: RetryModel | None = None,
            retry_attempts: int = 3,
            retry_delay: int = 1,
            **kwargs,
    ) -> requests.Response:
        """Resending API request if API error"""
        for retry_attempt in range(retry_attempts + 1):
            try:
                response = self.__base_request(request_model, retry_model, **kwargs)
            except APIException:
                if retry_attempt < retry_attempts:
                    sleep(retry_delay)
            else:
                return response

        self.logger.error(f"Request error occurs {request_model.url}")
        raise APIException("API retry attempts limit reached.")

    def send_retry_request(self, retry_model: RetryModel, **kwargs) -> Callable:
        """Send a retry request"""
        expected = retry_model.retry_until_values
        extract_value = inspect.getsource(retry_model.extract_value).strip()
        self.logger.info(f"Start retry queries for key: '{extract_value}'; expected values: {expected}")

        @retry(
            retry=retry_if_exception_type(retry_model.retry_if_exception_type),
            stop=stop_after_attempt(retry_model.stop_after_attempt),
            wait=retry_model.wait_type(),
        )
        def _send_retry_request(
                request_model: RequestModel,
        ) -> requests.Response:
            """
            :param request_model: (RequestModel): Request data
            :return: response object
            """
            response = requests.request(**asdict(request_model), timeout=API_TIMEOUT, **kwargs)
            received = retry_model.extract_value(response)

            if received not in expected:
                wait_type = inspect.getsource(retry_model.wait_type).strip()
                self.logger.warning(f"Got '{received}'; Retrying using model '{wait_type}'")
                raise ValueError(f"Field {received} is not found in {expected}")
            return response

        return _send_retry_request
