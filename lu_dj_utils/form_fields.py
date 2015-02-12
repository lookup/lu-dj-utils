# coding: utf-8
"""Some useful Django form fields.

"""
from __future__ import absolute_import, print_function, unicode_literals

import django.forms


class LowerCaseEmailField(django.forms.EmailField):

    def __init__(self, max_length=None, min_length=None, lower_case=False, *args, **kwargs):
        self.lower_case = lower_case
        super(LowerCaseEmailField, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        value = self.to_python(value).strip()
        if self.lower_case:
            value = value.lower()
        return super(LowerCaseEmailField, self).clean(value)
