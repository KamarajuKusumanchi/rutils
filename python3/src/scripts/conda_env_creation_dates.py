import json
import os
import subprocess
import re
import traceback


def get_conda_env_creation_dates():
    try:
        # Get conda environment paths
        result = subprocess.run(
            ['conda', 'info', '--json'], capture_output=True, text=True, check=True
        )
        # There were some characters such as
        #   \x1b[0m
        # at the beginning of result.stdout .
        # tags | color codes
        #
        # If I run
        #   json.loads(result.stdout)
        # on it, it is giving
        #  json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        #
        # Use a regular expression to strip the ANSI escape codes from the
        # output string before parsing it with json.loads()
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        clean_stdout = ansi_escape.sub('', result.stdout)
        conda_info = json.loads(clean_stdout)
        env_paths = [env for env in conda_info['envs']]

        creation_dates = {}
        for env_path in env_paths:
            history_file = os.path.join(env_path, 'conda-meta', 'history')
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line:
                        creation_dates[env_path] = first_line
        return creation_dates

    except subprocess.CalledProcessError as e:
        print("Error running conda command.")
        traceback.print_exc()
        return {}
    except FileNotFoundError as e:
        print("conda command not found. Ensure conda is installed and in your PATH.")
        traceback.print_exc()
        return {}


if __name__ == "__main__":
    dates = get_conda_env_creation_dates()
    if dates:
        for env_path, date in sorted(dates.items()):
            print(f"{date} {env_path}")
