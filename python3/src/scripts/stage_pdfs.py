#! /usr/bin/env python3
# Stages PDF books into a working directory as the first step in a
# read-annotate-export pipeline using pdfannots.
#
# PURPOSE:
#   Prepares a working directory of PDF files for annotation without modifying
#   the originals. This is useful when you want to:
#
#     1. Keep the original PDFs pristine and unmodified at all times
#     2. Annotate freely in the working directory without fear of data loss
#     3. Use pdfannots to extract annotations from the working copies
#        into plain text or Markdown for use in a note-taking system
#
# TYPICAL WORKFLOW:
#     1. Place original PDFs in $BOOKS_ROOT/originals/
#     2. Pipe a list of PDFs to this script via find or similar tools
#     3. Open PDFs from the working directory in your PDF reader (e.g., Okular
#        on Linux, Adobe Acrobat Reader on Windows via Git Bash)
#     4. Annotate while reading - highlights, notes, comments, etc.
#     5. Save the annotated PDF file back to the working directory
#     6. Run pdfannots on the working copy to extract annotations:
#            pdfannots $BOOKS_ROOT/working/yourfile.pdf
#
# USAGE:
#   Accepts a list of files from stdin - only .pdf files are processed,
#   all other file types (e.g., .txt) are silently skipped.
#
#   Both absolute and relative paths are supported:
#
#     $ find ~/books -iname '*python*cook*' | python.exe stage_pdfs.py
#     $ find . -iname '*python*cook*'       | python.exe stage_pdfs.py
#
# CROSS-PLATFORM USAGE:
#   This script runs on Linux and Windows (via Git Bash). Set the BOOKS_ROOT
#   environment variable in ~/.bashrc on each machine to point to the local
#   root directory. The path format can differ per machine - the script
#   handles it transparently via os.path.
#
#     Example ~/.bashrc entries:
#       Machine 1 (Windows): export BOOKS_ROOT="/c/Users/raju/books"
#       Machine 2 (Linux):   export BOOKS_ROOT="/opt/rajulocal/books"
#       Machine 3 (Windows): export BOOKS_ROOT="/h/books"

import os
import sys
import shutil

ROOT = os.environ["BOOKS_ROOT"].replace("\\", "/")
WORKING_DIR = os.path.join(ROOT, "working")

# Guard against running the script interactively without piped input.
# Without this check, sys.stdin would block indefinitely waiting for
# input, causing the script to hang with no prompt or error message.
# sys.stdin.isatty() returns True when stdin is connected to a terminal
# (i.e., no pipe), and False when data is being piped in.
if sys.stdin.isatty():
    print("Usage: find <path> -iname '*.pdf' | python stage_pdfs.py")
    sys.exit(1)

if not os.path.isdir(WORKING_DIR):
    print(f"Creating: {WORKING_DIR}")
    os.makedirs(WORKING_DIR)

for line in sys.stdin:
    src = os.path.realpath(line.strip())

    if not src.endswith(".pdf"):
        continue

    if not os.path.isfile(src):
        print(f"Warning: File not found, skipping: {src}")
        continue

    fname = os.path.basename(src)
    dst = os.path.join(WORKING_DIR, fname)

    if not os.path.isfile(dst):
        shutil.copy2(src, dst)
        print(f"Copied (new): {src} -> {dst}")
    elif os.path.getmtime(src) > os.path.getmtime(dst):
        shutil.copy2(src, dst)
        print(f"Copied (updated): {src} -> {dst}")
    else:
        print(f"Skipped (up to date): {fname}")
