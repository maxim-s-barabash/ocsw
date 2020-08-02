# !/usr/bin/env python
"""Command line interface."""

import argparse
import logging
import sys

from . import constants, errors
from .cmd import (
    cmd_blueprint,
    cmd_cloud,
    cmd_cloud_action,
    cmd_company,
    cmd_device,
    cmd_edge_action,
    cmd_firmware,
    cmd_group,
    cmd_identity,
    cmd_login,
    cmd_logout,
    cmd_release,
    cmd_stream,
    cmd_user,
)
from .sync2async import run
from .utils.argparse_action import HelpAction
from .utils.config import find_config_path

logging.basicConfig()

LOG = logging.getLogger("cli")


def main():
    parser = argparse.ArgumentParser(
        description="Manage and monitor your devices"
    )
    parser.add_argument(
        "-H", action=HelpAction, help="show help from all command"
    )
    parser.set_defaults(config_filename=constants.DEFAULT_CONFIG)
    parser.add_argument(
        "-C",
        metavar="PATH",
        dest="config_path",
        default=find_config_path(constants.DEFAULT_CONFIG, "."),
        help='location of configuration path (default "%(default)s")',
    )
    parser.add_argument(
        "-D", "--debug", action="store_true", help="enable debug output"
    )
    parser.add_argument(
        "-v", "--version", action="version", version=constants.VERSION
    )
    parser.add_argument(
        "--show-secrets",
        action="store_true",
        help="decrypt secrets and displays plain text",
    )

    parser.set_defaults(func=lambda **_kwargs: parser.print_help())
    subparsers = parser.add_subparsers(title="commands", metavar="")

    cmd_blueprint.init_cli(subparsers)
    cmd_cloud.init_cli(subparsers)
    cmd_cloud_action.init_cli(subparsers)
    cmd_company.init_cli(subparsers)
    cmd_device.init_cli(subparsers)
    cmd_edge_action.init_cli(subparsers)
    cmd_firmware.init_cli(subparsers)
    cmd_group.init_cli(subparsers)
    cmd_stream.init_cli(subparsers)
    cmd_user.init_cli(subparsers)

    cmd_identity.init_cli(subparsers)
    cmd_login.init_cli(subparsers)
    cmd_logout.init_cli(subparsers)
    cmd_release.init_cli(subparsers)

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)

    try:
        run(**vars(args))
    except KeyboardInterrupt:
        pass
    except errors.Error as ex:
        print(ex.message, file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        LOG.exception(ex)
        sys.exit(1)


if __name__ == "__main__":
    main()
