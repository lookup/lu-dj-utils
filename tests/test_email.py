# coding: utf-8
"""Source: lookup_www.common.tests.test_utils.mail (with some edition).

"""
from __future__ import absolute_import, print_function, unicode_literals

from mock import MagicMock, Mock, NonCallableMock, NonCallableMagicMock, patch

from django.conf import settings
from django.core import mail as django_mail
from django.test import SimpleTestCase, TestCase


class PlainEmail(SimpleTestCase):

    def setUp(self):
        NCMock = NonCallableMock

        self.subject = NCMock(spec=str)
        self.body = NCMock(spec=str)
        self.from_email = NCMock(spec=str)

        # self.to = NonCallableMagicMock(spec=list)
        # self.to.__iter__.return_value = ['to0', 'to1', 'to2']
        # self.cc = NonCallableMagicMock(spec=list)
        # self.cc.__iter__.return_value = ['cc0', 'cc1', 'cc2']
        # self.bcc = NonCallableMagicMock(spec=list)
        # self.bcc.__iter__.return_value = ['bcc0', 'bcc1', 'bcc2']

        self.to = ['to0', 'to1', 'to2']
        self.cc = ['cc0', 'cc1', 'cc2']
        self.bcc = ['bcc0', 'bcc1', 'bcc2']

        self.reply_to = NCMock(spec=str)
        self.fail_silently = NCMock(spec=bool)
        self.auth_user = NCMock(spec=str)
        self.auth_password = NCMock(spec=str)
        self.connection = NCMock()
        self.attachments = NCMock(spec=list)
        self.headers = NonCallableMagicMock(spec=dict)

    def test_create_message(self):
        from lu_dj_utils.email import PlainEmail

        msg = PlainEmail().create_message()
        self.assertIsInstance(msg, PlainEmail.django_mail_class)

        msg = PlainEmail(
            subject=self.subject, body=self.body, from_email=self.from_email,
            to=self.to, bcc=self.bcc, connection=self.connection,
            attachments=self.attachments, headers=self.headers, cc=self.cc
        ).create_message()
        self.assertIsInstance(msg, PlainEmail.django_mail_class)
        self.basic_msg_assertions(msg)

    def test_real_send(self):
        from lu_dj_utils.email import PlainEmail

        _reset_test_outbox()
        self.assertEqual(len(django_mail.outbox), 0)

        subject = 'hello!'
        body = 'my email body'
        to = ['a@a.cl', 'x@xx.com']

        result = PlainEmail(subject=subject, body=body).send()
        self.assertEqual(result, 0)

        result = PlainEmail(subject=subject, body=body, to=to).send()
        self.real_send_assertions(to, body, result)

    def basic_msg_assertions(self, msg):
        self.assertEqual(self.subject, msg.subject)
        self.assertEqual(self.body, msg.body)
        self.assertEqual(self.from_email, msg.from_email)
        self.assertEqual(self.to, msg.to)
        self.assertEqual(self.cc, msg.cc)
        self.assertEqual(self.bcc, msg.bcc)
        self.assertEqual(self.connection, msg.connection)
        self.assertEqual(self.attachments, msg.attachments)
        self.assertDictContainsSubset(self.headers, msg.extra_headers)

    def real_send_assertions(self, to, body, result):
        outbox = django_mail.outbox
        self.assertEqual(result, 1)
        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].to, to)
        self.assertIn(body, outbox[0].body)


class HTMLEmail(PlainEmail):

    def setUp(self):
        super(HTMLEmail, self).setUp()
        self.html_body = NonCallableMock(spec=str)

    def test_create_message(self):
        from lu_dj_utils.email import HTMLEmail

        msg = HTMLEmail(self.html_body).create_message()
        self.assertIsInstance(msg, HTMLEmail.django_mail_class)

        msg = HTMLEmail(
            self.html_body,
            subject=self.subject, body=self.body, from_email=self.from_email,
            to=self.to, bcc=self.bcc, connection=self.connection,
            attachments=self.attachments, headers=self.headers, cc=self.cc
        ).create_message()
        self.assertIsInstance(msg, HTMLEmail.django_mail_class)
        self.basic_msg_assertions(msg)
        self.assert_HTML_alternative(msg, self.html_body)

    def test_real_send(self):
        from lu_dj_utils.email import HTMLEmail, render_to_string

        _reset_test_outbox()
        self.assertEqual(len(django_mail.outbox), 0)

        subject = 'hello!'
        body = 'my email body'
        html_body_template_name = 'email1_body.html'
        to = ['a@a.cl', 'x@xx.com']

        html_body = render_to_string(html_body_template_name)

        result = HTMLEmail(
            html_body, subject=subject, body=body).send()
        self.assertEqual(result, 0)

        result = HTMLEmail(
            html_body, subject=subject, body=body, to=to).send()
        self.real_send_assertions(to, body, result)
        self.assert_HTML_alternative(django_mail.outbox[0], html_body)

    def assert_HTML_alternative(self, message, html_body):
        html_alternative = message.alternatives[0]
        self.assertEqual(html_alternative[0], html_body)
        self.assertEqual(html_alternative[1], 'text/html')


