#! /usr/bin/env python3

# list all dependencies, reverse dependencies of a package

import subprocess
# import sys
import argparse

parser = argparse.ArgumentParser(
    description='List all dependencies of a package')
parser.add_argument(
    "pkg", action='store',
    help='package name')
parser.add_argument(
    "-r", "--reverse_dep", action="store_true",
    default=False)
parser.add_argument(
    "--debug", action="store_true",
    default=False)
args = parser.parse_args()

# pkg=sys.argv[1]
pkg = args.pkg
reverse_dep = args.reverse_dep
debug = args.debug

if not reverse_dep:
    cmd = ["/usr/bin/apt-rdepends", "--state-show=Installed",
           "--state-follow=Installed", pkg]
else:
    cmd = ["/usr/bin/apt-rdepends", "--state-show=Installed",
           "--state-follow=Installed", "-r", pkg]

# cmd = ["ls", "-1"]
# cmd = "ls -1"
if (debug):
    print(cmd)
output = subprocess.check_output(cmd).decode()
print(output)
