#! /usr/bin/env bash

# Run any script in an emulated cron environment.
#
# To generate the cron environment, add this to crontab and wait for a minute
#* * * * *   /usr/bin/env > $HOME/x/cron-env
# once the file is populated, edit crontab and disable that line.
#
# To use this script
# run_as_cron.sh /the/problematic/script --with arguments --and parameters
/usr/bin/env -i $(cat $HOME/x/cron-env) "$@"
