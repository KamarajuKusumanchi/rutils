import unittest

import time_calc


class ConvertTime(unittest.TestCase):
    def test_convert_to_minutes(self):
        hm = time_calc.HourMinute("8:25")
        total_minutes = 505
        result = hm.total_minutes()
        self.assertEqual(result, total_minutes)

        hm = time_calc.HourMinute("14:12")
        total_minutes = 852
        result = hm.total_minutes()
        self.assertEqual(result, total_minutes)

    def test_diff_time(self):
        args = time_calc.parse_arguments(['--start', '2:05', '--end', '5:13'])
        difference = 188
        result = time_calc.diff_time(args.start, args.end)
        self.assertEqual(result, difference)

        args = time_calc.parse_arguments(['--start', '5:30', '--end', '10:05'])
        difference = 275
        result = time_calc.diff_time(args.start, args.end)
        self.assertEqual(result, difference)


if __name__ == '__main__':
    unittest.main()
