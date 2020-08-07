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

import base64
import json
import logging
import os

OCTAVE_API_DEFAULT = "https://octave-api.sierrawireless.io/v5.0"

OCTAVE_API = os.environ.get("OCTAVE_CLOUD_base_url", OCTAVE_API_DEFAULT)
OCTAVE_TOKEN = os.environ.get("OCTAVE_CLOUD_TOKEN")
OCTAVE_USER = os.environ.get("OCTAVE_CLOUD_USER")
OCTAVE_COMPANY = os.environ.get("OCTAVE_CLOUD_COMPANY")

CONFIG_PROPS = ("base_url", "login", "token", "company")
LOG = logging.getLogger(__name__)


def find_config_path(config_name, default="."):
    pwd = os.getcwd()

    while True:
        path = os.path.join(pwd, config_name)
        if os.path.exists(path):
            return os.path.realpath(pwd)
        pwd = os.path.dirname(pwd)
        if len(pwd) < 6:
            return os.path.realpath(default)


def decode_auth(auth):
    if isinstance(auth, str):
        auth = auth.encode("ascii")
    auth = base64.b64decode(auth)
    login, token = auth.split(b":", 1)
    return login.decode("utf8"), token.decode("utf8")


def encode_auth(login, token):
    auth = f"{login}:{token}".encode("utf-8")
    return base64.b64encode(auth).decode("utf-8")


class Config:

    base_url = OCTAVE_API
    login = OCTAVE_USER
    token = OCTAVE_TOKEN
    company = OCTAVE_COMPANY

    def __init__(self, config_path=None, config_filename=None, **kwargs):
        if config_path and config_filename:
            filename = os.path.join(config_path, config_filename)
        else:
            filename = config_path or config_filename

        if filename and os.path.isfile(filename):
            self.load(filename)
        self.set(**kwargs)

    def as_dict(self):
        return dict((name, getattr(self, name)) for name in CONFIG_PROPS)

    def set(self, **kwargs):
        for name in kwargs:
            if name in CONFIG_PROPS:
                value = kwargs[name]
                setattr(self, name, value)
            else:
                LOG.warning("Unknown key %s", name)
        return self

    @property
    def auth(self):
        cfg = self.as_dict()
        login = cfg.get("login", "")
        token = cfg.get("token", "")
        return encode_auth(login, token)

    @staticmethod
    def parse_auth(entries):
        """Parses authentication entries.

        Args:
          entries (dict): Dict of authentication entries.

        Returns:
          Authentication registry.
        """
        auth = entries.get("auth", "")
        return decode_auth(auth)

    def load(self, config_path):
        with open(config_path, "r") as fileptr:
            cfg = json.load(fileptr)
            data = dict()
            data["login"], data["token"] = self.parse_auth(cfg)
            data["base_url"] = cfg.get("base_url", "")
            data["company"] = cfg.get("company", "")

        self.set(**data)
        return self

    def save(self, filename):

        dirname = os.path.dirname(os.path.abspath(filename))
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with open(filename, "w") as fileptr:
            data = dict(
                auth=self.auth,
                company=self.__dict__.get("company"),
                base_url=self.__dict__.get("base_url"),
            )
            json.dump(data, fileptr)
        return self

    def __str__(self):
        return str(self.as_dict())
