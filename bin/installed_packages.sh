#! /usr/bin/env zsh

# sample usage
# % ~/bin/installed_packages.sh
# stored the list of installed packages in /home/rajulocal/logs/installed_packages_list_20150606_002619.txt


LOGDIR=~/logs
LOGFILE=$LOGDIR/installed_packages_list_$(date +%Y%m%d_%H%M%S).txt
dpkg -l | grep ^ii > $LOGFILE;
printf "stored the list of installed packages in $LOGFILE\n";
