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

LIMIT = 1000  # TODO: set from configure


class Dumper(yaml.SafeDumper):
    @staticmethod
    def str_presenter(dumper, data):
        if "\n" in data:  # check for multiline string
            items = [item.rstrip() for item in data.splitlines()]
            return dumper.represent_scalar(
                "tag:yaml.org,2002:str", "\n".join(items), style="|"
            )
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)


Dumper.add_representer(str, Dumper.str_presenter)


def save_edge_action(base_path, company_name, edge_action):
    name = edge_action.get("id")
    path = os.path.join(base_path, company_name, "edge_action", name)
    os.makedirs(path, exist_ok=True)

    # save action.js
    filename = os.path.join(path, "action.js")
    js_body = edge_action.get("js", "")
    with open(filename, "wb") as fileptr:
        fileptr.write(js_body.encode(encoding="utf-8"))

    # save meta.yaml
    meta = dict(
        disabled=edge_action.get("disabled", True),
        source=edge_action.get("source", ""),
        description=edge_action.get("description", ""),
        version=edge_action.get("version", 1),
    )
    filename = os.path.join(path, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
            Dumper=Dumper,
        )


def save_cloud_action(base_path, company_name, cloud_action):
    name = cloud_action.get("id")
    path = os.path.join(base_path, company_name, "cloud_action", name)
    os.makedirs(path, exist_ok=True)

    # save action.js
    filename = os.path.join(path, "action.js")
    js_body = cloud_action.get("js", "")
    with open(filename, "wb") as fileptr:
        fileptr.write(js_body.encode(encoding="utf-8"))

    # save meta.yaml
    meta = dict(
        disabled=cloud_action.get("disabled", True),
        source=cloud_action.get("source", ""),
        description=cloud_action.get("description", ""),
        version=cloud_action.get("version", 1),
    )
    filename = os.path.join(path, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
            Dumper=Dumper,
        )


def save_blueprint(
    base_path, company_name, blueprint, edge_package_index=None
):
    name = blueprint.get("id")
    path = os.path.join(base_path, company_name, "blueprint", name)
    os.makedirs(path, exist_ok=True)

    blueprint_cp_props = [
        "displayName",
        "localActions",
        "observations",
        "state",
        "version",
    ]

    meta = dict()
    for key in blueprint_cp_props:
        meta[key] = blueprint.get(key)
    filename = os.path.join(path, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
            Dumper=Dumper,
        )
    if edge_package_index:
        edge_package = edge_package_index.get(blueprint.get("edgePackage"))
        filename = os.path.join(path, "edgePackage.yaml")
        with open(filename, "wb") as fileptr:
            yaml.dump(
                edge_package,
                fileptr,
                default_flow_style=False,
                allow_unicode=True,
                encoding="utf-8",
                Dumper=Dumper,
            )


async def _fetch_edge_actions(client, base_path, companies):
    for company in companies:
        resp = await client.edge_actions(
            fields=[], company_name=company["name"], limit=LIMIT
        )
        list_action = resp.get("body")
        for action in list_action:
            company_name = match_company_name(
                companies, action.get("companyId", company)
            )
            save_edge_action(base_path, company_name, action)


async def _fetch_cloud_actions(client, base_path, companies):
    for company in companies:
        resp = await client.actions(
            fields=[], company_name=company["name"], limit=LIMIT
        )
        list_action = resp.get("body")
        for action in list_action:
            company_name = match_company_name(
                companies, action.get("companyId", company)
            )
            save_cloud_action(base_path, company_name, action)


async def _fetch_blueprints(client, base_path, companies):
    resp = await client.firmwares()
    data = resp.get("body")
    edge_package_index = dict((item["id"], item) for item in data)

    for company in companies:
        resp = await client.blueprints(
            fields=[], company_name=company["name"], limit=LIMIT
        )
        list_blueprint = resp.get("body")
        for blueprint in list_blueprint:
            company_name = match_company_name(
                companies, blueprint.get("companyId", company)
            )
            save_blueprint(
                base_path, company_name, blueprint, edge_package_index
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
        companies = list_companies
    else:
        companies = [
            item
            for item in list_companies
            if client.current_company in item.values()
        ]

    await _fetch_edge_actions(client, base_path, companies)
    await _fetch_cloud_actions(client, base_path, companies)
    await _fetch_blueprints(client, base_path, companies)


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
