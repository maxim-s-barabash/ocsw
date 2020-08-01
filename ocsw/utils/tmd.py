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

import textwrap

BOLD_STYLE = "\x1b[01m"
RESET_STYLE = "\x1b[00m"

__all__ = ("render_md",)


def render_md(md_text, width=79):
    """Render markdown text to text displays on console.

    Args:
        md_text (str): markdown test.
        width (int, optional): width of displayed text. Defaults to 79.

    Returns:
        str: text for output on console.
    """
    output = []
    for paragraph in md_text.splitlines(True):
        style = paragraph_style(paragraph)
        paragraph = html_paragraph(paragraph)

        indent = bullet_indent(paragraph)
        lines = textwrap.wrap(paragraph, width=width, subsequent_indent=indent)
        lines = lines or [""]

        if style:
            lines[0] = style + lines[0]
            lines[-1] = lines[-1] + RESET_STYLE
        output.extend(lines)

    return "\n".join(output)


def bullet_indent(paragraph):
    subsequent_indent = ""
    if paragraph.startswith("* "):
        subsequent_indent = "  "
    return subsequent_indent


def html_paragraph(paragraph):
    if paragraph.strip().lower() in ["<br />", "<br/>", "<br>"]:
        paragraph = "\n"
    return paragraph


def paragraph_style(paragraph):
    style = ""
    if paragraph.startswith("#"):
        style = BOLD_STYLE
    return style
