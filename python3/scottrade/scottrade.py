#! /usr/bin/env python3

# Statements downloaded from Scottrade brokerage account are of the form
# Monthly_Statement_<abbreviated month name>_<year>_<account number>.pdf .
# The idea here is to rename them as
# Monthly_Statement_<YYYY>_<MM>_<account_number>.pdf .
# For example, Monthly_Statement_Jul_2014_12345678.pdf will be changed to
# Monthly_Statement_2014_07_12345678.pdf
#
# sample usage:
# % ls -1 .
# [Content_Types].xml
# DownloadStatements_20151011233051.zip
# Monthly_Statement_Jul_2014_12345678.pdf
# 
# % scottrade.py . --dry
# Trial run. No changes are made
# ./Monthly_Statement_Jul_2014_12345678.pdf  ->  ./Monthly_Statement_2014_07_12345678.pdf
# 
# % ls -1 .
# [Content_Types].xml
# DownloadStatements_20151011233051.zip
# Monthly_Statement_Jul_2014_12345678.pdf
# 
# % scottrade.py .
# ./Monthly_Statement_Jul_2014_12345678.pdf  ->  ./Monthly_Statement_2014_07_12345678.pdf
# 
# % ls -1 .
# [Content_Types].xml
# DownloadStatements_20151011233051.zip
# Monthly_Statement_2014_07_12345678.pdf


def new_format(s):
    """ Change the order of month and year, replace month name with the month
    number. For example
    Monthly_Statement_Apr_2010_12345678.pdf will be changed to
    Monthly_Statement_2010_04_12345678.pdf
    """
    prefix = s[0:17]
    suffix = s[27:40]
    month_name = s[18:21]
    year = s[22:26]

    month_num = month_name_to_num(month_name)
    delim = '_'
    new_s = prefix + delim + year + delim + month_num + delim + suffix
    return new_s


def month_name_to_num(s):
    """ Change the month name to the number
    For example, given Apr, this function returns 04
    """
    if (s == 'Jan'):
        return '01'
    elif (s == 'Feb'):
        return '02'
    elif (s == 'Mar'):
        return '03'
    elif (s == 'Apr'):
        return '04'
    elif (s == 'May'):
        return '05'
    elif (s == 'Jun'):
        return '06'
    elif (s == 'Jul'):
        return '07'
    elif (s == 'Aug'):
        return '08'
    elif (s == 'Sep'):
        return '09'
    elif (s == 'Oct'):
        return '10'
    elif (s == 'Nov'):
        return '11'
    elif (s == 'Dec'):
        return '12'
    else:
        print("month name = ", s)
        raise ValueError("Invalid month name")

def is_native_format(s):
    """ Return True if string s is in the native format such as
    Monthly_Statement_Apr_2010_12345678.pdf
    Otherwise return False
    """
    res = True;
    if (s[0:18] != 'Monthly_Statement_'):
        res = False;
    elif (not s[18:21].isalpha()):
        res = False;
    elif (s[21] != '_' or s[26] != '_'):
        res = False;
    elif (not s[22:26].isdigit()):
        res = False;
    elif (not s[27:35].isdigit()):
        res = False;
    elif (s[35:39] != '.pdf'):
        res = False;
    return res;

def rename_files(args):
    """ Change all the filenames in native format to a new
    format for a given directory.

    For example, Monthly_Statement_Apr_2010_12345678.pdf will be changed to
    Monthly_Statement_2010_04_12345678.pdf

    Pass the dry option to perform a trial run where by the changes are shown
    but not actually executed.

    Todo:- Have to write an unit test for this function.
    """
    dirname = args.dir
    dry = args.dry

    if (dry):
        print("Trial run. No changes are made")

    import os
    files = os.listdir(dirname)
    for orig in files:
        if (is_native_format(orig)):
            dest = new_format(orig)
            orig_abs = os.path.join(dirname, orig)
            dest_abs = os.path.join(dirname, dest)
            print(orig_abs, " -> ", dest_abs)
            if (not dry):
                os.rename(orig_abs, dest_abs)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description='rename scottrade statements',
        )
    parser.add_argument("dir", action="store",
        help="directory to operate on")
    parser.add_argument("--dry", action="store_true",
        default=False, dest="dry",
        help="perform a trial run with no changes made")
    args = parser.parse_args()

    rename_files(args)
