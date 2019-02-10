import sys

"""
Utility script to calculate difference between two time stamps.

Sample usage:
 % python3 time_calc.py --start 2:05 --end 5:13
188.0
"""


def parse_arguments(args):
    import argparse
    parser = argparse.ArgumentParser(
        description='get difference between two timestamps')
    parser.add_argument(
        "--start", action='store',
        default="0:0", dest="start",
        help="Starting timestamp HH:MM")
    parser.add_argument(
        "--end", action='store',
        default="0:0", dest="end",
        help="Ending timestamp HH:MM")
    return parser.parse_args(args)


def diff_time(begin, end):
    hm_begin = HourMinute(begin)
    hm_end = HourMinute(end)
    total_minutes_begin = hm_begin.total_minutes()
    total_minutes_end = hm_end.total_minutes()
    return (total_minutes_end - total_minutes_begin)


class HourMinute:
    hours = 0
    mins = 0

    def __init__(self, hhmm_str):
        tokens = hhmm_str.split(":")
        self.hours = float(tokens[0])
        self.mins = float(tokens[1])

    def total_minutes(self):
        return self.hours * 60 + self.mins

    def dump(self):
        print("hours = ", self.hours)
        print("minutes = ", self.mins)


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    print(diff_time(args.start, args.end))
