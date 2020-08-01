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

"""Manage Devices."""

import asyncio
from operator import itemgetter

from ..utils import render
from ..utils.argparse_action import KeyValueAction
from ..utils.format_date import format_date
from ..utils.format_pretty_json import pprintj
from ..utils.helpers import get
from ..utils.table import ObjTable


async def cmd_devices_inspect(client, devices, **_kwargs):
    """Display detailed information on one or more device.

    Args:
        client (ocsw.api.client.APIClient): APIClient
        devices (list): list of device id or name
    """
    futures = [client.inspect_device(uid) for uid in devices]
    items = [resp.get("body") for resp in await asyncio.gather(*futures)]
    pprintj(items)


async def cmd_device_ls(client, show_tags, **_kwargs):
    """List devices connectivity."""
    fields = [
        "id",
        "displayName",
        "name",
        "lastEditDate",
        "lastSeen",
        "synced",
        "report",
    ]

    columns = [
        # dict(field='id', title='ID'),
        dict(field="name", title="NAME"),
        dict(field="displayName", title="DISPLAY NAME"),
        dict(
            field="lastSeen", title="LAST SEEN", render=render.timestamp_delta
        ),
        dict(
            field="lastEditDate",
            title="LAST CHANGE",
            render=render.timestamp_delta,
        ),
        dict(field="synced", title="SYNCED", render=render.yes_no),
        dict(
            field="report.developerMode.enable.value",
            title="DEV MODE",
            render=render.yes_no,
            default=False,
        ),
        dict(
            field="report.signal.bars.value", title="BARS", render=render.map
        ),
        dict(field="report.signal.rat.value", title="RAT", render=render.map),
        dict(
            field="report.battery.voltage.value",
            title="BATTERY",
            render=render.map,
            default="?",
        ),
    ]
    if show_tags:
        fields.append("tags")
        columns.append(dict(field="tags", title="TAGS"))

    resp = await client.devices(fields=fields)
    data = resp.get("body")

    table = ObjTable(data=data, columns=columns)
    print(table)


async def cmd_device_lc(client, show_tags, **_kwargs):
    """List devices configuration."""
    fields = [
        "id",
        "displayName",
        "name",
        "synced",
        "dirty",
        "lastEditDate",
        "localVersions",
    ]
    columns = [
        # dict(field='id', title='ID'),
        dict(field="name", title="NAME"),
        dict(field="displayName", title="DISPLAY NAME"),
        dict(
            field="blueprint.displayName",
            title="BLUEPRINT NAME",
            render=render.map,
        ),
        dict(
            field="localVersions.blueprintVersion",
            title="VERSION",
            render=render.map,
        ),
        dict(field="dirty", title="DIRTY", render=render.yes_no),
        dict(
            field="lastEditDate",
            title="LAST CHANGE",
            render=render.timestamp_delta,
        ),
        dict(field="synced", title="SYNCED", render=render.yes_no),
        dict(field="localVersions.edge", title="EDGE", render=render.map),
        dict(
            field="localVersions.firmware",
            title="FIRMWARE VERSION",
            render=render.map,
        ),
        dict(field="localVersions.legato", title="LEGATO", render=render.map),
    ]

    # "{{.name}}"
    # "{{.displayName}}"
    # "{{.blueprint.displayName}}"
    # "{{.localVersions.blueprintVersion}}"
    # "{{.dirty|yes_no}}"
    # "{{.lastEditDate|timestamp_delta}}"
    # "{{.synced|yes_no}}"
    # "{{.localVersions.edge}}"
    # "{{.localVersions.firmware}}"
    # "{{.localVersions.legato}}"

    if show_tags:
        fields.append("tags")
        columns.append(dict(field="tags", title="TAGS"))

    # devices
    devices_resp = await client.devices(fields=fields)
    devices_data = devices_resp.get("body")
    # blueprints
    blueprints_resp = await client.blueprints(fields=["id", "displayName"])

    # map devices and blueprints
    index_blueprints = dict(
        (blueprint.get("id"), blueprint)
        for blueprint in blueprints_resp.get("body")
    )
    for device in devices_data:
        blueprint_id = get(device, "localVersions.blueprintId")
        device["blueprint"] = index_blueprints.get(blueprint_id)

    table = ObjTable(data=devices_data, columns=columns)
    print(table)


