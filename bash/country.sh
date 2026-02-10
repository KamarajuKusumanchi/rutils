#! /usr/bin/env bash

# Background:
# This is the script version of the command
# $ grep "^37.238" /var/log/nginx/access.log | sort | awk '{print $1}' | xargs -I {} sh -c 'echo -n "{}, "; geoiplookup {} | awk -F": " "{print \$2}"'
# ...
# 37.238.100.8, IQ, Iraq
# 37.238.101.164, IQ, Iraq
# 37.238.101.42, IQ, Iraq
# ...

# Since we are writing a script, it is better to use while loop than xargs
# Read IP addresses from stdin, sort them, and get their location
sort | awk '{print $1}' | uniq | while read -r ip; do
    # Get GeoIP info and format output
    location=$(geoiplookup "$ip" | awk -F": " '{print $2}')
    echo "$ip, $location"
done
