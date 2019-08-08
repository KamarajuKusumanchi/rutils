#! /usr/bin/env bash

# Grep all git repos under a directory

# Todo:- By default, only the top level directories are searched. Afterwards
# generalize it?
#
# Todo:- By default, the action is hardcoded (ex:- "git grep"). But sometimes we
# might want to apply a slightly different action (ex:- "git up"). How
# to generalize for this?

# set -x

# If you set -e, then code will stop executing if there is a repo without any
# hits, since in that case, 'git grep' exits with a return code of 1.
# set -e

set -u

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 base_dir <option> <keyword>" >&2
    exit 1
fi

# The base directory can be specified either as a relative or absolute
# directory. Handle both cases.
base_dir=$(realpath $1)

cd "$base_dir"
find . -maxdepth 2 -name .git -type d -prune | while read d; do
    # Put everything in a subshell, so we do not have to reset the directory
    # back once the for loop finishes.
    (
    # We need the directory that holds the .git directory.
    repo_dir="$(dirname "$d")"

    # Print the repo name in green
    green=$(tput setaf 2)
    reset=$(tput sgr0)
    # Remove the leading "./" from the repo_dir when printing it.
    repo_name=${repo_dir:2}
    echo "$green$repo_name$reset"

    cd "$repo_dir"
    git grep -n "${@:2}"
    )
done
