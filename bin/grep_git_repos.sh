#! /usr/bin/env bash

# Grep all git repos under a directory

set -x
set -e
set -u

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 base_dir <options to git grep>" >&2
    exit 1
fi

cd "$(dirname "$0")"
./git_shelf.sh "$1" grep "${@:2}"
