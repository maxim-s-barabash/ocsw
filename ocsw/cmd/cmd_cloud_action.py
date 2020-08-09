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

"""Manage Cloud Actions."""

import asyncio
import difflib

from ..utils import render
from ..utils.color_diff import color_diff
from ..utils.format_date import ISO_8601, format_date
from ..utils.format_pretty_json import pprintj
from ..utils.table import ObjTable


async def cmd_cloud_actions_inspect(
    client, cloud_actions, version_number=None, **_kwargs
):
    """Display detailed information on one or more cloud actions.

    Args:
        client (ocsw.api.client.APIClient): APIClient
        cloud_actions (list): list of cloud actions id
        version_number (int): version of the requested object
    """
    futures = [
        client.inspect_action(uid, version_number=version_number)
        for uid in cloud_actions
    ]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_cloud_actions_ls(client, **_kwargs):

    fields = [
        "id",
        "description",
        "disabled",
        "lastEditDate",
        "source",
        "version",
        # "companyId",
    ]
    resp = await client.actions(
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
        dict(field="source", title="OBSERVATION"),
        dict(field="version", title="VERSION", render=render.map),
        # dict(field="companyId")
    ]

    table = ObjTable(data=list_data, columns=columns)
    print(table)


async def cmd_cloud_actions_diff(
    client, cloud_action, version_number=None, **_kwargs
):
    to_data_resp = await client.inspect_action(
        cloud_action, version_number=version_number
    )
    to_data = to_data_resp.get("body")
    to_version = to_data.get("version")

    from_version = max(1, to_version - 1)

    from_data_resp = await client.inspect_action(
        cloud_action, version_number=from_version
    )
    from_data = from_data_resp.get("body")
    diff = difflib.unified_diff(
        from_data.get("js").splitlines(keepends=True),
        to_data.get("js").splitlines(keepends=True),
        fromfile="{id}_v{version}_{description}".format(**from_data),
        tofile="{id}_v{version}_{description}".format(**to_data),
        fromfiledate=format_date(
            from_data.get("lastEditDate"), template=ISO_8601
        ),
        tofiledate=format_date(to_data.get("lastEditDate"), template=ISO_8601),
    )

    print("".join(color_diff(diff)))


def init_cli(subparsers):
    prompt = "Manage cloud actions"
    parser = subparsers.add_parser(
        "cloud_action", help=prompt, description=prompt
    )
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect",
        help="display detailed information on one or more cloud actions",
    )
    parser_inspect.set_defaults(func=cmd_cloud_actions_inspect)
    parser_inspect.add_argument(
        "-v",
        "--version",
        dest="version_number",
        type=int,
        help="version of the cloud action",
    )
    parser_inspect.add_argument(
        "cloud_actions", metavar="ACTION", nargs="+", help="cloud action id",
    )

    # LS
    parser_lc = sub.add_parser("ls", help="list cloud action")
    parser_lc.set_defaults(func=cmd_cloud_actions_ls)

    # DIFF
    parser_diff = sub.add_parser(
        "diff", help="differences in javascript between cloud action versions"
    )
    parser_diff.set_defaults(func=cmd_cloud_actions_diff)
    parser_diff.add_argument(
        "-v",
        "--version",
        dest="version_number",
        type=int,
        help="version of the cloud action",
    )
    parser_diff.add_argument(
        "cloud_action", metavar="ACTION", help="cloud action id",
    )
