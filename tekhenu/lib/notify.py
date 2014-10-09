"""
notify.py: Notify admin on exceptions

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

import logging
import datetime

from bottle import request

from google.appengine.api import mail


def send_notification(subject, body):
    """ Send notification email to configured admin emails """
    admin = request.app.config['notify.admin']
    sender = request.app.config['notify.sender']
    prefix = request.app.config.get('notify.subject_prefix')
    if prefix:
        subject = prefix + ' ' + subject
    mail.send_mail(sender, admin, subject, body)


def format_dict(d):
    """ Format dictionary as human-readable text """
    s = '\n'
    for k in d.keys():
        s += '    %s: ' % k
        try:
            v = d.getall(k)
            if len(v) > 1:
                s += ', '.join(v)
            elif len(v) == 1:
                s += v[0] and ('%r' % v[0]) or '(empty or None)'
            else:
                s += '(empty or None)'
        except AttributeError:
            try:
                v = d.get(k)
                if isinstance(v, (list, tuple)):
                    s += ', '.join(v)
                else:
                    s += v and ('%r' % v) or 'None'
            except KeyError:
                s += 'KeyError'
        except KeyError:
            s += 'KeyError'
        s += '\n'
    return s


def handle_error(exc, extras={}):
    """ Format error report and send out a message """
    msgs = []
    msgs.append("TIMESTAMP: %s" % datetime.datetime.utcnow())
    msgs.append("ERROR: %s" % exc.exception)
    msgs.append("PATH: %s %s" % (request.method, request.fullpath))
    msgs.append("PARAMS: %s" % format_dict(request.params))
    msgs.append("HEADERS: %s" % format_dict(request.headers))
    msgs.append("COOKIES: %s" % format_dict(request.cookies))
    msgs.append("IS XHR: %s" % 'yes' if request.is_xhr else 'no')
    msgs.append("IP: %s" % request.remote_addr)
    msgs.append("\n%s\n" % exc.traceback)
    if extras:
        msgs.append("EXTRA INFORMATION: %s" % format_dict(extras))
    subject = "'%s' at %s" % (exc.exception, request.path)
    send_notification(subject, '\n'.join(msgs))
    logging.error("Unhandled exception '%s'\n\n%s",
                  exc.exception, exc.traceback)