# noinspection PyUnresolvedReferences
class SendMail2(SimpleTestCase):

    def setUp(self):
        NCMock = NonCallableMock

        self.subject = NCMock(spec=str)
        self.body = NCMock(spec=str)
        self.from_email = NCMock(spec=str)
        self.to = NonCallableMagicMock(spec=list)
        self.cc = NonCallableMagicMock(spec=list)
        self.bcc = NonCallableMagicMock(spec=list)
        self.reply_to = NCMock(spec=str)
        self.fail_silently = NCMock(spec=bool)
        self.auth_user = NCMock(spec=str)
        self.auth_password = NCMock(spec=str)
        self.connection = NCMock()
        self.attachments = NCMock(spec=list)
        self.headers = NonCallableMagicMock(spec=dict)

    def test_simplest_call(self):
        from lu_dj_utils.email import send_mail2

        self.assertEqual(send_mail2(), 0)

    def test_full_call(self):
        """Test the function using all the parameters with mock objects."""
        from lu_dj_utils.email import send_mail2

        (subject, body, from_email, to, cc, bcc, reply_to, fail_silently,
            auth_user, auth_password, connection, attachments, headers) = \
        (self.subject, self.body, self.from_email, self.to, self.cc, self.bcc,
            self.reply_to, self.fail_silently, self.auth_user,
            self.auth_password, self.connection, self.attachments,
            self.headers)
        send_return_value = NonCallableMock()

        with patch.object(django_mail.EmailMessage, '__init__', return_value=None) as mock_init:
            with patch.object(django_mail.EmailMessage, 'send') as mock_send:
                mock_send.return_value = send_return_value

                rvalue = send_mail2(
                    subject, body, from_email, to, cc,
                    bcc, reply_to, fail_silently, auth_user, auth_password,
                    connection, attachments, headers)

                # check EmailMessage object construction
                mock_init.assert_called_once_with(subject, body, from_email,
                    to, bcc, connection, attachments, headers, cc)
                # check the returned value is the result of EmailMessage's send method
                self.assertEqual(rvalue, send_return_value)

    def test_connection(self):
        """Check which ``connection`` object is used to create the
        :class:`EmailMessage` object.

        If ``connection`` is passed, that one is used. If not, the result of
        :func:`django.core.mail.get_connection` is used.

        """
        from lu_dj_utils.email import send_mail2

        # Case A: if 'connection' is passed, that is used
        with patch.object(django_mail.EmailMessage, '__init__', return_value=None) as mock_init:
            with patch.object(django_mail.EmailMessage, 'send'):
                send_mail2(connection=self.connection)

                mock_init.assert_called_once_with(
                    '', '', None, None, None,
                    self.connection, None, None, None)

        # Case B: else, the result of 'get_connection' is used
        # (also, the arguments of that call are checked)
        with patch('django.core.mail.get_connection') as mock_get_connection:
            mock_connection = Mock(name='connection')
            mock_get_connection.return_value = mock_connection

            with patch.object(django_mail.EmailMessage, '__init__', return_value=None) as mock_init:
                with patch.object(django_mail.EmailMessage, 'send'):
                    send_mail2()

                    mock_init.assert_called_once_with(
                        '', '', None, None, None, mock_connection, None, None, None)
                    mock_get_connection.assert_called_once_with(
                        username=None, password=None, fail_silently=False)

    def test_reply_to(self):
        from lu_dj_utils.email import send_mail2

        mock_conn = Mock(name='connection')

        with patch('django.core.mail.get_connection') as mock_get_connection:
            mock_get_connection.return_value = mock_conn

            with patch.object(django_mail.EmailMessage, '__init__', return_value=None) as mock_init:
                with patch.object(django_mail.EmailMessage, 'send'):

                    send_mail2(headers=self.headers)
                    mock_init.assert_called_once_with(
                        '', '', None, None, None,
                        mock_conn, None, self.headers, None)
                    self.assertFalse(self.headers.__setitem__.called)

                    mock_init.reset_mock()
                    self.headers.reset_mock()

                    send_mail2(reply_to=self.reply_to, headers=self.headers)
                    mock_init.assert_called_once_with(
                        '', '', None, None, None,
                        mock_conn, None, self.headers, None)
                    self.headers.__setitem__.assert_called_once_with(
                        'Reply-To', self.reply_to)

                    mock_init.reset_mock()
                    self.headers.reset_mock()

                    send_mail2(reply_to=self.reply_to)
                    mock_init.assert_called_once_with('', '', None, None, None,
                        mock_conn, None, {'Reply-To': self.reply_to}, None)
                    self.assertFalse(self.headers.__setitem__.called)

    def test_real_call(self):
        from lu_dj_utils.email import send_mail2

        _reset_test_outbox()
        outbox = django_mail.outbox

        subject = 'hello!'
        body = 'my email body'
        to = ['a@a.cl', 'x@xx.com']

        self.assertEqual(len(outbox), 0)
        send_mail2(subject=subject, body=body, to=to)
        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].to, to)
        self.assertIn(body, outbox[0].body)

    def test_invalid_addresses(self):
        from lu_dj_utils.email import send_mail2

        _reset_test_outbox()
        outbox = django_mail.outbox

        subject = 'hello!'
        body = 'my email body'
        invalid_addresses = ['', ' ', 'x', 'x@x']
        not_str_addresses = [None, -15]

        # empty 'to' list: sends nothing
        send_mail2(subject=subject, body=body, to=[])
        self.assertEqual(len(outbox), 0)

        # Even though the addresses are invalid, the messages to them ARE SENT
        for address in invalid_addresses:
            temp = len(outbox)
            send_mail2(subject=subject, body=body, to=[address])
            self.assertEqual(len(outbox), temp + 1)

        # if address contains a newline, BadHeaderError(ValueError) is raised
        with self.assertRaises(ValueError):
            send_mail2(subject=subject, body=body, to=['\n'])

        # if address is not a string, ValueError is raised
        for address in not_str_addresses:
            with self.assertRaises(ValueError):
                send_mail2(subject=subject, body=body, to=[address])


