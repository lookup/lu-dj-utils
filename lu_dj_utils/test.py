# coding: utf-8
"""Utilities for creating test cases.

Source: lookup_www.common.utils.test.

"""
from __future__ import absolute_import, print_function, unicode_literals

from mock import NonCallableMock

import django.test


class TestServerClient(django.test.Client):

    """Overrides constructor kwarg ``SERVER_NAME``.

    Some unit tests require that the host of the HTTP requests returned by
    the test client is a valid domain, and not the default ``testserver``.
    By default this class uses ``testclient.com``.

    This source helped: http://stackoverflow.com/questions/6291120/

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('SERVER_NAME', 'testclient.com')
        super(TestServerClient, self).__init__(*args, **kwargs)


class MonkeyPatchedRF(django.test.RequestFactory):

    """Subclass that adds attributes ``session`` and ``user`` to requests.

    If the ``SessionMiddleware`` is enabled, "real" requests
    will have an attribute ``user``.

    If the ``AuthenticationMiddleware`` is enabled, "real" requests
    will have an attribute ``session``.

    By overriding method :meth:`request`, both attributes are added
    by default, although that can be changed with constructor kwargs
    ``add_session`` and ``add_user``.

    .. warning::
       The added attributes aren't "real", they are just mock objects
       (:class:`mock.NonCallableMock` specifically).

    """

    def __init__(self, add_session=True, add_user=True, **kwargs):
        self.add_session = add_session
        self.add_user = add_user
        super(MonkeyPatchedRF, self).__init__(**kwargs)

    def request(self, **request):
        req = super(MonkeyPatchedRF, self).request(**request)

        if self.add_session:
            req.session = NonCallableMock(name='request session')
            req.session.session_key = 'abc123'

        if self.add_user:
            req.user = NonCallableMock(name='request user')

        return req


def create_request(path, method='get', data=None, **extra):
    """Return a HTTP request for ``path`` and ``data`` using ``method``.

    This function is just a shortcut to avoid instantiation of
    :class:`MonkeyPatchedRF`. If you need many requests, it's better to
    create a request factory object and use it to create each one.

    :param path:
    :param method: HTTP method of the request, it can be any of the supported
        by :class:`django.test.RequestFactory` e.g. ``get``, ``post``,
        ``head``, ``options``, ``put`` or ``delete``
    :return: HTTP request for ``path`` and ``data`` using ``method``
    :rtype: :class:`django.core.handlers.wsgi.WSGIRequest`

    """
    method = method.lower()  # methods are in lower case in the RF class
    data = data or {}
    rf = MonkeyPatchedRF()

    func = getattr(rf, method)
    return func(path, data=data, **extra)


def setup_view(view, request, *args, **kwargs):
    """Mimic as_view() returned callable, but returns a view instance.

    :type args: the same you would pass to
        :func:`django.core.urlresolvers.reverse`
    :type kwargs: the same you would pass to
        :func:`django.core.urlresolvers.reverse`

    Source: http://tech.novapost.fr/django-unit-test-your-views-en.html

    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
