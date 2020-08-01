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

"""Data in the form of a table.

obj_table - designed to make it quick and easy to represent data in visually
appealing ASCII tables.
"""

import logging
from collections import defaultdict
from copy import deepcopy
from textwrap import wrap

__all__ = ("ObjTable", "PropTable")
ALIGN_LEFT = "<"
ALIGN_CENTER = "^"
ALIGN_RIGHT = ">"
LOG = logging.getLogger(__name__)


def cell_render(row_data, column_options):
    render = column_options.get("render")
    if render:
        val = render(row_data, column_options)
    else:
        field = column_options.get("field")
        val = row_data.get(field, "")
    return str(val)


def wrap_cells(row, columns):
    """Breaks into lines of the row."""
    new_row = []
    for cell_idx, cell in enumerate(row):
        column = columns[cell_idx]
        width = column["width"]
        template = column["template"]
        new_cell = [template.format(line) for line in wrap(cell, width=width)]
        new_row.append(new_cell)
    return new_row


def expand_cells(row, columns):
    """Expand the height of each cell to the height of the row."""
    height = max([len(cell) for cell in row])
    new_row = []
    for cell_idx, cell in enumerate(row):
        width = columns[cell_idx]["width"]
        blank = " " * width
        new_row.append(cell + [blank] * (height - len(cell)))
    return list(zip(*new_row))


def compute_widths(rows):
    widths = defaultdict(int)
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(len(cell), widths[idx])
    return widths


class ObjTable:
    """Render data as table.

    data - array[dict]
    columns - array[dict{
        title (optional) str
        field (optional) str
        render (optional) function(row_data:dict, column:dict)
        align (optional) "<", "^", ">"
        width (optional) int - max column width
        template (optional) str - custom column template
    }]
    """

    def __init__(self, data=None, columns=None, padding_right=3):
        self.data = data or []
        self.columns = columns or []
        self.padding_right = padding_right

    def row_render(self, row_data):
        return [cell_render(row_data, column) for column in self.columns]

    def rows_render(self):
        return [self.row_render(row_data) for row_data in self.data]

    def get_header_row(self):
        return [
            obj.get("title", obj.get("field")) or "" for obj in self.columns
        ]

    def get_columns(self, common_data):
        widths = compute_widths(common_data)
        columns = deepcopy(self.columns)
        for idx, column in enumerate(columns):
            column.setdefault("align", ALIGN_LEFT)
            column.setdefault("width", widths[idx])
            if column["align"] not in (ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT):
                LOG.warning("Invalid alignment value: %s", column["align"])
                column["align"] = ALIGN_LEFT

            column.setdefault(
                "template", "{{: {align}{width}s}}".format(**column)
            )
        return columns

    def stringify(self):
        header_row = self.get_header_row()
        data_rows = self.rows_render()
        common_data = [header_row] + data_rows
        columns = self.get_columns(common_data)

        new_rows = []
        for row in common_data:
            new_row = wrap_cells(row, columns)
            new_row = expand_cells(new_row, columns)
            new_rows.extend(new_row)

        padding_right = " " * self.padding_right
        pad = padding_right

        lines = [pad.join(row) for row in new_rows]
        return "\n".join(lines)

    def __str__(self):
        return self.stringify()


class PropTable(ObjTable):
    """PropTable for dict output, key value as table.

    >>> from datetime import date
    >>> item = {"date": 1595577615.600, "model": "MODEL-1234"}
    >>> props_row = [
    ...    {"name": "date", "label": "Date", "render": date.fromtimestamp},
    ...    {"name": "model", "label": "Model"}
    ... ]
    >>> print(PropTable(item, props_row))
    Date    2020-07-24
    Model   MODEL-1234
    """

    def __init__(self, item, props_row, padding_right=3):
        columns = [
            dict(field="key", title=""),
            dict(field="value", title=""),
        ]

        super(PropTable, self).__init__(
            data=self._prepare_date(item, props_row),
            columns=columns,
            padding_right=padding_right,
        )

    @staticmethod
    def _prepare_date(item, props_row):
        data = []
        for row in props_row:
            prop_name = row.get("name")
            if prop_name not in item:
                continue
            label = row.get("label", prop_name)
            render = row.get("render", str)
            value = render(item[prop_name])
            data.append(dict(key=label, value=value))
        return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
