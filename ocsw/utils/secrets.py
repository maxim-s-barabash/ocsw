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

import copy

from ..constants import MASKED_ATTRIBUTE_VALUE


def replace(data, match, repl):
    """Replace values for all key in match on repl value.

    Recursively apply a function to values in a dict or list until the input
    data is neither a dict nor a list.
    """
    if isinstance(data, dict):
        return {
            key: repl if key in match else replace(value, match, repl)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [replace(item, match, repl) for item in data]

    return data


def mask_secrets(structure, secrets, masked_value=MASKED_ATTRIBUTE_VALUE):
    """Replaces values in keys that are not for public distribution.

    Args:
        structure ([dict, list]): structure in which must to hide the values.
        secrets (list): key names
        masked_value (str): replace with this value

    Returns:
        [list, dict]: new structure
    """
    result = copy.deepcopy(structure)
    result = replace(result, secrets, masked_value)
    return result
