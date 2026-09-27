#!/usr/bin/env bash
#
# pip_wheel_deps.sh
#
# Lists the declared dependencies (Requires-Dist) of a PyPI package,
# based on the wheel that `pip` would actually select for the Python
# interpreter and platform currently running this script.
#
# Usage:
#   ./pip_wheel_deps.sh <package_name>
#
# Example:
#   ./pip_wheel_deps.sh curl_cffi
#
# Limitations:
#   - Only works for packages that publish a wheel (.whl). If a package
#     ships only a source distribution (.tar.gz), the *.whl glob below
#     matches nothing and the script fails.
#   - The version selected is "the latest version compatible with THIS
#     machine's Python/OS/architecture" — not necessarily the overall
#     latest version of the package. If the newest release dropped
#     support for this Python version or doesn't publish a wheel for
#     this platform, pip silently falls back to an older version, and
#     that fallback version's dependencies are what gets printed.
#   - Requires network access and an internet-connected `pip`.
#   - Reads metadata from an actual built artifact (the wheel), so it
#     reflects what would really be installed, not just what the
#     author declared in their build config.

set -euo pipefail

# Require exactly one argument: the package name.
# ${1:?message} exits with an error and prints "message" if $1 is unset/empty.
PKG="${1:?Usage: $0 <package_name>}"

# Use a per-package temp directory so repeated runs for different
# packages don't collide with each other.
DIR="/tmp/${PKG}_check"

# Wipe and recreate the directory so we always start clean.
# This guarantees the *.whl glob below matches exactly one file.
rm -rf "$DIR"
mkdir -p "$DIR"

# Download only the package itself, not its dependencies (--no-deps),
# so the directory ends up with just one wheel file. -q keeps it quiet.
pip download "$PKG" --no-deps -d "$DIR" -q

# Grab the single wheel file that was just downloaded.
WHL=$(ls "$DIR"/*.whl)

# Show exactly which file we're reading from, since the version
# selected depends on this machine's Python/platform (see limitations
# above) and may not be the newest version that exists on PyPI.
echo "Package: $PKG"
echo "Wheel:   $(basename "$WHL")"
echo "---"

# Wheels are zip files. The dependency list lives inside a file named
# <pkg>-<version>.dist-info/METADATA. We use a glob ("*/METADATA")
# instead of hardcoding the versioned folder name, since we don't want
# to parse that out separately. unzip -p prints just that one member
# to stdout, which we then filter for the Requires-Dist lines.
unzip -p "$WHL" "*/METADATA" | grep -i "Requires-Dist"
