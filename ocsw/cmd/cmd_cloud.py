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

"""WIP Manage Cloud."""

import asyncio
import os
import shutil

import yaml

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
    name = "{description}__{id}".format(**edge_action)
    path = os.path.join(base_path, company_name, "edge_action", name)
    export_action(path, edge_action)


def save_cloud_action(base_path, company_name, cloud_action):
    name = "{description}__{id}".format(**cloud_action)
    path = os.path.join(base_path, company_name, "cloud_action", name)
    export_action(path, cloud_action)


def save_blueprint(
    base_path, company_name, blueprint, edge_package_index=None
):
    name = "{displayName}__{id}".format(**blueprint)
    path = os.path.join(base_path, company_name, "blueprint", name)
    os.makedirs(path, exist_ok=True)

    blueprint_cp_props = [
        "displayName",
        "edgePackage",
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
    os.makedirs(base_path, exist_ok=True)
    shutil.rmtree(base_path, ignore_errors=False, onerror=None)

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


def get_template_filename4blueprint(items):
    values = [item["displayName"] for item in items]
    uniq_description = len(set(values)) == len(values)
    return "{displayName}" if uniq_description else "{displayName}__{id}"


def get_template_filename4actions(items):
    values = [item["description"] for item in items]
    uniq_description = len(set(values)) == len(values)
    return "{description}" if uniq_description else "{description}__{id}"


def export_action(outpath, action):
    os.makedirs(outpath, exist_ok=True)

    # save action.js
    filename = os.path.join(outpath, "action.js")
    js_body = action.get("js", "")
    with open(filename, "wb") as fileptr:
        fileptr.write(js_body.encode(encoding="utf-8"))

    # save meta.yaml
    meta = dict(
        disabled=action.get("disabled", True),
        source=action.get("source", ""),
        description=action.get("description", ""),
        version=action.get("version", 1),
    )
    filename = os.path.join(outpath, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
            Dumper=Dumper,
        )


def export_blueprint(outpath, blueprint):
    os.makedirs(outpath, exist_ok=True)

    meta = blueprint
    filename = os.path.join(outpath, "meta.yaml")
    with open(filename, "wb") as fileptr:
        yaml.dump(
            meta,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
            Dumper=Dumper,
        )


def export_edge_package(outpath, edge_package):
    os.makedirs(outpath, exist_ok=True)
    filename = os.path.join(outpath, "edgePackage.yaml")
    with open(filename, "wb") as fileptr:
        yaml.dump(
            edge_package,
            fileptr,
            default_flow_style=False,
            allow_unicode=True,
            encoding="utf-8",
            Dumper=Dumper,
        )


async def get_edge_package_index(client, company_name=None):
    resp = await client.firmwares(company_name=company_name)
    data = resp.get("body")
    return dict((item["id"], item) for item in data)


async def get_local_actions4blueprint(client, company_name, blueprint):
    futures = [
        client.inspect_edge_action(
            action_id,
            version_number=action_v["version"],
            company_name=company_name,
        )
        for action_id, action_v in blueprint.get("localActions", {}).items()
    ]
    return [resp.get("body") for resp in await asyncio.gather(*futures)]


async def _export_blueprints(client, company_name=None, outpath="."):
    resp = await client.blueprints(company_name=company_name, limit=LIMIT)
    edge_package_index = await get_edge_package_index(
        client, company_name=company_name
    )

    list_blueprint = resp.get("body")
    template_filename4blueprint = get_template_filename4blueprint(
        list_blueprint
    )
    for blueprint in list_blueprint:
        blueprint_name = template_filename4blueprint.format(**blueprint)
        blueprint_path = os.path.join(outpath, blueprint_name)
        export_blueprint(blueprint_path, blueprint)
        edge_package_id = blueprint.get("edgePackage")
        if edge_package_id:
            edge_package = edge_package_index.get(edge_package_id)
            export_edge_package(blueprint_path, edge_package)

        actions = await get_local_actions4blueprint(
            client, company_name, blueprint
        )

        template_filename4actions = get_template_filename4actions(actions)
        for action in actions:
            actions_path = os.path.join(blueprint_path, "localActions")
            action_name = template_filename4actions.format(**action)
            action_path = os.path.join(actions_path, action_name)
            export_action(action_path, action)


async def cmd_cloud_export(client, config_path, get_all=False, **_kwargs):
    """Download objects and refs from cloud."""
    prj_path = os.path.dirname(os.path.join(config_path, ".."))

    # get all companies
    resp = await client.companies(field=["id", "name"])
    list_companies = resp.get("body")

    if get_all:
        companies = list_companies
    else:
        companies = [
            item
            for item in list_companies
            if client.current_company in item.values()
        ]
    companies_name = [uid["name"] for uid in companies]

    for company_name in companies_name:
        base_path = os.path.join(prj_path, "companies", company_name)
        outpath = os.path.join(base_path, "blueprints")
        os.makedirs(outpath, exist_ok=True)
        shutil.rmtree(outpath, ignore_errors=False, onerror=None)
        await _export_blueprints(
            client, company_name=company_name, outpath=outpath
        )


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

    # FETCH
    parser_export = sub.add_parser(
        "export", help="download objects and refs from cloud",
    )
    parser_export.set_defaults(func=cmd_cloud_export)
    parser_export.add_argument(
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
