#! /usr/bin/env zsh

# The idea here is to keep track of the list of installed packages over time.
# The list is saved in ~/logs with a timestamp appended in the file name. It
# can come in handy to debug issues related to package upgrades.  For example,
# the user can run the script before and after the upgrade to figure out what
# all packages got upgraded and narrow down the package causing the issue.
#
# sample usage
# % installed_packages.sh
# stored the list of installed packages in /home/rajulocal/logs/installed_packages_list_20150606_002619.txt


LOGDIR=~/logs
mkdir -p $LOGDIR
LOGFILE=$LOGDIR/installed_packages_list_$(date +%Y%m%d_%H%M%S).txt
dpkg -l | grep ^ii > $LOGFILE;
printf "stored the list of installed packages in $LOGFILE\n";
