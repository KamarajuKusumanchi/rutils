#! /usr/bin/env bash

# Run git status on a bunch of directories

dirs=(
    "$HOME/work/github"
    "$HOME/work/gitlab"
    )
for i in ${dirs[@]}
do
    for project in `ls $i`
    do
        abs_path=$i/$project
        echo $abs_path

	# The -C is supported in git >= 1.8.5
	# -s gives the output in short-format
        git -C $abs_path status -s
    done
done
