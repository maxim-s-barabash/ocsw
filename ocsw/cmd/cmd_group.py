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

"""Manage user groups."""

import asyncio

from ..utils import render
from ..utils.format_pretty_json import pprintj
from ..utils.table import ObjTable


async def cmd_group_inspect(client, groups, **_kwargs):
    futures = [client.inspect_group(uid) for uid in groups]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_group_ls(client, **_kwargs):
    fields = []
    resp = await client.groups(fields=fields, refs=1)
    data = resp.get("body")

    columns = [
        dict(field="id", title="ID"),
        dict(field="displayName", title="NAME"),
        dict(
            field="creationDate",
            title="CREATION DATE",
            render=render.timestamp_delta,
        ),
        dict(
            field="lastEditDate",
            title="LAST EDIT DATE",
            render=render.timestamp_delta,
        ),
        dict(field="description", title="DESCRIPTION"),
        dict(
            field="memberIds",
            title="NUMBER MEMBER",
            render=lambda d, c: len(d.get(c["field"])),
        ),
    ]

    table = ObjTable(data=data, columns=columns)
    print(table)


def init_cli(subparsers):
    prompt = "Manage user groups"
    parser = subparsers.add_parser("group", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # LS
    parser_ls = sub.add_parser("ls", help="display user group list")
    parser_ls.set_defaults(func=cmd_group_ls)

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect",
        help="display detailed information on one or more user groups",
    )
    parser_inspect.set_defaults(func=cmd_group_inspect)
    parser_inspect.add_argument(
        "groups", metavar="GROUP", nargs="+", help="group id"
    )
