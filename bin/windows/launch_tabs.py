#!/usr/bin/env python3
"""launch_tabs.py — open Windows Terminal tabs in a set of directories.

Usage:
  launch_tabs.py                  -> uses config file, or hardcoded DEFAULT_DIRS
                                      if no config file
  launch_tabs.py dir3 dir4 ...    -> ignores config file and DEFAULT_DIRS, uses
                                      the given dirs instead
  launch_tabs.py --list           -> print the resolved directory list and exit
  launch_tabs.py --dry-run        -> print the wt command that would run, but
                                      don't execute it

Precedence: command line args > config file > hardcoded DEFAULT_DIRS below.

Config file location: $XDG_CONFIG_HOME/launch_tabs/dirs.conf (defaults to
~/.config/launch_tabs/dirs.conf if XDG_CONFIG_HOME is unset). One directory
per line. Blank lines and lines starting with '#' are ignored. If the config
file exists but has no active (non-comment, non-blank) lines, that's treated
the same as no config file — falls back to DEFAULT_DIRS.

Any directory that doesn't exist (from any source) is skipped with a
warning rather than being passed to wt.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---- hardcoded default directories (fallback if no config file and no CLI args) ----
DEFAULT_DIRS = [
    os.environ.get("learning", ""),
    os.environ.get("software", ""),
    (Path.home() / "x").as_posix(),
]


def config_file_path() -> Path:
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    return config_home / "launch_tabs" / "dirs.conf"


def read_config_dirs(path: Path) -> list[str]:
    dirs = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        dirs.append(line)
    return dirs


def find_wt() -> str:
    for candidate in ("wt.exe", "wt"):
        if shutil.which(candidate):
            return candidate
    print("Error: 'wt' / 'wt.exe' not found on PATH.", file=sys.stderr)
    sys.exit(1)


def filter_existing(dirs: list[str]) -> list[str]:
    valid = []
    for d in dirs:
        if d and Path(d).is_dir():
            valid.append(d)
        else:
            print(f"Warning: '{d}' does not exist or is not a directory — skipping.", file=sys.stderr)
    return valid


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open Windows Terminal tabs in a set of directories.",
        epilog="Precedence: command line dirs > config file > hardcoded DEFAULT_DIRS.",
    )
    parser.add_argument(
        "dirs",
        nargs="*",
        metavar="DIR",
        help="directories to open (overrides config file and DEFAULT_DIRS)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print the resolved, filtered directory list and exit (doesn't launch wt)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the wt command that would run, but don't execute it",
    )
    return parser.parse_args()


def resolve_dirs(cli_dirs: list[str]) -> list[str]:
    if cli_dirs:
        return cli_dirs

    config_path = config_file_path()
    if config_path.is_file():
        dirs = read_config_dirs(config_path)
        if dirs:
            return dirs
        # config file exists but has no active lines (e.g. all commented
        # out) -> treat the same as "no config file"

    return DEFAULT_DIRS


def main() -> None:
    args = parse_args()

    dirs = resolve_dirs(args.dirs)
    if not dirs:
        print("No directories to open.", file=sys.stderr)
        sys.exit(1)

    dirs = filter_existing(dirs)
    if not dirs:
        print("No valid directories to open.", file=sys.stderr)
        sys.exit(1)

    if args.list:
        for d in dirs:
            print(d)
        return

    wt = find_wt()

    # First pane: wt -d dir1
    # Each subsequent: ; new-tab -d dirN
    wt_args = [wt, "-d", dirs[0]]
    for d in dirs[1:]:
        wt_args += [";", "new-tab", "-d", d]

    if args.dry_run:
        print(" ".join(wt_args))
        return

    subprocess.run(wt_args, check=True)


if __name__ == "__main__":
    main()
