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

"""Manage Cloud."""

import os

import yaml

from ..utils.format_pretty_json import pprintj
from ..utils.helpers import match_company_name


def save_edge_actions(base_path, company_name, edge_action):
    name = edge_action.get("id")
    path = os.path.join(base_path, company_name, "edge_action", name)
    os.makedirs(path, exist_ok=True)

    # save action.js
    filename = os.path.join(path, "action.js")
    js = edge_action.get("js", "")
    with open(filename, "wb") as fileptr:
        fileptr.write(js.encode(encoding="utf-8"))

    # save meta.yaml
    meta = dict(
        disabled=edge_action.get("disabled", True),
        source=edge_action.get("source", ""),
        description=edge_action.get("description", ""),
        version=edge_action.get("version", 1),
    )
    filename = os.path.join(path, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.safe_dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
        )


def save_cloud_action(base_path, company_name, cloud_action):
    name = cloud_action.get("id")
    path = os.path.join(base_path, company_name, "cloud_action", name)
    os.makedirs(path, exist_ok=True)

    # save action.js
    filename = os.path.join(path, "action.js")
    js = cloud_action.get("js", "")
    with open(filename, "wb") as fileptr:
        fileptr.write(js.encode(encoding="utf-8"))

    # save meta.yaml
    meta = dict(
        disabled=cloud_action.get("disabled", True),
        source=cloud_action.get("source", ""),
        description=cloud_action.get("description", ""),
        version=cloud_action.get("version", 1),
    )
    filename = os.path.join(path, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.safe_dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
        )


async def cmd_cloud_fetch(
    client, config_path, config_filename, get_all=False, **_kwargs
):
    """Download objects and refs from cloud."""
    workdir = os.path.dirname(os.path.join(config_path, config_filename))
    base_path = os.path.join(workdir, "company")

    # get all companies
    resp = await client.companies(field=["id", "name"])
    list_companies = resp.get("body")

    companies = [client.current_company]
    if get_all:
        companies = [item["name"] for item in list_companies]

    for company in companies:
        resp = await client.edge_actions(
            fields=[], company_name=company, limit=1000
        )
        list_action = resp.get("body")
        for action in list_action:
            company_name = match_company_name(
                list_companies, action.get("companyId", company)
            )
            save_edge_actions(base_path, company_name, action)

    for company in companies:
        resp = await client.actions(
            fields=[], company_name=company, limit=2000
        )
        list_action = resp.get("body")
        pprintj(list_action)
        for action in list_action:
            company_name = match_company_name(
                list_companies, action.get("companyId", company)
            )
            save_cloud_action(base_path, company_name, action)


def init_cli(subparsers):
    prompt = "Manage Cloud"
    parser = subparsers.add_parser("cloud", help=prompt, description=prompt)
    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    sub = parser.add_subparsers(metavar="COMMAND")

    # FETCH
    parser_fetch = sub.add_parser(
        "fetch", help="download objects and refs from cloud",
    )
    parser_fetch.set_defaults(func=cmd_cloud_fetch)
    parser_fetch.add_argument(
        "--all",
        action="store_true",
        dest="get_all",
        help="from all companies",
    )

    # TODO: implement this
    # # PULL
    # parser_pull = sub.add_parser(
    #     "pull", help="fetch and integrate with local package",
    # )
    # parser_pull.set_defaults(func=cmd_cloud_pull)

    # # PUSH
    # parser_push = sub.add_parser(
    #     "push", help="update remote refs along with associated objects",
    # )
    # parser_push.set_defaults(func=cmd_cloud_push)
