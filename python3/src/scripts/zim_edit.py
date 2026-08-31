#!/usr/bin/env python3
# Opens a zim wiki file in vim.
# If the file already exists, the script will just open it.
# If the file does not exist, the script will create it with standard
# zim-formatted header and add some predefined extra lines at the end.
#
# Usage: zim_edit.py <file.txt> or zim_edit.py <dir/file.txt>
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: zim_edit.py <file.txt>", file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    name = filepath.stem

    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)

        now = datetime.now().astimezone()
        creation_date = now.strftime("%Y-%m-%dT%H:%M:%S%z")
        creation_date = creation_date[:-2] + ":" + creation_date[-2:]

        day_name = now.strftime("%A")
        day = now.day
        month = now.strftime("%B")
        year = now.year

        content = f"""Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.6
Creation-Date: {creation_date}

====== {name} ======
Created {day_name} {day} {month} {year}

'''
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
'''
"""
        filepath.write_text(content)

    subprocess.run(["vim", str(filepath)])

if __name__ == "__main__":
    main()
