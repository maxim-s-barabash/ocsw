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

"""Manage Edge Actions."""

import asyncio

from ..utils import render
from ..utils.format_pretty_json import pprintj
from ..utils.helpers import get
from ..utils.table import ObjTable


async def cmd_edge_actions_inspect(client, edge_actions, **_kwargs):
    """Display detailed information on one or more edge actions.

    Args:
        client (ocsw.api.client.APIClient): APIClient
        edge_actions (list): list of edge actions id
    """
    futures = [client.inspect_edge_action(uid) for uid in edge_actions]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_edge_actions_ls(client, **_kwargs):

    fields = [
        "id",
        "description",
        "disabled",
        "lastEditDate",
        "source",
        "version",
        # "companyId",
    ]
    resp = await client.edge_actions(
        fields=fields,
        sort="description",
        limit=1000,  # TODO: set from configure
    )

    list_data = resp.get("body")

    columns = [
        dict(field="id", title="ID"),
        dict(field="description", title="NAME", render=render.map),
        dict(field="disabled", title="DISABLED", render=render.yes_no),
        dict(
            field="lastEditDate",
            title="UPDATE DATE",
            render=render.timestamp_delta,
        ),
        dict(
            field="source",
            title="OBSERVATION",
            render=lambda d, c: get(d, c["field"], "").split("://")[-1],
        ),
        dict(field="version", title="VERSION", render=render.map),
        # dict(field="companyId")
    ]

    table = ObjTable(data=list_data, columns=columns)
    print(table)


def init_cli(subparsers):
    prompt = "Manage edge actions"
    parser = subparsers.add_parser(
        "edge_action", help=prompt, description=prompt
    )
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect",
        help="display detailed information on one or more edge actions",
    )
    parser_inspect.set_defaults(func=cmd_edge_actions_inspect)
    parser_inspect.add_argument(
        "edge_actions",
        metavar="ACTION",
        nargs="+",
        help="edge action id or name",
    )

    # LS
    parser_lc = sub.add_parser("ls", help="list edge action")
    parser_lc.set_defaults(func=cmd_edge_actions_ls)
