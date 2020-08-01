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

"""Release Notes."""

from ..utils.format_date import format_date
from ..utils.tmd import render_md


async def cmd_release_note(client, **_kwargs):
    """Prints version and release notes."""
    resp = await client.release_note(order="asc", limit=0)
    data = resp.get("body")

    for item in data:
        version = item.get("version", "Unknown")
        date = format_date(item.get("creationDate", 0), template="%B %dth, %Y")
        notes = f"# Version: {version} - {date}\n"
        notes += item.get("notes", "")
        notes += "\n\n"
        print(render_md(notes, width=79))


def init_cli(subparsers):
    prompt = "Display Octave API Version Information"
    parser = subparsers.add_parser("release", help=prompt, description=prompt)
    parser.set_defaults(func=cmd_release_note)
