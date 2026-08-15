#!/usr/bin/env bash
#
# launch_tabs.sh — open Windows Terminal tabs in a set of directories.
#
# Usage:
#   ./launch_tabs.sh                -> uses config file, or the hardcoded DIRS list if no config file
#   ./launch_tabs.sh dir3 dir4 ...   -> ignores config file and DIRS, uses the given dirs instead
#
# Precedence: command line args > config file > hardcoded DIRS below.
#
# Config file location: $XDG_CONFIG_HOME/launch_tabs/dirs.conf (defaults to
# ~/.config/launch_tabs/dirs.conf if XDG_CONFIG_HOME is unset). One directory
# per line. Blank lines and lines starting with '#' are ignored.
#
# Any directory that doesn't exist (from any source: CLI args, config file,
# or the hardcoded default) is skipped with a warning rather than being
# passed to wt.

set -euo pipefail

# ---- hardcoded default directories (fallback if no config file exists) ----
# Uses ${var:-} so the script doesn't blow up under 'set -u' if learning/software
# aren't set in the environment — this fallback array is only used when neither
# CLI args nor a config file supply directories.
DIRS=(
  "${learning:-}"
  "${software:-}"
  "$HOME/x"
)

# ---- config file location ----
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/launch_tabs"
CONFIG_FILE="$CONFIG_DIR/dirs.conf"

# ---- load config file if present (and no command line args given) ----
read_config_dirs() {
  local file="$1"
  local line
  local -a result=()
  while IFS= read -r line || [ -n "$line" ]; do
    # strip leading/trailing whitespace
    line="${line#"${line%%[![:space:]]*}"}"
    line="${line%"${line##*[![:space:]]}"}"
    # skip blank lines and comments
    [ -z "$line" ] && continue
    [ "${line:0:1}" = "#" ] && continue
    result+=("$line")
  done < "$file"
  printf '%s\n' "${result[@]}"
}

if [ "$#" -gt 0 ]; then
  DIRS=("$@")
elif [ -f "$CONFIG_FILE" ]; then
  mapfile -t CONFIG_DIRS < <(read_config_dirs "$CONFIG_FILE")
  if [ "${#CONFIG_DIRS[@]}" -gt 0 ]; then
    DIRS=("${CONFIG_DIRS[@]}")
  fi
fi

if [ "${#DIRS[@]}" -eq 0 ]; then
  echo "No directories to open." >&2
  exit 1
fi

# ---- drop directories that don't exist, warning about each ----
VALID_DIRS=()
for d in "${DIRS[@]}"; do
  if [ -d "$d" ]; then
    VALID_DIRS+=("$d")
  else
    echo "Warning: '$d' does not exist or is not a directory — skipping." >&2
  fi
done
DIRS=("${VALID_DIRS[@]}")

if [ "${#DIRS[@]}" -eq 0 ]; then
  echo "No valid directories to open." >&2
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
