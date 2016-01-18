#! /usr/bin/env python3


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


if __name__ == "__main__":
    s = "Monthly_Statement_Apr_2010_12345678.pdf"
    ns = new_format(s)
    s_need_conversion = is_native_format(s)
    ns_need_conversion = is_native_format(ns)
    print("s_need_conversion = ", s_need_conversion);
    print("ns_need_conversion = ", ns_need_conversion);
