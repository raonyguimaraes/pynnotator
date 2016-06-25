from unittest import TestCase

import pynnotator

class TestDbnfsp(TestCase):
    def test_is_string(self):
        s = pynnotator.dbnfsp()
        self.assertTrue(isinstance(s, basestring))