async def cmd_device_li(client, show_tags, **_kwargs):
    """List devices identity."""
    fields = [
        "id",
        "displayName",
        "name",
        "creationDate",
        "hardware",
    ]

    columns = [
        dict(field="name", title="NAME"),
        dict(field="displayName", title="DISPLAY NAME"),
        dict(
            field="creationDate",
            title="CREATION DATE",
            render=render.timestamp_delta,
        ),
        dict(
            field="event.0.creationDate",
            title="LAST EVENT",
            render=render.timestamp_delta,
        ),
        dict(field="hardware.model", title="MODEL", render=render.map),
        dict(field="hardware.module", title="MODULE", render=render.map),
        dict(field="hardware.fsn", title="SERIAL NUMBER", render=render.map),
        dict(field="hardware.imei", title="IMEI", render=render.map),
        # dict(field='hardware.iccid', title='ICCID', render=render.map),
        dict(field="hardware.countryCode", title="COUNTRY", render=render.map),
        dict(field="id", title="ID"),
    ]
    if show_tags:
        fields.append("tags")
        columns.append(dict(field="tags", title="TAGS"))

    resp = await client.devices(fields=fields)
    data = resp.get("body")

    futures = [
        client.events(
            f'/{client.current_company}/devices/{item["name"]}/:inbox',
            limit=1,
            order="desc",
            fields=["id", "elems", "creationDate", "path"],
        )
        for item in data
    ]
    # futures = [
    #     client.device_events(
    #         f'{item["name"]}/:inbox',
    #         limit=1,
    #         order="desc",
    #         fields=["id", "elems", "creationDate", "path"],
    #     )
    #     for item in data
    # ]

    resp = await asyncio.gather(*futures)
    for idx, item in enumerate(data):
        item["event"] = resp[idx].get("body")

    table = ObjTable(data=data, columns=columns)
    print(table)


async def cmd_device_actions(client, device_identifier, **_kwargs):
    fields = [
        "localActions",
        "path",
    ]
    resp = await client.inspect_device(
        device_identifier, fields=fields, refs=1
    )

    local_actions = get(resp, "head.references.localAction", {})
    list_data = sorted(local_actions.values(), key=itemgetter("description"))

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
    ]

    table = ObjTable(data=list_data, columns=columns)
    print(table)


async def cmd_device_tags(client, device_identifier, tags, **_kwargs):
    """Set device tags. All tags are replaced with new ones."""
    props = dict(tags=tags)
    fields = ["id", "tags"]
    resp = await client.update_device(
        device_identifier, fields=fields, props=props
    )
    pprintj(resp)


async def cmd_device_recent_events(client, device_identifier, **_kwargs):

    resp = await client.inspect_device(
        device_identifier, fields=["id", "name", "path"]
    )
    device_data = resp.get("body")
    device_path = device_data["path"]

    resp = await client.device_events(
        device_identifier,
        fields=["elems", "creationDate", "path"],
        filters=f'path!="{device_path}/:inbox"',
        sort="creationDate",
        order="desc",
    )

    data = resp.get("body")
    columns = [
        dict(
            field="creationDate",
            title="creationDate",
            render=lambda a, b: format_date(
                a[b["field"]], "%b %d, %Y %X %Z%z"
            ),
        ),
        dict(
            field="path",
            title="EVENT FROM",
            render=lambda a, b: a["path"].split(f"{device_path}/")[-1],
        ),
        dict(field="elems", width=70),
    ]

    table = ObjTable(data=data, columns=columns)
    print(table)


