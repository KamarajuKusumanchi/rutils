#! /usr/bin/env bash

# Play a random telugu song

# The song links are obtained from this repo
REPO=$HOME/work/github/telugu_song_lyrics
if [ ! -d "$REPO" ]; then
    echo "ERROR: $REPO does not exist"
    exit 1
fi
cd $REPO

songs=`git grep -h youtube | cut -f 2- -d ' ' | cut -f 1 -d ','`
random_song=`shuf -n1 -e $songs`

# PLAYER=/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe
PLAYER=/usr/bin/google-chrome
"$PLAYER" $random_song
