#! /usr/bin/env python3

import sys
from lib.file_utils import backup_with_timestamp

src = sys.argv[1]
backup_with_timestamp(src)
