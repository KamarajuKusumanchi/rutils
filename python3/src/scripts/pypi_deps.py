#!/usr/bin/env python3
"""
pypi_deps.py

Lists the declared dependencies (Requires-Dist) for the newest release
of a PyPI package, as reported by PyPI's JSON API — the same "latest
version" number shown on the package's PyPI project page.

Usage:
    ./pypi_deps.py <package_name>

Example:
    ./pypi_deps.py curl_cffi

Limitations:
    - Reports the version as declared in PyPI's index metadata, which
      is the author's build-time declaration, not extracted from an
      actual installable artifact. For well-maintained packages these
      always match, but metadata can in principle drift from what's
      actually shipped in a given wheel.
    - Does not check whether this "latest" version is installable on
      any particular machine — it may have no wheel for your Python
      version or OS at all, or a wheel could exist only for other
      platforms. It answers "what does the latest release declare",
      not "what would pip actually install for me".
    - Dependencies (`requires_dist`) can include environment markers
      (e.g. extras, or `; python_version < "3.8"`) which are printed
      as-is rather than evaluated against a specific environment.
    - Requires network access, and the `requests` library installed
      (pip install requests).
"""

import sys

import requests


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <package_name>")

    package = sys.argv[1]
    url = f"https://pypi.org/pypi/{package}/json"

    response = requests.get(url)
    if response.status_code != 200:
        sys.exit(f"Error: could not fetch metadata for '{package}' "
                  f"(HTTP {response.status_code})")

    data = response.json()
    info = data["info"]
    version = info["version"]
    dependencies = info.get("requires_dist") or []

    print(f"Package: {package}")
    print(f"Latest version (per PyPI): {version}")
    print("---")

    if not dependencies:
        print("(no declared dependencies)")
    else:
        for dep in dependencies:
            print(dep)


if __name__ == "__main__":
    main()
