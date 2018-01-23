#! /usr/bin/env bash
# Dump some of the recent revisions of a file tracked by svn.
set -e
set -u
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <file_name> <number_of_revisions>" >&2
	exit 1
fi
fname="$1"
nrev="$2"
svn log $fname --limit $nrev | grep -E -e 'r[[:digit:]]+' -o | {
    while read cur_rev
	do
	    outfile=${fname}_${cur_rev}
	    svn cat -${cur_rev} $fname > $outfile
		echo wrote $outfile
	done
}
