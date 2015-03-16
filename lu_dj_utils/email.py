# coding: utf-8
"""Email-related utilities to create, render and send messages.

Source: lookup_www.common.utils.mail (with some edition).

"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

import django.core.mail
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


class PlainEmail(object):

    """Friendly wrapper over :class:`django.core.mail.EmailMessage`

    .. note::
        The only public attribute is :attr:`connection` because it can be
        changed safely after instantiation.

    """

    django_mail_class = django.core.mail.EmailMessage

    def __init__(
            self, subject='', body='', from_email=None, to=None, cc=None,
            bcc=None, reply_to=None, connection=None, attachments=None,
            headers=None):

        self._subject = subject
        self._body = body

        self._from_email = from_email
        self._to = to
        self._cc = cc
        self._bcc = bcc

        self.connection = connection
        self._attachments = attachments

        headers = set_header_reply_to(headers, reply_to)
        self._headers = headers

    def create_message(self):
        """Create an email message.

        :return: email message object
        :rtype: :attr:`django_mail_class`

        """
        return self.django_mail_class(
            subject=self._subject,
            body=self._body,
            from_email=self._from_email,
            to=self._to,
            bcc=self._bcc,
            connection=self.connection,
            attachments=self._attachments,
            headers=self._headers,
            cc=self._cc)

    def send(self):
        """Create the email message and send it.

        :return: the number of email messages sent (return value of :meth:`EmailMessage.send`)
        :rtype: int

        """
        message = self.create_message()
        return message.send()


class HTMLEmail(PlainEmail):

    """Customization of :class:`PlainEmail` to send a multipart HTML email."""

    django_mail_class = django.core.mail.EmailMultiAlternatives
    _EMAIL_ALTERNATIVE_MIME_TYPE = 'text/html'

    def __init__(self, html_body, *args, **kwargs):
        super(HTMLEmail, self).__init__(*args, **kwargs)
        self._html_body = html_body

    def create_message(self):
        message = super(HTMLEmail, self).create_message()
        message.attach_alternative(self._html_body, self._EMAIL_ALTERNATIVE_MIME_TYPE)
        return message


def send_mail2(
        subject='', body='', from_email=None, to=None, cc=None, bcc=None,
        reply_to=None, fail_silently=False, auth_user=None,
        auth_password=None, connection=None, attachments=None, headers=None):
    """Combination of :func:`django.core.mail.send_mail` and
    :class:`django.core.mail.EmailMessage`.

    The original ``send_mail`` was too limited and kind of deprecated ('The API
    for this method is frozen'). This function augments it.

    These are the parameters differences:
    * ``message`` renamed to ``body`` (compliant with ``EmailMessage``)
    * ``recipient_list`` renamed to ``to`` (compliant with ``EmailMessage``)
    * added ``cc``, ``bcc``, ``reply_to``, ``attachments`` and ``headers``
    * set default values for ``subject``, ``message``/``body``, ``from_email``,
        ``recipient_list``/``to``

    Check parameters definitions at :class:`django.core.mail.EmailMessage`
    and :func:`django.core.mail.get_connection`.

    :return: the number of email messages sent (return value of
        :meth:`EmailMessage.send`)

    .. warning::
        All passed email addresses must be validated beforehand. For example,
        all these values **WILL** result in a message being sent
        (i.e. return value will be ``> 0``:
        ``['', ' ', 'x', 'x@x']``
        Other values may raise exceptions e.g. ValueError and
        its subclass BadHeaderError.

    .. warning::
        Do not confuse ``from_email`` with ``auth_user``.

    """
    # 1. basic validation of given addresses lists/tuples
    # 2. get the connection
    # 3. set header 'Reply-To' (if given)
    # 4. create the EmailMessage object
    # 5. send it

    if to is not None:
        validate_addresses(to)
    if cc is not None:
        validate_addresses(cc)
    if bcc is not None:
        validate_addresses(bcc)

    if connection is None:
        connection = django.core.mail.get_connection(
            username=auth_user,
            password=auth_password,
            fail_silently=fail_silently)

    headers = set_header_reply_to(headers, reply_to)
    message = django.core.mail.EmailMessage(
        subject, body, from_email, to, bcc, connection, attachments, headers, cc)

    return message.send()


def send_templated_mail(
        context, subject_template_name, body_template_name, html_body_template_name=None,
        **kwargs):
    """Send mail by rendering subject and body templates using ``context``.

    The message will be a plain text or HTML multipart email depending on
    whether ``html_body_template_name`` is None or not.

    ``kwargs`` is passed directly to :class:`PlainEmail`, allowing full
    customization of the email creation (e.g. to, cc, bcc, headers, attachments)
    and send (i.e. connection object) process.

    :param context: context data used to render the templates
    :type context: :class:`dict`
    :param subject_template_name: the name of the subject template
    :type subject_template_name: string
    :param body_template_name: the name of the plain-text body template
    :type body_template_name: string
    :param html_body_template_name: if a multipart HTML email is desired, the
        name of the HTML body template; None otherwise
    :type html_body_template_name: string or None
    :return: True if at least one message is sent successfully; False otherwise
    :rtype: bool

    .. warning::
        All passed email addresses **must** be validated beforehand.

    .. warning::
        ``to``, ``cc`` and ``bcc`` arguments must be **iterables** of strings,
        not plain strings, no matter if their length is 1.

    """
    #noinspection PyBroadException
    try:
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(body_template_name, context)
        if html_body_template_name is None:
            html_body = None
        else:
            html_body = render_to_string(html_body_template_name, context)
    except Exception:
        logger.exception(
            "Failed to render body or subject.\nTemplate names: (%s, %s, %s)\nContext: %s" %
            (subject_template_name, body_template_name, html_body_template_name, context))
        return False

    #noinspection PyBroadException
    try:
        if html_body is None:
            message = PlainEmail(subject=subject, body=body, **kwargs)
        else:
            message = HTMLEmail(html_body, subject=subject, body=body, **kwargs)

        result = message.send()
        if not result >= 1:
            logger.error("No mail was sent.\nsubject: %s\nbody: %s\nkwargs: %s" %
                         (subject, body, kwargs))
            return False
    except Exception:
        logger.exception("send_templated_mail failed.\nsubject: %s\nbody: %s\nkwargs: %s" %
                         (subject, body, kwargs))
        return False
    return True


def set_header_reply_to(headers, reply_to):
    """Set ``reply_to`` as email header ``'Reply-To'``.

    :param headers: email headers
    :type headers: dict or None
    :param reply_to: email address to set as header ``'Reply-To'``
    :type reply_to: basestring or None
    :return: updated headers, if ``reply_to`` is not None
    :rtype: dict, if ``reply_to`` is not None; unknown otherwise

    >>> set_header_reply_to(None, 'a@a.com')
    {'Reply-To': 'a@a.com'}
    >>> set_header_reply_to({}, 'a@a.com')
    {'Reply-To': 'a@a.com'}
    >>> set_header_reply_to({'Reply-To': 'a@a.com'}, 'b@b.com')
    {'Reply-To': 'b@b.com'}
    >>> set_header_reply_to(None, None)
    None
    >>> set_header_reply_to({}, None)
    {}

    """
    if reply_to is not None:
        if headers is None:
            headers = {'Reply-To': reply_to}
        else:
            headers['Reply-To'] = reply_to
    return headers


def validate_addresses(addresses):
    """Check that ``addresses`` can be joined in a single string.

    :param addresses: email addresses
    :rtype: list or tuple
    :raises: ValueError if ``addresses`` couldn't be joined

    """
    addresses = list(addresses)
    try:
        ', '.join(addresses)
    except TypeError:
        raise ValueError("Email addresses couldn't be joined in a single string: %s\n"
                         "Hint: probably one of them is not a string" % addresses)
