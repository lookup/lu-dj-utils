# coding: utf-8
"""Utilities related to logging, log records, etc.

Source: lookup_www.common.log (with some modifications).

"""
from __future__ import absolute_import, print_function, unicode_literals


def not_http_404(log_record):
    """Check if ``log_record``'s ``status_code`` is not 404.

    :param log_record: log record
    :type log_record: :class:`logging.LogRecord`
    :return: False if ``log_record``'s ``status_code`` is 404

    """
    # LogRecord objects created by logger `django.request` have attribute `status_code`
    try:
        if log_record.status_code == 404:
            return False
    except Exception:
        pass
    return True
