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

"""Manage users."""

import asyncio

from ..utils import render
from ..utils.format_pretty_json import pprintj
from ..utils.secrets import mask_secrets
from ..utils.table import ObjTable


async def cmd_users_inspect(client, users, show_secrets=False, **_kwargs):
    futures = [client.inspect_identity(uid) for uid in users]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    if not show_secrets:
        items = mask_secrets(items, ["requestId", "masterToken"])
    pprintj(items)


async def cmd_user_ls(client, **_kwargs):
    columns = [
        dict(field="id", title="ID"),
        dict(field="name", title="USER NAME"),
        dict(field="firstName", title="FIRST NAME"),
        dict(field="lastName", title="LAST NAME"),
        dict(field="email", title="E-MAIL"),
        dict(
            field="creationDate",
            title="CREATION DATE",
            render=render.timestamp_delta,
        ),
    ]
    resp = await client.identities()
    data = resp.get("body")
    table = ObjTable(data=data, columns=columns)
    print(table)


def init_cli(subparsers):
    prompt = "Manage users"
    parser = subparsers.add_parser("user", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # LS
    parser_ls = sub.add_parser("ls", help="display user list")
    parser_ls.set_defaults(func=cmd_user_ls)

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect", help="display detailed information on one or more users"
    )
    parser_inspect.set_defaults(func=cmd_users_inspect)
    parser_inspect.add_argument(
        "users", metavar="USER", nargs="+", help="user id"
    )
