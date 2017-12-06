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

        # In the git status command below:
        # -s gives the output in short-format
        # -b shows the branch and tracking information
        # -C is used to specify the project directory.
        # The -C option is supported in git >= 1.8.5
        #
        # I am not interested if the output of "git status -sb" is just
        # ## master...origin/master
        # But want to capture things like
        # ## master...origin/master [ahead 1]
        # to show if the repository is ahead of 'origin/master'.
        output=$(git -C $abs_path status -sb | grep -v "^## master\.\.\.origin/master$")

        # Simply printing $output will not show any colors. So rerun the git
        # command, which will give colored output.
        if [ -n "$output" ]; then
            echo $abs_path
            git -C $abs_path status -sb
        fi
    done
done
