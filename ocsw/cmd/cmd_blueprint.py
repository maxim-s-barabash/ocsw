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

"""Manage Blueprints.

A Blueprint captures the current device's resources, Observations,
Edge Actions, services, and firmware, as a versioned configuration
Blueprint that can be applied to other devices. This is useful for
Applying Blueprints the same settings to multiple devices.
"""

import asyncio

from ..utils import render
from ..utils.format_pretty_json import pprintj
from ..utils.table import ObjTable


async def cmd_blueprint_inspect(
    client, blueprints, version_number=None, **_kwargs
):
    """Display detailed information on one or more blueprints.

    Args:
        client (ocsw.api.client.APIClient): APIClient
        blueprints (list): list of blueprints id
        version_number (int): version of the requested object
    """
    futures = [
        client.inspect_blueprint(uid, version_number=version_number)
        for uid in blueprints
    ]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_blueprint_ls(client, **_kwargs):
    fields = ["id", "displayName", "creationDate", "lastEditDate", "version"]

    columns = [
        dict(field="id", title="ID"),
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
        # dict(field='lastEditDate', title='LAST EDIT DATE',
        #      render=render.timestamp_delta),
        # dict(field='lastSeen', title='LAST SEEN',
        #      render=render.timestamp_delta),
        # dict(field='state', title='STATE'),
        dict(field="version", title="VERSION"),
        # dict(field='observations', title='observations'),
    ]

    resp = await client.blueprints(fields=fields)
    data = resp.get("body")

    table = ObjTable(data=data, columns=columns)
    print(table)


def init_cli(subparsers):
    prompt = "Manage blueprints"
    parser = subparsers.add_parser(
        "blueprint", help=prompt, description=prompt
    )
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    parser_ls = sub.add_parser("ls", help="display blueprint list")
    parser_ls.set_defaults(func=cmd_blueprint_ls)

    parser_inspect = sub.add_parser(
        "inspect",
        help="display detailed information on one or more blueprints",
    )
    parser_inspect.set_defaults(func=cmd_blueprint_inspect)
    parser_inspect.add_argument(
        "-v",
        "--version",
        dest="version_number",
        type=int,
        help="version of the cloud action",
    )
    parser_inspect.add_argument(
        "blueprints", metavar="BLUEPRINT", nargs="+", help="blueprint id"
    )
