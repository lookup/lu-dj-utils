# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from mock import MagicMock, Mock, NonCallableMock, NonCallableMagicMock, patch

from django.http import QueryDict
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.test.utils import override_settings
from django.utils.six.moves.urllib.parse import (
    quote, quote_plus, unquote, unquote_plus, urlparse, urlunparse,
    urlsplit, urlunsplit,
)


class BuildQuerystring(SimpleTestCase):  # TODO: change to unittest.TestCase?

    def setUp(self):
        mock_param = NonCallableMock()
        self._dict = {'next': '/a&b/', 'x': mock_param}
        self._query_dict = QueryDict('', mutable=True)
        self._query_dict.update(self._dict)

        part_a = 'next=%2Fa%26b%2F'
        part_b = 'x=' + quote_plus(str(mock_param))
        self.expected = (part_a + '&' + part_b, part_b + '&' + part_a)

    def test_with_dict(self):
        from lu_dj_utils.urls import build_querystring

        result = build_querystring(self._dict)
        self.assertTrue(
            result == self.expected[0] or result == self.expected[1])

    def test_with_query_dict(self):
        from lu_dj_utils.urls import build_querystring

        result = build_querystring(self._query_dict)
        self.assertTrue(
            result == self.expected[0] or result == self.expected[1])


class Functions(TestCase):  # TODO: change to SimpleTestCase or unittest.TestCase?

    @override_settings(SITE_ID=10)
    def test_build_full_url(self):
        from django.contrib.sites.models import Site
        from lu_dj_utils.urls import build_full_url

        Site.objects.create(pk=10, domain='mycooldomain.com')
        site2 = Site.objects.create(domain='www.domain2.com')

        obj = Mock()
        obj.get_absolute_url = Mock(return_value='/asdfkas/asldfk/12/5')

        url = build_full_url(obj)
        self.assertEqual(url, 'http://mycooldomain.com/asdfkas/asldfk/12/5')
        url = build_full_url(obj, site2)
        self.assertEqual(url, 'http://www.domain2.com/asdfkas/asldfk/12/5')
        url = build_full_url(obj, protocol='sftp')
        self.assertEqual(url, 'sftp://mycooldomain.com/asdfkas/asldfk/12/5')

    @override_settings(SITE_ID=10)
    def test_get_full_url(self):
        from django.contrib.sites.models import Site
        from lu_dj_utils.urls import get_full_url

        Site.objects.create(pk=10, domain='mycooldomain.com')
        site2 = Site.objects.create(domain='www.domain2.com')

        absolute_url = '/asdfkas/asldfk/12/5'

        url = get_full_url(absolute_url)
        self.assertEqual(url, 'http://mycooldomain.com/asdfkas/asldfk/12/5')
        url = get_full_url(absolute_url, site2)
        self.assertEqual(url, 'http://www.domain2.com/asdfkas/asldfk/12/5')
        url = get_full_url(absolute_url, protocol='sftp')
        self.assertEqual(url, 'sftp://mycooldomain.com/asdfkas/asldfk/12/5')
