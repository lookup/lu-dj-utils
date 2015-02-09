# coding: utf-8
"""URL and HTTP related utilities.

Source: lookup_www.common.utils.urls (a subset with some edition).

"""
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import QueryDict


def build_querystring(query_dict):
    """Return a query string using ``query_dict`` contents.

    :param query_dict: contents of the query string
    :type query_dict: dict or :class:`django.http.QueryDict`
    :return: query string
    :rtype: str

    .. note::
        Note that ``query_dict`` can be a :class:`django.http.QueryDict`,
        which is a multi-valued dictionary.

    >>> q = {'next': '/a&b/'}
    >>> build_querystring(q)
    'next=%2Fa%26b%2F'

    >>> q = QueryDict('', mutable=True)
    >>> q['next'] = '/a&b/'
    >>> build_querystring(q)
    'next=%2Fa%26b%2F'

    """
    if not isinstance(query_dict, QueryDict):
        q = QueryDict('', mutable=True)
        q.update(query_dict)
        query_dict = q
    return query_dict.urlencode()


def reverse_with_querystring(url_name, query_dict, *args, **kwargs):
    """Return a reversed URL plus a querystring.

    The full URL is composed of the URL resolved using ``url_name``, ``args``
    and ``kwargs`` plus the query string built with ``query_dict``.

    :param url_name: URL pattern name to be reversed/resolved
    :type url_name: str
    :param query_dict: contents of the query string
    :type query_dict: dict or :class:`django.http.QueryDict`
    :param args: passed to :func:`django.core.urlresolvers.reverse`
    :param kwargs: passed to :func:`django.core.urlresolvers.reverse`
    :return: full URL e.g. '/tmovil/planes/seleccion-comuna/?x=y&foo=bar&foo='
    :rtype: str

    """
    querystring = build_querystring(query_dict)
    reversed_url = reverse(url_name, *args, **kwargs)
    return reversed_url + '?' + querystring


def build_full_url(obj, site=None, protocol='http'):
    """Build a full URL considering current site and ``obj``'s absolute URL.

    :param obj: must have a method named ``get_absolute_url``
    :type obj: :class:`django.db.models.Model`
    :param site: the site to use for the URL; if None, the current site will
        be used
    :type site: :class:`django.contrib.sites.models.Site` or None
    :param protocol: e.g. ftp, https
    :type protocol: string
    :return: full URL to access ``obj``
    :rtype: string

    >> build_full_url(Telefono.objects.get(slug='alcatel-282')
    http://www.lookup.cl/tmovil/telefonos/alcatel-282/

    """
    if site is None:
        site = get_current_site(None)
    # noinspection PyUnresolvedReferences
    return ''.join([protocol, '://', str(site), obj.get_absolute_url()])


def get_full_url(absolute_url, site=None, protocol='http'):
    """Convert ``absolute_url`` to a full URL considering current site.

    :param absolute_url: URL to convert
    :type absolute_url: str
    :param site: the site to use for the URL; if None, the current site will
        be used
    :type site: :class:`django.contrib.sites.models.Site` or None
    :param protocol: e.g. ftp, https
    :type protocol: string
    :return: full URL
    :rtype: string

    .. warning::
        ``absolute_url`` must begin with a slash character (``/``).

    >>> get_full_url('/x/abc/?ksdfd')
    http://www.lookup.cl/x/abc/?ksdfd

    """
    if site is None:
        site = get_current_site(None)
    return ''.join([protocol, '://', str(site), absolute_url])
