import argparse


class KeyValueAction(argparse.Action):
    """Action argparse.

    argparse action to split an argument into KEY=VALUE form
    on the first = and append to a dictionary.
    """

    def _process_value(self, value):
        if "=" in value:
            return value.split("=", 1)
        raise argparse.ArgumentError(
            self, f"could not parse argument {value:r} as k=v format"
        )

    def __call__(self, parser, args, values, option_string=None):
        if values is None:
            return
        if not isinstance(values, (list, tuple)):
            values = [values]
        dest = getattr(args, self.dest) or {}
        dest.update(dict(self._process_value(value) for value in values))
        setattr(args, self.dest, dest)


class HelpAction(argparse.Action):
    """Retrieve subparsers from parser."""

    def __init__(
        self,
        option_strings,
        dest=argparse.SUPPRESS,
        default=argparse.SUPPRESS,
        help=None,  # pylint: disable=redefined-builtin
    ):

        super(HelpAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )

    def __call__(self, parser, namespace, values, option_string=None):
        subparsers_actions = [
            action
            for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        ]

        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                print(f"## Command: {choice}\n")
                print(subparser.format_help())
        parser.exit()
