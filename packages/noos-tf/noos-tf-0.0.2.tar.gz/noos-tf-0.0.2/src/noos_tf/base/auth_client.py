from typing import Optional

from requests import auth

from . import http_client


class HTTPTokenAuth(auth.AuthBase):
    """Attaches a bearer token authentication header."""

    # Default token header and value
    default_header = "X-TokenAuth"
    default_value = "Token"

    def __init__(
        self, token: str, header: Optional[str] = None, value: Optional[str] = None
    ) -> None:
        self._token = token
        self._header = header or self.default_header
        self._value = value or self.default_value

    def __call__(self, r):
        r.headers[self._header] = f"{self._value} {self._token}"
        return r


class AuthClient(http_client.JSONClient):
    """Base class for authenticated clients (for token- or basic-based auth)."""

    # Default token authentication class
    default_auth_class = HTTPTokenAuth

    def set_auth_header(self, *args) -> None:
        """Set authentication header."""
        token_auth = self.default_auth_class(*args)
        token_auth(self.conn)
