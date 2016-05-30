#! /usr/bin/env zsh

do_it()
{
  echo ---------------------------------------------
  date
  echo ---------------------------------------------
  set -x
  cd ~/work/gitlab/rutils
  git commit -m "Initial commit of bin/git-up"
  git push -u origin master
}

do_it 2>&1 | tee -a ~/logs/commit.log
