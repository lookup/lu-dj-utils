# coding: utf-8
"""Source: lookup_www.common.views (but just a subset).

"""
from __future__ import absolute_import, print_function, unicode_literals

import logging


logger = logging.getLogger(__name__)


class SetTestCookieMixin(object):

    """Override :meth:`get` to set test cookie, creating a session in advance.

    This lets us track a visitor by effectively knowing its session key before
    he/she performs any "action".

    """

    def get(self, request, *args, **kwargs):
        """Override to set a cookie (create a session) to track user."""
        try:
            request.session.set_test_cookie()
        except Exception:
            logger.exception("Couldn't set test cookie", extra={'request': request})
        return super(SetTestCookieMixin, self).get(request, *args, **kwargs)
