#! /usr/bin/env bash

#------------------------------------------------------------------------------
# If I cd into a directory for the first time in last 24 hours and if the
# directory is part of a git project, then check if the git repo is updated
# upstream. If yes, then prompt the user and check if the user wants to
# update the repo to upstream and if the user says yes, do it. Assume that I am
# using bash.
#
# How to use it: source this script in your .bashrc
#
# changelog:
# * 2026-04-14 initial version is from @claude.

# Track visited dirs to avoid re-checking within 24 hours
_GIT_CHECK_CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/git_upstream_checks"
mkdir -p "$_GIT_CHECK_CACHE_DIR"

_check_git_upstream() {
    # Only run after a directory change
    [[ "$PWD" == "$_LAST_PWD" ]] && return
    _LAST_PWD="$PWD"

    # Check if this dir is inside a git repo
    local git_root
    git_root=$(git rev-parse --show-toplevel 2>/dev/null) || return

    # Build a cache key from the git root path (replace / with _)
    local cache_key="${_GIT_CHECK_CACHE_DIR}/${git_root//\//_}"

    # Skip if we've already checked this repo in the last 24 hours
    if [[ -f "$cache_key" ]]; then
        local last_check now
        last_check=$(cat "$cache_key")
        now=$(date +%s)
        (( now - last_check < 86400 )) && return
    fi

    # Record the check time
    date +%s > "$cache_key"

    # Fetch upstream quietly (no output if offline)
    git fetch --quiet 2>/dev/null || return

    # Get current branch and its upstream
    local branch upstream local_sha upstream_sha
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    upstream=$(git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>/dev/null) || return

    local_sha=$(git rev-parse HEAD)
    upstream_sha=$(git rev-parse "$upstream")

    # If already up to date, do nothing
    [[ "$local_sha" == "$upstream_sha" ]] && return

    # Check if we're strictly behind (not diverged)
    local merge_base
    merge_base=$(git merge-base HEAD "$upstream")

    if [[ "$merge_base" == "$local_sha" ]]; then
        local commit_count
        commit_count=$(git rev-list HEAD.."$upstream" --count)
        echo ""
        echo "📦 Git: '$branch' is $commit_count commit(s) behind '$upstream'."
        read -rp "   Pull now? [y/N] " answer
        if [[ "$answer" =~ ^[Yy]$ ]]; then
            git pull
        fi
    else
        # Diverged — just warn, don't auto-pull
        echo ""
        echo "⚠️  Git: '$branch' has diverged from '$upstream'. Manual merge required."
    fi
}

PROMPT_COMMAND="_check_git_upstream${PROMPT_COMMAND:+; $PROMPT_COMMAND}"
#------------------------------------------------------------------------------

