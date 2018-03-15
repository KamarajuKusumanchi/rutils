#! /bin/env bash

# Print svn log over the last 24 hours.

set -x
now=`date +%s`
yesterday=$(( now - 86400 ))
d1=`date --date @$yesterday -Iseconds`
d2=`date --date @$now -Iseconds`
svn log -r {$d1}:{$d2}
