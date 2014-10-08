"""
content.py: Content details page

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals, division

from bottle_utils import csrf
from bottle_utils.i18n import i18n_path
from google.appengine.ext import ndb
from bottle_utils.i18n import lazy_gettext as _
from bottle import view, default_app, request, response, redirect, abort

from db.models import Content, Event


app = default_app()

PREFIX = '/content'


def get_content_or_404(id):
    """
    Return content entity or abort with HTTP 404 if none is found.

    :param id:  id of the content
    :returns:   ``Content`` object
    """
    content = Content.get_cached(id)
    if not content:
        abort(404)
    return content


@app.get(PREFIX + '/:id')
@csrf.csrf_token
@view('content_details', errors={}, Content=Content)
def show_content_details(id):
    content = get_content_or_404(id)
    if request.params.get('edit') == '1':
        vals = dict(title=content.title, license=content.license)
    else:
        vals = {}
    return dict(content=content, vals=vals)


@app.post(PREFIX + '/:id')
@csrf.csrf_protect
@view('content_details', Content=Content)
def update_content_details(id):
    content = get_content_or_404(id)

    if not content.is_editable:
        # Translators, shown when content is not editable (it's on air, etc)
        response.flash(_('This content is not editable'))
        redirect(i18n_path(content.path))

    errors = {}

    title = request.forms.getunicode('title', '').strip()
    license = request.forms.get('license') or None

    if not content.title and not title:
        errors['title'] = _('Title cannot be blank')

    if license and license not in Content.LICENSE_CHOICES:
        errors['license'] = _('Please select a license from provided choices')

    if not errors:
        to_put = []
        if title and content.title != title:
            content.title = title
            to_put.append(Event.create(Event.TITLE, content.key))
        if license and content.license != license:
            content.license = license
            to_put.append(Event.create(Event.LICENSE, content.key))
        if to_put:
            # If we have events in to_put list, we also need to put the content
            to_put.append(content)
        ndb.put_multi(to_put)
        response.flash(_('Content has been updated'))
        redirect(content.path)

    return dict(vals=request.forms, errors=erorrs, content=content)


@app.post(PREFIX + '/:id/votes/')
@csrf.csrf_protect
def update_content_details(id):
    to_put = []
    content = get_content_or_404(id)
    ref_path = i18n_path(request.forms.get('back', content.path))

    if not content.is_editable:
        response.flash(_('Voting is disabled for content that is being '
                         'broadcast'))
        redirect(ref_path)

    vote = request.forms.get('vote')

    if vote not in ['up', 'down']:
        response.flash(_('There was a problem with the request. Please try '
                         'again later.'))
        redirect(ref_path)

    if vote == 'up':
        content.upvotes += 1
        to_put.append(Event.create(Event.UPVOTE, content.key))
    elif vote == 'down':
        content.downvotes += 1
        to_put.append(Event.create(Event.DOWNVOTE, content.key))
    to_put.append(content)
    ndb.put_multi(to_put)
    redirect(ref_path)
