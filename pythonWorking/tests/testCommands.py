

# cd "C:\Users\jaese\Desktop\programming folder\python\pythonWorking\tests"
"""
cd python\pythonWorking
python -m unittest tests.testCommands -v
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main
import commands
from storage import load_entries, save_entries, append_entries, save_json


class TestStringMethods(unittest.TestCase):


    def test_has_entry(self):
        entries = [
            {
                "date":"2026-07-20",
                "text":"python 공부"
            },
            {
                "date":"2026-07-22",
                "text":"GitHub"
            }
        ]
        result = main.has_entry(entries, "2026-07-22")
        self.assertTrue(result)


    def test_has_date(self):
        result = main.has_date("date", ["main.py", "date", "2026-07-20"])
        self.assertTrue(result)


    def test_date_format_check(self):
        result = main.date_format_check("date", ["main.py", "date", "2026/07/20"])
        self.assertFalse(result)


    def test_date_exist_check(self):
        result = main.date_exist_check("date", ["main.py", "date", "2020-02-29"])
        self.assertEqual(result,None)


    def test_find_entries(self):

        entries = [
            {
                "date":"2026-07-20",
                "text":"python 공부"
            },
            {
                "date":"2026-07-21",
                "text":"GitHub"
            }
        ]

        result = commands.find_entries(entries, "python")
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()