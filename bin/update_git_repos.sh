#! /usr/bin/env bash

# Update all git repos under a directory

set -x
set -e
set -u
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 base_dir" >&2
    exit 1
fi

cd "$(dirname "$0")"
./git_shelf.sh "$1" up
