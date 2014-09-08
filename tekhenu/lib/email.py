"""
email.py: Wrapper for sending email messages

Copyright 2014 Outernet Inc <hello@outernet.is>
All rights reserved.
"""

from __future__ import unicode_literals, print_function

import logging

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import mandrill
from bottle import template, request


def send_multiple(to_list, subject, text=None, html=None, data={},
                  mandrill_args={'preserve_recipients': False},
                  use_template=None):
    """ Sends out text/HTML email with specified templates """
    conf = request.app.config

    # Set up mandrill API access
    mandrill_client = mandrill.Mandrill(conf['mandrill.key'])

    # Prepare data for the email
    parsed = urlparse(request.url)
    data['protocol'] = parsed.scheme
    data['host'] = parsed.netloc
    data['host_url'] = parsed.scheme + '://' + parsed.netloc

    # Construct message object
    message = mandrill_args
    message.update({
        'subject': subject,
        'from_name': conf['mandrill.sender_name'],
        'from_email': conf['mandrill.sender_email'],
        'to': [dict(email=e[0], name=e[1], type='to') for e in to_list]
    })

    logging.debug("Prepared message: %s" % message)

    if text:
        message['text'] = ''.join(template(text, **data))
    if html:
        message['html'] = ''.join(template(html, **data))

    if use_template:
        try:
            return mandrill_client.messages.send_template(
                template=use_template, message=message, async=False)
        except Exception, e:
            logging.exception('Error sending email: %s' % e)
            return None
    else:
        try:
            return mandrill_client.messages.send(message=message, async=False)
        except Exception, e:
            logging.exception('Error sending email: %s' % e)
            return None


def send_mail(to, subject, text=None, html=None, to_name='',
              data={}, mandrill_args={'preserve_recipients': False},
              use_template=None):
    """ Send out text/HTML email with specified templates """
    return send_multiple([(to, to_name)], subject, text, html, data,
                         mandrill_args, use_template)

