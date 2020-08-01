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

"""Octave Cloud authentication and auth configuration saving."""

import getpass
import os

from ..api.client import APIClient
from ..utils.config import Config
from ..utils.helpers import match_company_name


def request_auth(login=None, token=None):
    """Interactively request a missed login, token from the console.

    Args:
        login (str): login
        token (str): token

    Returns:
        dict: auth {login, token}
    """
    auth = dict(
        login=login or input("User name: "),
        token=token or getpass.getpass("Token: "),
    )
    return auth


async def cmd_login(
    config_path, config_filename, username, token, company=None, **_kwargs
):
    """Wizard to create a configuration file."""
    print(
        "Login with your token from Octave Cloud. "
        "If you don't have a token, head over to "
        "https://octave.sierrawireless.io/ to create one."
    )
    try:
        auth = request_auth(username, token)
    except KeyboardInterrupt:
        return

    filename = os.path.join(config_path, config_filename)

    config = Config(filename, **auth)
    client = APIClient(**config.as_dict())
    resp = await client.companies(fields=["id", "name"])

    config.set(company=match_company_name(resp.get("body"), company))
    config.save(filename)
    print(f"WARNING! Your token will be stored unencrypted in {filename!s}.")


def init_cli(subparsers):
    prompt = "Log in to a Octave Cloud"
    parser = subparsers.add_parser("login", help=prompt, description=prompt)
    parser.set_defaults(func=cmd_login)
    parser.add_argument(
        "company", metavar="COMPANY", nargs="?", help="company name"
    )
    parser.add_argument("-t", "--token", metavar="", help="token")
    parser.add_argument("-u", "--username", metavar="", help="username")
