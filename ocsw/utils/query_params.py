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


def query_filter(filters):
    # TODO: implement this
    filters = filters or ""
    return filters


def query_params(
    sort=None,
    order=None,
    start=0,
    limit=None,
    fields=None,
    filters=None,
    refs=0,
    **_kwargs,
):
    params = dict()

    if sort:
        params["sort"] = sort
    if order in ("desc", "asc"):
        params["order"] = order

    if fields:
        params["only"] = ",".join(fields)
    if filters:
        params["filter"] = query_filter(filters)

    if start:
        params["start"] = start
    if limit:
        params["limit"] = limit
    if refs:
        params["refs"] = 1

    return params
