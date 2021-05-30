#! /usr/bin/env bash

# list of packages that apt-get wants to upgrade.
# Sample usage:
# $script > ~/x/to_upgrade_`date +'%Y%m%d'`.txt
#
# Sample use case:
# $script | popsort.py > ~/x/to_upgrade_`date +'%Y%m%d_%H%M%S'`.txt
sudo apt-get -s upgrade | awk '$1 ~ /Inst/ { print $2; }'

