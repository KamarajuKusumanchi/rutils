#!/usr/bin/env bash
#
# launch_tabs.sh — open Windows Terminal tabs in a set of directories.
#
# Usage:
#   ./launch_tabs.sh                  -> uses the hardcoded DIRS list below
#   ./launch_tabs.sh dir3 dir4 ...    -> ignores DIRS, uses the given dirs instead

set -euo pipefail

# ---- hardcoded default directories ----
DIRS=(
    "$learning"
    "$software"
    "$HOME/x"
)

# ---- pick which list to use ----
if [ "$#" -gt 0 ]; then
    DIRS=("$@")
fi

if [ "${#DIRS[@]}" -eq 0 ]; then
    echo "No directories to open." >&2
    exit 1
fi

# ---- figure out how to invoke wt ----
if command -v wt.exe >/dev/null 2>&1; then
    WT=wt.exe
elif command -v wt >/dev/null 2>&1; then
    WT=wt
else
    echo "Error: 'wt' / 'wt.exe' not found on PATH." >&2
    exit 1
fi

# ---- build the argument list ----
# First pane: wt -d dir1
# Each subsequent: ; new-tab -d dirN
args=(-d "${DIRS[0]}")
for d in "${DIRS[@]:1}"; do
    args+=(\; new-tab -d "$d")
done

# ---- launch ----
"$WT" "${args[@]}"
