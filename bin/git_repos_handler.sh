#! /usr/bin/env bash

# Apply a git operation on all the git repos under a directory.

# Todo:- By default, only the top level directories are searched. Afterwards
# generalize it?

# set -x

# Do not set the -e option here. Instead, let the calling function set it if
# necessary. This is so because, when doing a git operation, we might get a
# nonzero return code but still want to continue looping over other repos.
# For example, git grep PATTERN returns an exit code of 1 if the PATTERN does
# not exist in the repo. In that case, we still want to continue searching
# over other repos.

set -u

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 base_dir <options to git command>" >&2
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
    git "${@:2}"
    )
done