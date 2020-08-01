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

"""Manage Companies."""
import asyncio
import os

from .. import errors
from ..utils import render
from ..utils.config import Config
from ..utils.format_pretty_json import pprintj
from ..utils.helpers import get_company_name
from ..utils.table import ObjTable


async def cmd_inspect(client, companies, **_kwargs):
    futures = [client.inspect_company(uid) for uid in companies]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_ls(client, **_kwargs):
    fields = [
        "id",
        "name",
        "displayName",
        "creationDate",
        "lastEditDate",
    ]
    current_company = client.current_company
    columns = [
        dict(field="id", title="ID"),
        dict(
            field="name",
            title="NAME",
            render=lambda d, c: d.get(c["field"], "")
            + (" (current)" if d.get(c["field"]) == current_company else ""),
        ),
        dict(field="displayName", title="DISPLAY NAME"),
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
    ]

    resp = await client.companies(fields=fields)
    data = resp.get("body")
    table = ObjTable(data=data, columns=columns)
    print(table)


async def cmd_switch(client, config_path, config_filename, company, **_kwargs):
    """Switch company."""
    resp = await client.companies(fields=["id", "name"])
    data = resp.get("body")
    company_name = get_company_name(data, company)
    if not company_name:
        raise errors.NotFound(f"Company {company} not found")

    filename = os.path.join(config_path, config_filename)
    config = Config(filename)
    config.company = company_name
    config.save(filename)


def init_cli(subparsers):
    prompt = "Manage companies"
    parser = subparsers.add_parser("company", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # LS
    parser_ls = sub.add_parser("ls", help="display company list")
    parser_ls.set_defaults(func=cmd_ls)

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect", help="display detailed information on one or more companies"
    )
    parser_inspect.set_defaults(func=cmd_inspect)
    parser_inspect.add_argument(
        "companies", metavar="COMPANY", nargs="+", help="company id"
    )

    # SWITCH
    parser_switch = sub.add_parser("switch", help="set company active")
    parser_switch.set_defaults(func=cmd_switch)
    parser_switch.add_argument(
        "company", metavar="COMPANY", help="company id or name"
    )
