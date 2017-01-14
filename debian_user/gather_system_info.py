#! /usr/bin/env python3
import re
import subprocess
import shutil
import sys

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
module instead of copying them everywhere. For example this function
already exists in python3/stuff.py
'''


def parse_arguments(args):
    import argparse
    parser = argparse.ArgumentParser(
        description="Script to gather system information."
        )
    parser.add_argument(
        "--debug", "-d", action='store_true',
        default=False, dest='debug',
        help='show debug output. Default is false.')
    parser.add_argument(
        "--verbose", "-v", action='store_true',
        default=False, dest='verbose',
        help='show verbose output. Default is false.')

    res = parser.parse_args(args)
    if res.debug:
        print(res)
    return res


def determine_category(msg, args):
    import operator

    debug = args.debug

    known_categories = ['audio', 'video', 'wireless', 'apt']

    category_count = {k: 0 for k in known_categories}

    word_to_category = {
        'audio': 'audio',
        'sound': 'audio',

        'video': 'video',
        'graphics': 'video',
        'display': 'video',

        'wireless': 'wireless',
        'wire less': 'wireless',
        'wifi': 'wireless',

        'apt-get': 'apt',
        'aptget': 'apt',
        'apt': 'apt',
        'aptitude': 'apt',
        'install': 'apt',
        'update': 'apt',
        'package': 'apt',
        'packages': 'apt',
        'packaging': 'apt',
        'repository': 'apt',
        'repositories': 'apt'}

    # Todo: checking for single words at the moment. Have to extend this to
    # check for two word combos (ex:- 'wire less').
    words = msg.split()
    for w in words:
        if w in word_to_category:
            category = word_to_category[w]
            category_count[category] += 1

    if (debug):
        print('category_count')
        print(category_count)

    # get the category that occurred most number of times
    max_count_category = max(category_count.items(),
                             key=operator.itemgetter(1))[0]
    if (debug):
        print("max_count_category = ", max_count_category)
    return max_count_category


def collect_system_info(category):
    if category == 'audio':
        print('collecting info on:', category)
        collect_audio_info()
    else:
        print("unknown category:", category)


def collect_audio_info():
    ''' Use inxi if it exists. Otherwise get the information by running
    individual commands.'''
    have_inxi = shutil.which('inxi')
    if (have_inxi):
        run_inxi()
    else:
        run_lspci()
        run_lsmod()
        kernel_version()
        print_sources_list()


def run_inxi():
    cmd = "inxi -Ar"
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    print(output)


def run_lspci():
    # This tells what audio drivers are currently in use
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
    args = parse_arguments(sys.argv[1:])
    topic = input("Enter a brief description of the issue:\n")
    category = determine_category(topic, args)
    collect_system_info(category)
