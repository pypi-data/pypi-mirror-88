
"""
vbinds - This package's command-line entry-point application.
"""

# built-in
import argparse
import os

# internal
from vbinds.classes.icon_cache import IconCache
from vbinds.classes.engine import engine_from_output_root
from vbinds.classes.playable_class import get_classes


def entry(args: argparse.Namespace) -> int:
    """ Execute the requested task. """

    args.out_dir = os.path.abspath(args.out_dir)

    # initialize an icon cache and query engine
    icon_cache = IconCache(os.path.join(args.out_dir, "icons"))
    engine = engine_from_output_root(args.out_dir)

    icon_cache.get("spell_frost_frostshock")
    icon_cache.get("spell_nature_lightning")

    classes = get_classes(engine)
    for class_data in classes:
        print(class_data)
        print(class_data.roles())

    engine.save()

    return 0


def add_app_args(parser: argparse.ArgumentParser) -> None:
    """ Add application-specific arguments to the command-line parser. """

    parser.add_argument("-o", "--out-dir", default=os.getcwd(),
                        help="root directory for program outputs")
