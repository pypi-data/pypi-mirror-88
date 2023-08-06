"""Tests for dlutil"""

import unittest

from dlmontepython.htk.sources.dlutil import remove_comments, load_ascii

class DLUtilTestCase(unittest.TestCase):

    def test_remove_comments(self):

        line1 = "# comment"
        line2 = "content # trailing comment"
        line3 = "\t # comment"
        line4 = "content"
        line5 = "content1 content2 # trailing comment"
        line6 = "content#comment"

        self.assertEqual(remove_comments(line1), "")
        self.assertEqual(remove_comments(line2), "content")
        self.assertEqual(remove_comments(line3), "")
        self.assertEqual(remove_comments(line4), "content")
        self.assertEqual(remove_comments(line5), "content1 content2")
        self.assertEqual(remove_comments(line6), "content")


    def test_load_ascii(self):

        lines = load_ascii(__file__)
        self.assertIsNotNone(lines)

        with self.assertRaises(IOError):
            lines = load_ascii("nonexistant.py")
