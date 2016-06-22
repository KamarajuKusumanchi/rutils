#! /usr/bin/env zsh

do_it()
{
  echo ---------------------------------------------
  date
  echo ---------------------------------------------
  set -x
  cd ~/work/gitlab/rutils
  git commit -m "Initial commit of bin/popsort.py"

  # This calls git-up which is a custom script.
  # It is part of this package.
  git up
  git push -u origin master
}

do_it 2>&1 | tee -a ~/logs/commit.log
