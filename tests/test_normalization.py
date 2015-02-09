# coding: utf-8
"""Source: lookup_www.lu_base.tests (but just a subset).

"""
from __future__ import absolute_import, print_function, unicode_literals

import unittest


class Functions(unittest.TestCase):

    def test_normalize_email(self):
        from lu_dj_utils.normalization import normalize_email

        self.assertEqual('a@a.com', normalize_email('A@A.COM'))
        self.assertEqual('a@a.com', normalize_email(' a@a.com '))
        self.assertEqual('a@a.com', normalize_email('\t  a@a.com\n'))

    def test_normalize_name(self):
        from lu_dj_utils.normalization import normalize_name

        self.assertEqual(normalize_name('oneTwoThree'), 'one_two_three')
        self.assertEqual(normalize_name('UnoAUno'), 'uno_a_uno')
        self.assertEqual(normalize_name('UnoAUNo'), 'uno_au_no')
