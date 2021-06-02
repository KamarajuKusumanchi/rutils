#! /usr/bin/env bash

# cd into a directory
# unzip all zip files and then remove the zip files.

set -e -u
set -x

if [ "$#" -ne 1 ]; then
  echo "unzip all zip files in dir_name and then remove the zip files"
  echo "Usage: $0 dir_name" >&2
  exit 1
fi

dir_name="$1"
cd "$dir_name"
unzip "*.zip" && rm -f *.zip
