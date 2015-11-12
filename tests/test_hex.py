# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import unittest

from django.utils import six


class FunctionsTest(unittest.TestCase):

    def test_hex_sha1(self):
        from lu_dj_utils.hex import hex_sha1, SHA1_RE

        self.assertEqual(
            hex_sha1(''.encode('utf-8'),
                     ''.encode('utf-8')),
            'da39a3ee5e6b4b0d3255bfef95601890afd80709')
        self.assertEqual(
            hex_sha1('chao1'.encode('utf-8'),
                     'hola'.encode('utf-8')),
            'bf01a6b75b943b6be4b0d5cce120d5cee9559217')
        self.assertEqual(
            hex_sha1('hola'.encode('utf-8'),
                     'chao1'.encode('utf-8')),
            '61807d12b62246bbe5f46955746b9a4ffbc6fb0d')
        self.assertEqual(
            hex_sha1('hola'.encode('utf-8'),
                     'chao1'.encode('utf-8')),
            '61807d12b62246bbe5f46955746b9a4ffbc6fb0d')

        # test results match the corresponding regex
        for i in range(0, 10000):
            value = hex_sha1(''.encode('utf-8'), six.text_type(i).encode('utf-8'))
            self.assertIsNotNone(SHA1_RE.match(value))

    def test_random_hex_32(self):
        # values random enough such that there are no repetitions in 10,000 calls

        from lu_dj_utils.hex import random_hex_32, HEX_32_RE

        keys = {}
        size_ = 10000
        for i in range(0, size_):
            random_key = random_hex_32()
            keys[random_key] = None
            # test results match the corresponding regex
            self.assertIsNotNone(HEX_32_RE.match(random_key))
        # if there were any repeated keys then len(keys) < size_
        self.assertEquals(size_, len(keys))

    def test_random_hex_6(self):
        # values random enough such that there are no repetitions in 100 calls
        # (with 1,000 it fails frequently enough to be annoying)

        from lu_dj_utils.hex import random_hex_6, HEX_6_RE

        keys = {}
        size_ = 100
        for i in range(0, size_):
            random_key = random_hex_6()
            keys[random_key] = None
            # test results match the corresponding regex
            self.assertIsNotNone(HEX_6_RE.match(random_key))
        # if there were any repeated keys then len(keys) < size_
        self.assertEquals(size_, len(keys))
