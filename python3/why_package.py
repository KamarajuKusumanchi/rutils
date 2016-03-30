import subprocess
import argparse


def do_it(cmd):
    print(cmd)
    subprocess.call([cmd], shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Utility script that tells why a given set of packages
        are installed.''')
    parser.add_argument(
        "fname", action="store",
        help='''file containing a list of packages separated by spaces.
        Multiple lines are fine.''')
    args = parser.parse_args()

    packages = []

    fname = args.fname
    fh = open(fname)
    for line in fh:
        words = line.rstrip().split()
        packages += words

    print("Processing")
    print(packages)
    for i in packages:
        do_it('aptitude why {i}'.format(**locals()))


# Sample usage:
# python3 -u why_package.py packages.txt |& tee log.txt
