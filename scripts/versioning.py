#! /usr/bin/env python3
"""
A script to change version numbers for multiple paths.

./versioning.py -ov 1.0.4 -nv 1.0.5
"""

from pathlib import Path
import argparse
import datetime


def update_string(file_path, search_string, replace_string):
    """
    Updates the specified string in a file.

    Parameters
    ----------
    file_path: Path
        Path object representing the file to update.
    search_string: str
        The string to search for in the file.
    replace_string: str
        The string to replace with the new value.
    """
    current_content = file_path.read_text()
    new_content = current_content.replace(search_string, replace_string)
    if current_content != new_content:
        file_path.write_text(new_content)
        print(f"Updated string in: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        prog="versioning.py",
        description="Replace version or release string"
    )
    parser.add_argument(
        "-ov",
        "--old_version",
        type=str,
        required=True,
        help="The old version string in form x.y.z",
    )
    parser.add_argument(
        "-nv",
        "--new_version",
        type=str,
        required=True,
        help="The new version string in form x.y.z",
    )
    args = parser.parse_args()
    version_data = [
        (
            Path("/home/gilles/documents/repositories/dawgdad/pyproject.toml"),
            f"version = \"{args.old_version}\"",
            f"version = \"{args.new_version}\""
        ),
        (
            Path("/home/gilles/documents/repositories/dawgdad/README.md"),
            f"version = {{{args.old_version}}}",
            f"version = {{{args.new_version}}}"
        ),
        (
            Path("/home/gilles/documents/repositories/dawgdad/docs/requirements.txt"),
            f"dawgdad=={args.old_version}",
            f"dawgdad=={args.new_version}"
        ),
        (
            Path("/home/gilles/documents/repositories/dawgdad/docs/source/conf.py"),
            f"release = '{args.old_version}'",
            f"release = '{args.new_version}'"
        ),
        (
            Path("/home/gilles/documents/repositories/virtual/requirements.txt"),
            f"dawgdad=={args.old_version}",
            f"dawgdad=={args.new_version}"
        ),
    ]
    for file_path, search_string, replace_string in version_data:
        update_string(
            file_path=file_path,
            search_string=search_string,
            replace_string=replace_string
        )


if __name__ == "__main__":
    main()
