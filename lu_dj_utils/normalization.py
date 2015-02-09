# coding: utf-8
"""Source: lookup_www.lu_base.utils (but just an edited subset).

"""
from __future__ import absolute_import, print_function, unicode_literals

import re


def normalize_email(email):
    """Lowercase ``email`` and remove its leading and trailing whitespace.

    >>> normalize_email('A@A.COM')
    'a@a.com'
    >>> normalize_email('\t  a@a.com\n')
    'a@a.com'

    """
    return email.strip().lower()


def normalize_name(name):
    """Convert camel-case style names into underscore separated words.

    >>> normalize_name('oneTwoThree')
    'one_two_three'
    >>> normalize_name('FourFiveSix')
    'four_five_six'

    Source: `django.contrib.formtools.wizard.views.normalize_name`

    """
    new = re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', name)
    return new.lower().strip('_')
