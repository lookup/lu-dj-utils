# coding: utf-8
"""Some useful Django model fields.

Source: lookup_www.common.fields (but just a subset).

"""
from __future__ import absolute_import, print_function, unicode_literals

import django.db.models
import django.forms

import lu_dj_utils.hex


class Hex32Field(django.db.models.CharField):

    """Hex digits string of length 32, very practical for hash keys.

    Default value is calculated by :func:`lu_dj_utils.hex.random_hex_32` (UUID version 4).
    Although it's very unlikely that it returns a repeated value,
    uniqueness is enforced at database level as precautionary measure.

    """

    description = "32-hex-digits string"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = False
        kwargs['default'] = lu_dj_utils.hex.random_hex_32
        kwargs['max_length'] = 32
        kwargs['unique'] = True
        kwargs.setdefault('editable', False)
        super(Hex32Field, self).__init__(*args, **kwargs)


class Hex6Field(django.db.models.CharField):

    """Hex digits string of length 6.

    Default value is calculated by :func:`lu_dj_utils.hex.random_hex_6`
    (substring of UUID version 4).
    Uniqueness is enforced at database level as precautionary measure.

    """

    description = "6-hex-digits string"

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = False
        kwargs['default'] = lu_dj_utils.hex.random_hex_6
        kwargs['max_length'] = 6
        kwargs['unique'] = True
        kwargs.setdefault('editable', False)
        super(Hex6Field, self).__init__(*args, **kwargs)


# Tell South about the custom field. Since it's essentially an IntegerField (as
# South and DB are concerned), the definitions are as simple as they can be.
# Read:
# * http://south.readthedocs.org/en/latest/customfields.html#extending-introspection
# * http://south.readthedocs.org/en/latest/tutorial/part4.html#simple-inheritance
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^common\.fields\.Hex32Field"])
add_introspection_rules([], ["^common\.fields\.Hex6Field"])
