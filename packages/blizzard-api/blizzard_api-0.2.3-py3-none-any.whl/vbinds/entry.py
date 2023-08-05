# =====================================
# generator=datazen
# version=1.1.1
# hash=9526b3b2cf3f63248b92b918b7a3c1bc
# =====================================

"""
vbinds - This package's command-line entry-point (boilerplate).
"""

# built-in
import argparse
import logging
import sys
from typing import List

# internal
from vbinds import VERSION, DESCRIPTION
from vbinds.app import entry, add_app_args


def main(argv: List[str] = None) -> int:
    """ Program entry-point. """

    result = 0

    # fall back on command-line arguments
    command_args = sys.argv
    if argv is not None:
        command_args = argv

    # initialize argument parsing
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--version", action="version",
                        version="%(prog)s {0}".format(VERSION))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="set to increase logging verbosity")

    add_app_args(parser)

    # parse arguments and execute the requested command
    try:
        args = parser.parse_args(command_args[1:])
        args.version = VERSION

        # initialize logging
        log_level = logging.DEBUG if args.verbose else logging.INFO
        logging.basicConfig(level=log_level,
                            format=("%(name)-36s - %(levelname)-6s - "
                                    "%(message)s"))

        # run the application
        result = entry(args)
    except SystemExit as exc:
        result = 1
        if exc.code is not None:
            result = exc.code

    return result
