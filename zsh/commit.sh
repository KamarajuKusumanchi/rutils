#! /bin/env zsh

do_it()
{
  echo ---------------------------------------------
  date
  echo ---------------------------------------------
  set -x
  cd ~/dev
  ls
}

do_it 2>&1 | tee -a ~/x/junk2.log
