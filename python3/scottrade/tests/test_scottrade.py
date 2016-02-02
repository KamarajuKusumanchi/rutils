#! /usr/bin/env python3

import unittest

import scottrade

class TestScottrade(unittest.TestCase):
    def test_new_format(self):
        s = "Monthly_Statement_Apr_2010_12345678.pdf"
        ns = scottrade.new_format(s)
        self.assertEqual(ns, "Monthly_Statement_2010_04_12345678.pdf")

    def test_is_native_format(self):
        s1 = "Monthly_Statement_Apr_2010_12345678.pdf"
        s1_fmt = scottrade.is_native_format(s1)
        self.assertEqual(s1_fmt, True)

        s2 = "Monthly_Statement_2010_04_12345678.pdf"
        s2_fmt = scottrade.is_native_format(s2)
        self.assertEqual(s2_fmt, False)


if __name__ == '__main__':
    unittest.main()
