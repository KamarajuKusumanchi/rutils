import re

# Todo: compact_print function already exists in ../stuff.py
# use it instead of copying it here.
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

def print_sources_list():
    fname = "/etc/apt/sources.list"
    comment_pattern = "^\s*#"
    # print("-"*80)
    print("\ncontents of ", fname, "\n")
    compact_print(fname, comment_pattern)
    # print("-"*80)

if __name__ == "__main__":
    print_sources_list()
