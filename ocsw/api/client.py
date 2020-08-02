# Copyright (c) 2020 Maxim Barabash
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Octave Cloud SDK."""


import logging

import aiohttp

from .. import errors
from ..constants import (
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
    OCTAVE_API_DEFAULT,
)
from .action import ActionApiMixin
from .blueprint import BlueprintApiMixin
from .company import CompanyApiMixin
from .device import DeviceApiMixin
from .event import EventApiMixin
from .firmware import FirmwareApiMixin
from .group import GroupApiMixin
from .identity import IdentityApiMixin
from .local_action import EdgeActionApiMixin
from .release import ReleaseApiMixin
from .stream import StreamApiMixin


class APIClient(
    ActionApiMixin,
    BlueprintApiMixin,
    CompanyApiMixin,
    DeviceApiMixin,
    EventApiMixin,
    FirmwareApiMixin,
    GroupApiMixin,
    IdentityApiMixin,
    EdgeActionApiMixin,
    ReleaseApiMixin,
    StreamApiMixin,
):
    """A low-level client for the Octave Cloud API."""

    log = logging.getLogger(__name__)

    def __init__(
        self,
        session=None,
        base_url=OCTAVE_API_DEFAULT,
        login=None,
        token=None,
        company=None,
        user_agent=DEFAULT_USER_AGENT,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        **_kwargs,
    ):
        """Constructor APIClient."""
        self._session = session
        self._base_url = base_url or OCTAVE_API_DEFAULT
        self._company_identifer = company
        self._auth = dict(login=login, token=token)
        self._user_agent = user_agent
        self._timeout = timeout

    @property
    def current_company(self):
        return self._company_identifer

    @property
    def _headers(self):
        headers = dict()
        if self._user_agent:
            headers["User-Agent"] = str(self._user_agent)
        if self._auth["login"]:
            headers["X-Auth-User"] = str(self._auth["login"])
        if self._auth["token"]:
            headers["X-Auth-Token"] = str(self._auth["token"])
        return headers

    def get_path(self, tmpl, **kwargs):
        kwargs.setdefault("base_url", self._base_url)
        kwargs.setdefault("company_name", self._company_identifer)
        return tmpl.format(**kwargs)

    def _url(self, resource, **kwargs):
        path = self.get_path(resource, **kwargs)
        if "?" in path:
            raise errors.InvalidResource(f"Broken resource {path!r}")
        return path
        # if resource.startswith("/"):
        #     url = f"{self._base_url}{resource}"
        # else:
        #     url = f"{self._base_url}/{self._company_identifer}/{resource}"
        # return url

    async def _result(self, response):
        # self.log.debug(r"request header:%s", dict(resp.headers))
        self.log.debug(r"request url: %s", response.request_info.real_url)
        # text = await response.text()
        # self.log.debug("response.text %s", text)
        result = await response.json()
        self.log.debug("result %s", result)
        head = result.get("head", {})
        errs = head.get("errors")
        if errs:
            raise errors.APIError("\n".join(errs), response=response)
        return result

    async def _request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self._timeout)
        kwargs.setdefault("headers", self._headers)
        if self._session:
            session = self._session
            async with session.request(method, url, **kwargs) as resp:
                result = await self._result(resp)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as resp:
                    result = await self._result(resp)
        return result

    async def _get(self, url, **kwargs):
        return await self._request("GET", url, **kwargs)

    async def _post(self, url, **kwargs):
        return await self._request("POST", url, **kwargs)

    async def _put(self, url, **kwargs):
        return await self._request("PUT", url, **kwargs)

    async def _delete(self, url, **kwargs):
        return await self._request("DELETE", url, **kwargs)

    # # async def count(self, entity):
    # #     """return number of entities
    # #     body: {count: 3}
    # #     ...
    # #     """
    # #     url = self._url(f'count/{entity}')
    # #     params = dict()
    # #     return await self._get(url, params=params)
