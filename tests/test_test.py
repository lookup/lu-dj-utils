# coding: utf-8
"""Source: lookup_www.common.utils.tests.test_utils_test.

"""
from __future__ import absolute_import, print_function, unicode_literals

from django.test import SimpleTestCase, TestCase
from django.utils import six


class FunctionsTest(TestCase):  # TODO: change to SimpleTestCase or unittest.TestCase?

    def test_create_request(self):
        from django.core.handlers.wsgi import WSGIRequest
        from lu_dj_utils.test import create_request

        req = create_request('my-path', 'get')
        self.assertIsInstance(req, WSGIRequest)
        self.assertEqual(req.META['PATH_INFO'], 'my-path')
        self.assertEqual(req.META['REQUEST_METHOD'], 'GET')

        data = {'x': 'y', 'a': 1}
        req = create_request('something', 'post', data=data)
        self.assertIsInstance(req, WSGIRequest)
        self.assertEqual(req.META['PATH_INFO'], 'something')
        self.assertEqual(req.META['REQUEST_METHOD'], 'POST')
        six.assertCountEqual(  # in Python2 = assertItemsEqual
            self,
            req.POST.items(),
            [('x', 'y'), ('a', '1')])
