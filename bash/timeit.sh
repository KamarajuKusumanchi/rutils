#!/bin/bash

# To run a command
# $0 command
# To time the command
# $0 -v command

# other uses:
# provides a template code on using the getopts to parse arguments.

# Initial version is from https://eklitzke.org/bash-$%2A-and-$@

SHOWTIMES=0
OPTIND=1
while getopts "h?v" opt; do
    case "$opt" in
        h|\?)
            echo "usage: $0 [-v]"
            exit 0
            ;;
        v)
            SHOWTIMES=1
            ;;
    esac
done
shift $((OPTIND - 1))

# N.B. must use "$@" here, NOT $*
if [ "$SHOWTIMES" -eq 1 ]; then
    time "$@"
else
    "$@"
fi
