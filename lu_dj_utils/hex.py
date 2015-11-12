# coding: utf-8
"""Functions and constants about hex values, UUID, hashes and random values.

Source: lookup_www.common.utils.hash

"""
from __future__ import absolute_import, print_function, unicode_literals

import hashlib
import re
import uuid


HEX_6_RE = re.compile('^[a-f0-9]{6}$')  # 6 hex digits string
HEX_32_RE = re.compile('^[a-f0-9]{32}$')  # 32 hex digits string
HEX_40_RE = re.compile('^[a-f0-9]{40}$')  # 40 hex digits string
SHA1_RE = HEX_40_RE
UUID4_RE = HEX_32_RE


def hex_sha1(salt, value):
    """Return a 40-character string containing only hexadecimal digits based on
    the string resulting from the concatenation of strings `salt` and `value`.
    These can be regular or unicode strings but non-ascii characters can not be
    used.

    Equivalent to hashlib.sha1(salt + value).hexdigest()

    :param salt:
    :type salt: six.binary_type
    :param value:
    :type value: six.binary_type

    """
    m = hashlib.sha1()
    m.update(salt)
    m.update(value)
    return m.hexdigest()


def random_hex_32():
    """Return a 32-character string containing only hexadecimal digits based on
    a random generated version-4 UUID.

    """
    return uuid.uuid4().hex


def random_hex_6():
    """Return a string of 6 hexadecimal digits based on :func:`random_hex_32`.

    """
    return random_hex_32()[:6]