async def cmd_device_recent_changes(client, device_identifier, **_kwargs):

    resp = await client.inspect_device(
        device_identifier, fields=["id", "name", "path"]
    )
    device_data = resp.get("body")
    device_path = device_data["path"]

    resp = await client.events(
        f"{device_path}/:inbox",
        fields=["elems", "creationDate", "path"],
        sort="creationDate",
        order="desc",
    )

    data = resp.get("body")
    columns = [
        dict(
            field="creationDate",
            title="creationDate",
            render=lambda a, b: format_date(
                a[b["field"]], "%b %d, %Y %X %Z%z"
            ),
        ),
        dict(field="elems", width=70),
        # dict(field='path')
    ]

    table = ObjTable(data=data, columns=columns)
    print(table)


async def cmd_device_create(client, name, imei, fsn, **_kwargs):
    resp = await client.create_device(name, imei, fsn)
    pprintj(resp)


async def cmd_device_rm(client, devices, **_kwargs):
    for device_identifier in devices:
        resp = await client.remove_device(device_identifier)
        messages = resp.get("messages") or []
        print("\n".join(messages))


def init_cli(subparsers):
    prompt = "Manage devices"
    parser = subparsers.add_parser("device", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # EDGE ACTIONS
    parser_actions = sub.add_parser("actions", help="list device edge actions")
    parser_actions.set_defaults(func=cmd_device_actions)
    parser_actions.add_argument(
        "device_identifier", metavar="DEVICE", help="device id or name"
    )

    # CREATE
    parser_create = sub.add_parser("create", help="creating device")
    parser_create.set_defaults(func=cmd_device_create)
    parser_create.add_argument(
        "-n", "--name", required=True, help="device name, "
    )
    parser_create.add_argument(
        "-i", "--imei", required=True, help="IMEI of the Device"
    )
    parser_create.add_argument(
        "-f", "--fsn", required=True, help="serial number of the device"
    )

    # INSPECT
    parser_inspect = sub.add_parser(
        "inspect", help="display detailed information on one or more devices"
    )
    parser_inspect.set_defaults(func=cmd_devices_inspect)
    parser_inspect.add_argument(
        "devices", metavar="DEVICE", nargs="+", help="device id or name"
    )

    # LC
    parser_lc = sub.add_parser("lc", help="list devices configuration")
    parser_lc.set_defaults(func=cmd_device_lc)
    parser_lc.add_argument(
        "-t",
        "--tags",
        dest="show_tags",
        action="store_true",
        help="show device tags",
    )

    # LI
    parser_li = sub.add_parser("li", help="list devices identity")
    parser_li.set_defaults(func=cmd_device_li)
    parser_li.add_argument(
        "-t",
        "--tags",
        dest="show_tags",
        action="store_true",
        help="show device tags",
    )
    # LS
    parser_ls = sub.add_parser("ls", help="list devices connectivity")
    parser_ls.set_defaults(func=cmd_device_ls)
    parser_ls.add_argument(
        "-t",
        "--tags",
        dest="show_tags",
        action="store_true",
        help="show device tags",
    )
    # RM
    parser_rm = sub.add_parser("rm", help="remove one or more devices")
    parser_rm.set_defaults(func=cmd_device_rm)
    parser_rm.add_argument(
        "devices", metavar="DEVICE", nargs="+", help="device id or name"
    )

    # TAGS
    parser_tags = sub.add_parser("tags", help="set device tags")
    parser_tags.set_defaults(func=cmd_device_tags)
    parser_tags.add_argument(
        "device_identifier", metavar="DEVICE", help="device id or name"
    )
    parser_tags.add_argument(
        "tags",
        metavar="TAG=VALUE",
        nargs="*",
        action=KeyValueAction,
        help="add category=value params",
    )

    # Recent events
    parser_events = sub.add_parser("events", help="display recent events")
    parser_events.set_defaults(func=cmd_device_recent_events)
    parser_events.add_argument(
        "device_identifier", metavar="DEVICE", help="device id or name"
    )

    # Recent events
    parser_events = sub.add_parser("changes", help="display recent changes")
    parser_events.set_defaults(func=cmd_device_recent_changes)
    parser_events.add_argument(
        "device_identifier", metavar="DEVICE", help="device id or name"
    )
