from unittest import TestCase

import pynnotator

class TestPynnotator(TestCase):
    def test_is_string(self):
        s = pynnotator.pynnotator()
        self.assertTrue(isinstance(s, basestring))