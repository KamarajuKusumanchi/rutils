#! /usr/bin/env bash

# Script to generate a list of libwrap-enabled applications

# find all executables and test for libwrap
find /bin /usr/bin /sbin /usr/sbin -type f -perm -1 | \
while read filename; do
    haslib=$(ldd "$filename" | grep libwrap.so);
    if [ "$haslib" != "" ]; then echo "$filename"; fi;
done

# Credits:
# The initial version of this script is copied from the book
# Ubuntu - Powerful Hacks and Customizations by Dr. Neal Krawetz
