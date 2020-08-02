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

"""Manage Firmwares."""

from ..utils import render
from ..utils.format_date import format_date
from ..utils.table import ObjTable, PropTable
from ..utils.tmd import render_md


async def cmd_firmware_note(client, firmwares, **_kwargs):

    resp = await client.firmwares()
    data = resp.get("body")
    list_firmwares = [i for i in data if i.get("id") in firmwares]

    props_row = [
        dict(name="name", label="Firmware Name"),
        dict(name="id", label="Id"),
        dict(name="version", label="Version"),
        dict(name="creationDate", label="Creation Date", render=format_date),
        dict(name="module", label="Model"),
        dict(name="modemFirmware", label="Modem Firmware"),
        dict(name="legato", label="Legato"),
    ]

    output = []
    for item in list_firmwares:

        table = str(PropTable(item, props_row))
        output.append(table)

        notes = item.get("notes", "")
        output.extend(["Notes", "", render_md(notes)])

    print("\n".join(output))


async def cmd_firmware_ls(client, **_kwargs):

    columns = [
        dict(field="id", title="ID"),
        dict(
            field="creationDate",
            title="CREATION DATE",
            render=render.timestamp_delta,
        ),
        dict(field="version", title="VERSION"),
        # dict(field='creatorId', title='creatorId'),
        dict(field="legato", title="LEGATO"),
        dict(field="model", title="MODEL"),
        dict(field="modemFirmware", title="MODEM FIRMWARE"),
        dict(field="module", title="MODULE"),
        dict(field="name", title="NAME"),
    ]

    resp = await client.firmwares()
    data = resp.get("body")

    table = ObjTable(data=data, columns=columns)
    print(table)


def init_cli(subparsers):
    prompt = "Manage firmware"
    parser = subparsers.add_parser("firmware", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # LS
    parser_ls = sub.add_parser("ls", help="list of available firmware")
    parser_ls.set_defaults(func=cmd_firmware_ls)

    # INSPECT
    parser_inspect = sub.add_parser(
        "note", help="display notes on one or more firmware"
    )
    parser_inspect.set_defaults(func=cmd_firmware_note)
    parser_inspect.add_argument(
        "firmwares", metavar="FIRMWARE", nargs="+", help="firmware id"
    )