class SendTemplatedMailTest(TestCase):

    def setUp(self):
        self.valid_address = 'pedro@perez.cl'
        self.invalid_address = 'pedro@perez'

        self.username = NonCallableMock()
        self.context = dict(nombre=self.username)

        # these templates must exist
        self.subject_name = 'email1_subject.txt'
        self.body_name = 'email1_body.txt'
        self.html_body_name = 'email1_body.html'

    def test_enviar_correo_with_valid_address(self):
        address = self.valid_address
        self.assertTrue(self._send_default(address))

    def test_enviar_correo_with_invalid_address(self):
        """It **will** send the message, even if the address is invalid."""
        address = self.invalid_address
        self.assertTrue(self._send_default(address))

    def test_enviar_correo(self):
        _reset_test_outbox()
        outbox = django_mail.outbox

        address = self.valid_address

        # there is no emails before sending the email
        self.assertEqual(len(outbox), 0)

        # we trigger the action that send the email
        self._send_default(address)

        # email actually sent?
        self.assertEqual(len(outbox), 1)

        # the email is sent to the right destination
        self.assertEqual(outbox[0].to, [address])
        self.assertEqual(outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

    def test_html(self):
        from lu_dj_utils.email import render_to_string, send_templated_mail

        _reset_test_outbox()
        outbox = django_mail.outbox
        self.assertEqual(len(outbox), 0)

        email_address = self.valid_address

        result = send_templated_mail(
            self.context, self.subject_name, self.body_name,
            self.html_body_name, to=[email_address])
        self.assertTrue(result)
        self.assertEqual(len(outbox), 1)

        message = outbox[0]
        html_body = render_to_string(self.html_body_name, self.context)
        html_alternative = message.alternatives[0]
        self.assertEqual(html_alternative[0], html_body)
        self.assertEqual(html_alternative[1], 'text/html')

    def _send_default(self, email_address):
        from lu_dj_utils.email import send_templated_mail

        return send_templated_mail(
            self.context, self.subject_name, self.body_name, to=[email_address])


class Functions(SimpleTestCase):

    # noinspection PyTypeChecker
    def test_set_header_reply_to(self):
        from lu_dj_utils.email import set_header_reply_to

        func = set_header_reply_to

        email1 = NonCallableMock(spec=str)
        email2 = NonCallableMock(spec=str)

        self.assertEqual(func(None, email1), {'Reply-To': email1})
        self.assertEqual(func({}, email1), {'Reply-To': email1})
        self.assertEqual(func({'Reply-To': email1}, email2), {'Reply-To': email2})
        self.assertIsNone(func(None, None))
        self.assertEqual(func({}, None), {})


def _reset_test_outbox():
    """Empty the outbox manually.

    Apparently there is a bug in TestCase because the test runner should clear
    the contents of the test email outbox at the start of each test case,
    and it is not doing that.

    https://docs.djangoproject.com/en/dev/topics/testing/overview/#emptying-the-test-outbox

    """
    django_mail.outbox = []
