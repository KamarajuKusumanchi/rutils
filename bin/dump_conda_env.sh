#! /usr/bin/env bash

set -e
set -u
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 env_name out_dir" >&2
  exit 1
fi

env_name="$1"
out_dir="$2"
asof=`date +%Y%m%d`
out_fname=environment_${env_name}_${asof}.yml
out_file=${out_dir}/${out_fname}

echo "conda environment of" $env_name "is saved to" $out_file
conda env export --name $env_name > $out_file
