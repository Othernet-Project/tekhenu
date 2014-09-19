"""
broadcast.py: Broadcast management features

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals, division

import math

from bottle_utils import csrf
from bottle_utils.i18n import i18n_path
from google.appengine.ext import ndb
from bottle_utils.i18n import lazy_gettext as _
from bottle import view, default_app, request, response, redirect, abort

from db.models import Content

from . import QueryResult

app = default_app()

PREFIX = '/broadcast'
ALLOWED_PER_PAGE = [10, 20, 50]
PER_PAGE_CHOICES = [(str(x), str(x)) for x in ALLOWED_PER_PAGE]
VOTE_CHOICES = (
    # Translators, used in votes sorting order drop-down
    ('asc', _('highest first')),
    # Translators, used in votes sorting order drop-down
    ('desc', _('lowest first')),
    # Translators, used in votes sorting order drop-down
    ('cont', _('controversial')),
)
LICENSE_CHOICES = (
    # Translators, used as choice in license drop-down in broadcast list
    ('NONE', _('No license')),
    # Translators, used as choice in license drop-down in broadcast list
    ('FREE', _('Any free')),
    # Translators, used as choice in license drop-down in broadcast list
    ('NONFREE', _('Any non-free')),
) + Content.LICENSES[1:]


def get_content_list():
    """
    Create a query over ``Content`` objects using query string parameters.

    :param per_page:    number of items to return per page
    :returns:           ``QueryResult`` object
    """
    search = request.params.getunicode('q', '').strip()
    archive = request.params.get('archive')
    license = request.params.get('license')
    votes = request.params.get('votes')
    try:
        page = int(request.params.get('p', '1'))
    except ValueError:
        page = 1
    try:
        per_page = int(request.params.get('pp', '10'))
    except ValueError:
        per_page = 10
    if per_page not in ALLOWED_PER_PAGE:
        per_page = 10

    q = Content.query()
    if search:
        keywords = Content.get_keywords(search)
        q = q.filter(ndb.AND(*[Content.keywords == kw for kw in keywords]))
    if archive:
        q = q.filter(Content.archive == archive)
    if license:
        if license == 'NONE':
            q = q.filter(Content.license == None)
        elif license == 'FREE':
            q = q.filter(Content.license.IN(Content.FREE_LICENSES))
        elif license == 'NONFREE':
            q = q.filter(Content.license.IN(Content.NONFREE_LICENSES))
        else:
            q = q.filter(Content.license == license)
    if votes == 'asc':
        q = q.order(+Content.votes)
    elif votes == 'desc':
        q = q.order(-Content.votes)
    elif votes == 'cont':
        q = q.filter(ndb.AND(
            Content.votes_ratio <= 1.2, Content.votes_ratio >= 0.8))
        q = q.order(-Content.votes_ratio)
    q = q.order(-Content.updated)

    count = q.count()

    if not count:
        return QueryResult([], count, 1, 1)

    npages = int(math.ceil(count / per_page))

    if page * per_page > count:
        page = npages

    offset = int(per_page * (page - 1))
    items = q.fetch(per_page, offset=offset)
    return QueryResult(items, count, per_page, page)


def get_common_context():
    """
    Return base context for handlers in this module
    """
    sel = request.params.get('select', '0') == '1'
    return dict(per_page=PER_PAGE_CHOICES, votes=VOTE_CHOICES,
                licenses=LICENSE_CHOICES, content=get_content_list(),
                vals=request.params, sel=sel, css='admin')


@app.get(PREFIX)
def redirect_to_correct_url():
    redirect(i18n_path(PREFIX + '/'))


@app.get(PREFIX + '/')
@view('admin_list', errors={}, Content=Content)
@csrf.csrf_token
def show_content_list():
    return get_common_context()


def finish_with_message(message):
    response.flash(message)
    redirect(i18n_path(PREFIX + '/'))


@app.post(PREFIX + '/')
@view('admin_list', Content=Content)
def handle_content_edits():
    sel = request.params.get('select', '0') == '1'
    to_put = []

    selection = request.forms.getall('selection')
    if not selection:
        # Translators, used as error message on broadcast page when there is
        # no selection to operate on
        finish_with_message(_('No content selected'))

    keys = [ndb.Key('Content', key) for key in selection]
    action = request.forms.get('action')

    if action == 'status':
        archive = request.forms.get('archive')
        if archive not in Content.ARCHIVE_CHOICES:
            finish_with_message(_('Invalid request'))
        for content in ndb.get_multi(keys):
            if content.archive != archive:
                content.archive = archive
                to_put.append(content)
        ndb.put_multi(to_put)
    elif action == 'delete':
        ndb.delete_multi(keys)
    finish_with_message(_('Broadcast data updated'))

