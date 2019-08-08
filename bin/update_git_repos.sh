#! /usr/bin/env bash

# Update all git repos under a directory

# Todo:- By default, only the top level directories are updated. Afterwards
# generalize it?
#
# Todo:- By default, the action is hardcoded (ex:- "git up"). But sometimes we
# might want to apply a different action (ex:- "git grep -i foo"). How to
# generalize for this?

# set -x
set -e
set -u
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 base_dir" >&2
    exit 1
fi

# The base directory can be specified either as a relative or absolute
# directory. Handle both cases.
base_dir=$(realpath $1)

cd "$base_dir"
find . -maxdepth 2 -name .git -type d -prune | while read d; do
    # Remove "./" from the beginning and "/.git" from the end
    repo_dir=${d:2:-5}
    echo "$repo_dir"
    cd "$repo_dir"
    # call my custom git-up script to update the repository
    git up
    cd "$base_dir"
done
