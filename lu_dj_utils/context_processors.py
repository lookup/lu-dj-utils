# coding: utf-8
"""Some useful Django template context processors.

"""
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


def track_visit(request):
    """Whether the current visit should be tracked by analytics software/services.

    .. warning:
       The setting ``TESTING`` must be defined.

    A visit should not be tracked if the website is running in debug mode, in test or
    if the user is a staff member.

    Based in ``lookup_www0/lookup/context_processors.py/do_register_visit``.

    """
    do_track_visit = True
    if settings.DEBUG or settings.TESTING:
        do_track_visit = False
    if hasattr(request, 'user'):
        if request.user.is_staff:
            do_track_visit = False
    return {'track_visit': do_track_visit}
