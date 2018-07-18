#! /usr/bin/env python3

# Script to backup a file or directory
#
# The input is copied to src_asof_YYYYMMDD_HHmmSS where src is the original
# file or directory and YYYYMMDD_HHmmSS is its last modified time.

import sys
from lib.file_utils import backup_with_timestamp

src = sys.argv[1]
backup_with_timestamp(src)
