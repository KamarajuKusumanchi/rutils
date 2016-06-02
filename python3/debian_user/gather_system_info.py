import re
import subprocess

''' This script aims to gather system information for common configuration
tasks such as sound, graphics, wireless, network, printer etc., Initially, only
the sound task is supported. Support for other tasks will be added in the due
course.

Output:
Relevant system information will be printed to stdout.

Potential use case:
When requesting help on a particular task on debian-user mailing list, the
requestor can simply copy paste the output of this script into the initial
email so that experts will have all the necessary information to solve the
issue at hand.

Todo:
Move functions such as compact_print into a standalone
module instead of copying them everywhere. For example these functions
already exist in ../stuff.py
'''


def sound():
    run_lspci()
    run_lsmod()
    print_sources_list()
    kernel_version()


def run_lspci():
    cmd = "lspci -nnk | grep -i audio"
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    print(output)


def run_lsmod():
    cmd = "lsmod | grep snd"
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    print(output)


def print_sources_list():
    fname = "/etc/apt/sources.list"
    comment_pattern = "^\s*#"
    print("\n# contents of ", fname)
    compact_print(fname, comment_pattern)
    print()


def compact_print(fname, comment_pattern):
    empty_pattern = "^\s*$"

    fh = open(fname)
    for line in fh:
        line = line.rstrip()
        if re.search(comment_pattern, line):
            continue
        elif re.search(empty_pattern, line):
            continue
        else:
            print(line)


def kernel_version():
    cmd = "uname -a"
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    print(output)


if __name__ == "__main__":
    sound()
