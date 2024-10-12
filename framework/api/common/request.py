from dataclasses import dataclass, field
from typing import Any, Callable
from framework.api.payloads import RequestPayload


@dataclass
class RetryModel:
    """
    Retrying request until any of key values found
    Examples of wait_type:
    lambda: wait_fixed(wait_fixed_interval=3) # 3, 3
    lambda: wait_incrementing(start=2, increment=2, max=8) # 2, 4, 6, 8, 8
    lambda: wait_incrementing(start=8, increment=2, max=18), # total 690 seconds
    lambda: wait_exponential(min=3, max=24) # 3, 6, 12, 24, 24
    Examples of wait_for_key:
    lambda response: response.json().get("jobIsFinished") is not False
    """

    extract_value: Callable
    retry_until_values: list
    wait_type: Callable
    max_attempts: int = 2
    stop_after_attempt: int = 10
    retry_if_exception_type: type[BaseException] | tuple[type[BaseException]] = ValueError


@dataclass
class RequestModel:
    """Base class for HTTP request models."""

    url: str
    method: str
    headers: dict = field(default_factory=dict)


@dataclass
class HttpGet(RequestModel):
    """Represents an HTTP GET request, including URL, headers, optional parameters, and method."""

    params: RequestPayload | dict | None = None
    method: str = "get"


@dataclass
class HttpPost(RequestModel):
    """Represents an HTTP POST request, including URL, headers, optional data or JSON payload, and method."""

    data: RequestPayload | None = None
    json: RequestPayload | dict[str, Any] | None = None
    method: str = "post"
