from dataclasses import dataclass


@dataclass
class RequestPayload:
    """This class represents a root model for request payload."""

    pass


@dataclass
class UserData(RequestPayload):
    """Data class representing User info."""

    userId: str
    user_email: str | None = None
    title: str | None = None
    body: str | None = None
