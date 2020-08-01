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

"""Cell value render."""

from .date_fns import distance_in_words_to_now
from .helpers import get

__all__ = ("map", "yes_no", "timestamp_delta")


def map(row_data, column_options):
    """Get string value in structure.

    column_options["field"] - must be separated by dots

    Args:
        row_data (dict): an object containing a value
        column_options (dict): column options {field, default}

    Returns:
        str: value
    """
    field = column_options.get("field")
    default = column_options.get("default", "")
    val = get(row_data, field, default)
    return str(val)


def yes_no(row_data, column_options):
    """Convert bollean value to "yes" on "no".

    Args:
        row_data (dict): an object containing a value
        column_options (dict): column options {field, default}

    Returns:
        string: "yes" or "no"
    """
    field = column_options.get("field")
    default = column_options.get("default", None)
    val = get(row_data, field, default)
    if val is None:
        return ""
    return "yes" if val else "no"


def timestamp_delta(row_data, column_options):
    """Convert timestamp value to human readable time delta.

    Args:
        row_data (dict): an object containing a value
        column_options (dict): column options {field, default}

    Returns:
        str: human readable time delta
    """
    field = column_options.get("field")
    default = column_options.get("default", None)
    val = get(row_data, field, default)
    return distance_in_words_to_now(val) if val else ""
