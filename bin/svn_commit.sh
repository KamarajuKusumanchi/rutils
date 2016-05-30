#! /usr/bin/env zsh

do_it()
{
  echo ---------------------------------------------
  date
  echo ---------------------------------------------
  set -x
  cd ~/repo
  svn commit -m "message"
  ls
}

do_it 2>&1 | tee -a ~/logs/commit.log
