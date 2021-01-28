#! /usr/bin/env bash

# Script to run black on selected text
# Adapted from
# https://godatadriven.com/blog/partial-python-code-formatting-with-black-pycharm/
# His script is a bit complex and the sed commands are Mac specific.
# I simplified the script and made it work with GNU sed.
# Tested it on Windows 10 + git bash + GNU sed 4.7

# Sample run:
# black_on_selection.sh black foo.py 52 54

set -eux

black=$1
input_file=$2
start_line=$3
end_line=$4

# Read selected lines and write to tmpfile
tmpfile=$(mktemp)
# Note:
# * $(($end_line+1)) q    will make sed quit when it encounters $end_line+1
# This matters if $input_file has lots of lines.
# * -b will preserve the line endings
sed -b -n "$start_line,$end_line p; $(($end_line+1)) q" $input_file > $tmpfile

# format the selection with black
$black $tmpfile

# Replace the corresponding lines in the original and create a backup.
sed -b "-i_asof_`date +%Y%m%d_%H%M%S -r $input_file`" \
    -e "$start_line e cat $tmpfile" \
    -e "$start_line,$end_line d" \
    $input_file
