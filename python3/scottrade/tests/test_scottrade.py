#! /usr/bin/env python3

import unittest

import scottrade

class TestScottrade(unittest.TestCase):
    def test_new_format(self):
        s = "Monthly_Statement_Apr_2010_12345678.pdf"
        ns = scottrade.new_format(s)
        self.assertEqual(ns, "Monthly_Statement_2010_04_12345678.pdf")

if __name__ == '__main__':
    unittest.main()
