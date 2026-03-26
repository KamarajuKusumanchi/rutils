#! /usr/bin/env python3
# Script to create a file with today's date yyyy-mm-dd.txt and fill it with
# some content if such a file does not already exist and then open it in vim.
# If the file already exists, just open it in vim.
from pathlib import Path
import subprocess
from datetime import date


def main():
    # Get today's date in yyyy-mm-dd format
    date_str = date.today().isoformat()
    filename = f"{date_str}.txt"

    # If the file does not exist, create it with some content.
    if not Path(filename).exists():
        with open(filename, "w") as f:
            f.write("-" * 80 + "\n")
            f.write(f"today | {date_str}\n")
            f.write("-" * 80 + "\n")

    # Open in vim
    subprocess.run(["vim", filename])


if __name__ == "__main__":
    main()
