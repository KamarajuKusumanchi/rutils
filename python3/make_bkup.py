#! /usr/bin/env python3

# Script to backup a file or directory
#
# The input is copied to src_asof_YYYYMMDD_HHmmSS where src is the original
# file or directory and YYYYMMDD_HHmmSS is its last modified time.

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from lib.file_utils import backup_with_timestamp

src = sys.argv[1]
backup_with_timestamp(src)
