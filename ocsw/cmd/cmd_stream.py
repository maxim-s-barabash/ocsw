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

"""Manage streams and events."""

import asyncio

from ..utils import render
from ..utils.format_pretty_json import pprintj
from ..utils.table import ObjTable


async def cmd_stream_inspect(client, streams, **_kwargs):
    futures = [client.inspect_stream(uid) for uid in streams]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_stream_ls(client, **_kwargs):

    fields = [
        "id",
        # 'name',
        # 'creatorId'
        # # 'creationDate',
        "lastEditDate",
        # 'lastEditorId',
        "description",
        "capacity",
        "path",
    ]

    resp = await client.streams(fields=fields, limit=20, start=40)
    data = resp.get("body")

    columns = [
        dict(field="id", title="ID"),
        dict(
            field="lastEditDate",
            title="LAST CHANGE",
            render=render.timestamp_delta,
        ),
        dict(field="description", title="DESCRIPTION"),
        dict(field="capacity", title="CAPACITY"),
        dict(field="path", title="PATH"),
    ]

    table = ObjTable(data=data, columns=columns)
    print(table)


async def cmd_stream_events_list(client, stream, **_kwargs):

    fields = [
        # 'id',
        # 'streamId',
        # 'creatorId',
        # 'lastEditorId',
        # 'metadata',
        # 'creationDate',
        "lastEditDate",
        "generatedDate",
        # 'path',
        "location",
        # 'hash',
        "tags",
        "elems",
    ]

    resp = await client.events(stream, fields=fields)
    data = resp.get("body")

    columns = [
        # dict(field='id', title='ID'),
        # dict(field='creationDate', title='creationDate',
        #      render=render.timestamp_delta),
        dict(
            field="lastEditDate",
            title="LAST CHANGE",
            render=render.timestamp_delta,
        ),
        # dict(field='generatedDate', title='generatedDate',
        #      render=render.timestamp_delta),
        # dict(field='hash', title='hash'),
        # dict(field='metadata', title='metadata'),
        # dict(field='path', title='PATH'),
        # dict(field='tags', title='tags'),
        dict(field="elems", title="elems", width=65),
    ]

    table = ObjTable(data=data, columns=columns,)
    print(table)


def init_cli(subparsers):
    prompt = "Manage streams"
    parser = subparsers.add_parser("stream", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # LS
    parser_ls = sub.add_parser("ls", help="display streams list")
    parser_ls.set_defaults(func=cmd_stream_ls)

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect", help="display detailed information on one or more streams"
    )
    parser_inspect.set_defaults(func=cmd_stream_inspect)
    parser_inspect.add_argument(
        "streams", metavar="STREAM", nargs="+", help="stream id"
    )

    # EVENT
    parser_events = sub.add_parser("events", help="display stream events list")
    parser_events.set_defaults(func=cmd_stream_events_list)
    parser_events.add_argument(
        "stream", metavar="STREAM", help="stream id or path"
    )
