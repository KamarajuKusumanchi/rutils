#! /usr/bin/env sh

# Summary:
# Script to convert mediawiki files to dokuwiki files.
#
# Assumptions:
# * pandoc is installed
#
# The --shift-heading-level-by=-1 ensures that
#     ==== foo ====
# is converted to
#     ==== foo ====
# instead of
#     === foo ===
pandoc -f mediawiki -t dokuwiki --shift-heading-level-by=-1 "$@"
