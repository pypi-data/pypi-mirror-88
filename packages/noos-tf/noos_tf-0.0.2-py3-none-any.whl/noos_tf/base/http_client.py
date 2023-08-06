from http import client as http_client
from typing import Dict, Optional
from urllib import parse

import requests


class ClientError(Exception):
    """Basic exception raised by a JSON client."""


class HTTPError(ClientError):
    """Exception encountered over a HTTP client connection."""


JSON_CONTENT_TYPE = {
    "application/json",
    "application/vnd.api+json",
    "application/vnd.api+json; charset=utf-8",
}


class JSONClient:
    """Base class for JSON clients."""

    _conn: Optional[requests.Session] = None

    # Default base URL
    default_base_url: str = ""

    # Default connection timeout at 10''
    default_timeout = 10.0

    # Default JSON response back
    default_headers = {"Accept": "application/json"}

    def __init__(
        self,
        base_url: Optional[str] = None,
        default_timeout: Optional[float] = None,
        default_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._url = base_url or self.default_base_url
        self._timeout = default_timeout or self.default_timeout
        self._headers = default_headers or self.default_headers

    @property
    def conn(self) -> requests.Session:
        """HTTP client connection object."""
        if self._conn is None:
            self._conn = requests.Session()
            self._conn.headers.update(self._headers)
        return self._conn

    # Public HTTP methods:

    def _post(self, path: str, data: Optional[dict] = None, statuses: tuple = ()) -> dict:
        return self._request(method="POST", path=path, data=data, statuses=statuses)

    def _put(self, path: str, data: Optional[dict] = None, statuses: tuple = ()) -> dict:
        return self._request(method="PUT", path=path, data=data, statuses=statuses)

    def _patch(self, path: str, data: Optional[dict] = None, statuses: tuple = ()) -> dict:
        return self._request(method="PATCH", path=path, data=data, statuses=statuses)

    def _get(self, path: str, params: Optional[dict] = None, statuses: tuple = ()) -> dict:
        return self._request(method="GET", path=path, params=params, statuses=statuses)

    def _delete(self, path: str, params: Optional[dict] = None, statuses: tuple = ()) -> dict:
        return self._request(method="DELETE", path=path, params=params, statuses=statuses)

    # Private methods:

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        statuses: tuple = (),
    ) -> dict:
        url = parse.urljoin(self._url, path)

        response = self.conn.request(
            method, url, params=params, json=data, headers=self._headers, timeout=self._timeout
        )

        _check_response(response, statuses=statuses)
        return _deserialize_response(response)


# Helpers:


def _check_response(response: requests.Response, statuses: tuple = ()) -> None:
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise HTTPError(f"{response.status_code}: {response.text}")
    else:
        if response.status_code not in statuses:
            codes = ",".join([str(status) for status in statuses])
            raise HTTPError(f"Unexpected {response.status_code} response: expected {codes}")


def _deserialize_response(response: requests.Response) -> dict:
    content_type = response.headers.get("content-type", "")
    if content_type in JSON_CONTENT_TYPE:
        return response.json()

    # When 204 is returned, there is explicitly no content.
    if response.status_code == http_client.NO_CONTENT:
        return {}

    raise ClientError(f"No JSON content returned: {response.text}")
