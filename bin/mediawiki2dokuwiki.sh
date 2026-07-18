#! /usr/bin/env sh

# Summary:
# Script to convert mediawiki files to dokuwiki files.
#
# Assumptions:
# * pandoc is installed
#
# 1)
# The --shift-heading-level-by=-1 ensures that
#     ==== foo ====
# is converted to
#     ==== foo ====
# instead of
#     === foo ===
#
# 2) The lua script replaces non-breaking spaces (U+00A0, UTF-8: 0xC2 0xA0)
# with regular spaces

pandoc -f mediawiki -t dokuwiki --shift-heading-level-by=-1 --lua-filter="$(dirname "$0")/nbsp.lua" "$@"
