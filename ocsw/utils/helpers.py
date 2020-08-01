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

"""Various helper functions."""

from .. import errors


def get(obj, path, default=None):
    """Gets the value at path of object.

    If the resolved value is undefined, the default value is returned
    in its place.

    Exampele:
    >>> obj = { 'a': [{ 'b': { 'c': 3 } }] }
    >>> get(obj, 'a.0.b.c')
    3

    Args:
        obj (dict,list): The object to query.
        path (str): The path of the property to get.
        default (any, optional): The value returned for unresolved values.

    Returns:
        any: Returns the resolved value.
    """
    path_items = path.split(".")
    value = obj
    try:
        for key in path_items:
            if isinstance(value, (list, tuple)):
                value = value[int(key)]
            else:
                value = value[key]
    except (KeyError, ValueError, TypeError):
        value = default
    return value


def get_company_name(companies_list, company):
    """Return company name from companies on companies_list.

    Args:
        companies_list (list): [description]
        company (str): company id or name

    Returns:
        str: company name or ""
    """
    company_name = ""
    for item in companies_list:
        if company == item.get("id") or company == item.get("name"):
            company_name = item.get("name")
            break
    return company_name


def match_company_name(companies_list, company_identifier=None):
    """Return company name by company_identifier or first in companies_list.

    Args:
        companies_list (list): list of companies
        company_identifier (str, optional): name or ID of the expected company.
                                            Defaults to None.

    Raises:
        errors.NotFound: if the expected company is not on the list

    Returns:
        str: company name.
    """
    if company_identifier:
        company_name = get_company_name(companies_list, company_identifier)
        if not company_name:
            raise errors.NotFound(f"Company {company_identifier!r} not found")
    else:
        company_name = get(companies_list, "0.name")
    return company_name
