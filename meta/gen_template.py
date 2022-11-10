#!/usr/bin/env python3
"""
Takes the `version.py` file from the Godot repository, this
repo's README.md, and the two template files in this directory, 
and generates an AppStream metainfo
and `.desktop` file that we can use for the Snap.

Due to the files needed, this should be run `after` in Snapcraft.
"""

# This is the `version.py` file from Godot, it doesn't exist here but will
# in the Snapcraft environment
import version  # type: ignore

from string import Template
from typing import Dict
from pathlib import Path
import argparse
from xml.sax import saxutils

SUMMARY = "A free, open source game engine."
# Careful if you change this, it also needs to be changed in the
# `snapcraft.yaml` if you do
ID = "org.godotengine.Godot"


def read_description(readme: Path) -> str:
    with open(readme, 'r') as f:
        return f.read()


def longname() -> str:
    """
    Makes the full name of the engine so it matches its
    stability. Godot 3 and Godot 4 should be labelled as
    such as applications, and unstable versions should also
    be marked.

    In addition, point releases are only tagged if the version
    is unstable. I.E. "Godot 3.2" is only "Godot 3.2" if it's a
    beta release, otherwise it's just "Godot 3" (i.e. the current
    stable 3.x release).

    Here are some examples:
        Godot 4.0.0 stable -> "Godot Engine 4"
        Godot 4.0.0 beta -> "Godot Engine 4 (beta)"
        Godot 3.4.0 stable -> "Godot Engine 3"
        Godot 3.5.0 beta -> "Godot Engine 3.5.0 (beta)"
    """
    name = version.name + f' {version.major}'
    if version.status != 'stable':
        if version.minor != 0 or version.patch != 0:
            name += f'.{version.minor}.{version.patch}'
        name += f' ({version.status})'
    return name


def gen_file(template_name: Path, values: Dict[str, str]):
    """
    Opens the file given by `template_name` and uses basic, 
    unescaped string substitution to dump the values from the
    dictionary `values`.
    """
    # Output the final file in the local directory
    outname = Path(template_name.name.replace('template', ID))
    with open(outname, 'w') as of, open(template_name, 'r') as template:
        of.write(
            Template(template.read()).safe_substitute(**values)
        )


def existing_file(arg: str) -> Path:
    """
    A wrapper function for argparse to convert a given path to
    a `pathlib.Path` provided:
        1. It is a valid file path
        2. The file actually exists
    Otherwise an argparse error will be raised and the user will be notified.
    """
    path = Path(arg)

    if not path.is_file():
        raise argparse.ArgumentError("argument must be a valid file name")

    if not path.exists():
        raise argparse.ArgumentError("file specified by argument must exist")

    return path


def parse_args():
    """
    Let us set values via CLI so we don't always have to edit this file
    to change stuff
    """
    parser = argparse.ArgumentParser(
        prog="Metainfo Template Filler",
        description="Fills a .desktop file and a metainfo.xml file \
            with some basic data for Snapcraft"
    )

    parser.add_argument('--desktop-template',
                        type=existing_file, default=Path('template.desktop'))
    parser.add_argument('--metainfo-template',
                        type=existing_file, default=Path('template.metainfo.xml'))
    parser.add_argument('--readme', type=existing_file, required=True)
    parser.add_argument('--summary', type=str, default=SUMMARY)
    parser.add_argument('--id', type=str, default=ID)

    return parser.parse_args()


def main():
    args = parse_args()

    values = {
        'summary': args.summary,
        'longname': longname(),
        'description': saxutils.escape(read_description(args.readme)),
        'version': f'{version.major}.{version.minor}.{version.patch}',
        'grade': f'{version.status}'
    }

    gen_file(args.desktop_template, values)
    gen_file(args.metainfo_template, values)


if __name__ == '__main__':
    main()
