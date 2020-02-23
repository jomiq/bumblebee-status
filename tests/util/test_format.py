import unittest

from util.format import *

class format(unittest.TestCase):
    def test_int_from_string(self):
        self.assertEqual(100, asint('100'))
        self.assertEqual(-100, asint('-100'))
        self.assertEqual(0, asint('0'))

    def test_int_from_none(self):
        self.assertEqual(0, asint(None))

    def test_int_from_int(self):
        self.assertEqual(100, asint(100))
        self.assertEqual(-100, asint(-100))
        self.assertEqual(0, asint(0))

    def test_int_minimum(self):
        self.assertEqual(100, asint(100, minimum=10))
        self.assertEqual(100, asint(100, minimum=100))
        self.assertEqual(10, asint(5, minimum=10))

    def test_int_maximum(self):
        self.assertEqual(100, asint(100, maximum=200))
        self.assertEqual(100, asint(100, maximum=100))
        self.assertEqual(100, asint(200, maximum=100))

    def test_true_from_str(self):
        self.assertTrue(asbool('true'))
        self.assertTrue(asbool(True))
        self.assertTrue(asbool('t'))
        self.assertTrue(asbool('1'))
        self.assertTrue(asbool('yes'))
        self.assertTrue(asbool('y'))
        self.assertTrue(asbool('on'))

    def test_false_from_str(self):
        self.assertFalse(asbool('false'))
        self.assertFalse(asbool(False))
        self.assertFalse(asbool('f'))
        self.assertFalse(asbool('0'))
        self.assertFalse(asbool('no'))
        self.assertFalse(asbool('n'))
        self.assertFalse(asbool('off'))
        self.assertFalse(asbool(None))

    def test_list_from_None(self):
        self.assertEqual([], aslist(None))

    def test_list_from_list(self):
        self.assertEqual([1,2,3], aslist([1,2,3]))

    def test_list_from_str(self):
        self.assertEqual(['12', '13', '14'], aslist('12,13,14'))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4