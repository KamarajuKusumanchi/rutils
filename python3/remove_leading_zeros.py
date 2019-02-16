#! /usr/bin/env python3

# The idea here is to remove leading zeros from an otherwise integer value.

# sample usage:
# $cat << EOF | ./remove_leading_zeros.py
# > 001
# > 002
# > 003
# > EOF
# 1
# 2
# 3

import sys

for i in sys.stdin:
    print(int(i))