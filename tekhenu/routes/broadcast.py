"""
broadcast.py: Broadcast management features

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals, division

import csv
import math
import logging
from datetime import datetime

from bottle_utils import csrf
from google.appengine.ext import ndb
from bottle_utils.i18n import i18n_path
from google.appengine.ext.deferred import defer
from bottle_utils.i18n import lazy_gettext as _
from bottle import view, default_app, request, response, redirect, abort

from db.models import Content, Event

from . import QueryResult

app = default_app()

PREFIX = '/broadcast'
ALLOWED_PER_PAGE = [20, 50, 100]
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
NOTES_CHOICES = (
    ('1', _('With notes')),
    ('0', _('Without notes')),
)


def get_content_list():
    """
    Create a query over ``Content`` objects using query string parameters.

    :param per_page:    number of items to return per page
    :returns:           ``QueryResult`` object
    """
    search = request.params.getunicode('q', '').strip()
    archive = request.params.get('archives')
    license = request.params.get('license')
    votes = request.params.get('votes')
    notes = request.params.get('notes')
    try:
        page = int(request.params.get('p', '1'))
    except ValueError:
        page = 1
    try:
        per_page = int(request.params.get('pp', '20'))
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
    if notes == '1':
        q = q.filter(Content.has_notes == True)
    elif notes == '0':
        q = q.filter(Content.has_notes == False)
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


def get_common_context(extra_context={}):
    """
    Return base context for handlers in this module
    """
    sel = request.params.get('select', '0') == '1'
    ctx = dict(per_page=PER_PAGE_CHOICES, votes=VOTE_CHOICES,
               notes=NOTES_CHOICES, licenses=LICENSE_CHOICES,
               content=get_content_list(), vals=request.params, sel=sel,
               css='admin', total_count=Content.query().count())
    ctx.update(extra_context)
    return ctx


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
        archive = request.forms.get('archive') or None
        if archive not in Content.ARCHIVE_CHOICES:
            finish_with_message(_('Invalid request'))
        for content in ndb.get_multi(keys):
            if content.archive != archive:
                content.archive = archive
                if archive == None:
                    to_put.append(Event.create(Event.UNBROADCAST, content.key))
                else:
                    to_put.append(Event.create(Event.BROADCAST, content.key))
                to_put.append(content)
        ndb.put_multi(to_put)
    elif action == 'delete':
        ndb.delete_multi(keys)
    finish_with_message(_('Broadcast data updated'))


@app.post(PREFIX + '/new/')
@csrf.csrf_protect
@view('admin_list', Content=Content)
def handle_manual_add():
    url = request.params.get('url', '').strip()
    title = request.params.getunicode('title', '').strip()
    license = request.params.get('license') or None
    archive = request.params.get('archive') or None

    errors = {}
    if not url:
        # Translators, used as error message on failure to submit content
        errors['url'] = _('Please type in a valid URL')

    if not errors:
        try:
            content = Content.create(url=url, license=license, title=title,
                                     archive=archive)
            logging.info("Created content for '%s' (real url: '%s')", url,
                         content.url)
            response.flash(_('Content has been added'))
            redirect(i18n_path(PREFIX + '/'))
        except Content.InvalidURLError as err:
            logging.debug("URL error while parsing '%s': %s", url, err)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('This URL is invalid')
        except Content.FetchError as err:
            logging.debug("Fetch error while parsing '%s': %s (%s)",
                          url, err, err.error)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('The page at specified URL does not exist')
        except Content.NotAllowedError as err:
            logging.debug("Access error while parsing '%s': %s", url, err)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('The page must be accessible to robots')
        except Content.ContentError as err:
            logging.debug("Content error while parsing '%s': %s (%s)", url,
                          err, err.error)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('The content on the page could not be '
                              'understood, please provide and URL to a valid '
                              'web page')
        except Content.BotError as err:
            logging.exception("Error while fetching '%s':  %s", url, err)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('There was an unknown error with the URL')

    return get_common_context(dict(vals=request.forms, errors=errors))


def bulk_create(rows, check=False):
    content = []
    logging.info('Enqueued bulk import with %s rows', len(rows))
    for url, title, license, archive, partner, timestamp, replaces, notes in rows:
        ts = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %Z')
        try:
            content.append(Content.create(
                url=url,
                title=title,
                license=license or None,
                archive=archive or None,
                created=ts,
                replaces=replaces or None,
                notes=notes or None,
                partner=partner or None,
                is_partner=partner != '',
                check_url=check and not url.startswith('outernet://'),
                override_timestamp=ts,
            ))
        except Exception as err:
            logging.exception("Error while adding content with URL '%s'", url)
    logging.debug('Successfully importent following:\n\n%s',
                  '\n'.join([c.key.id() for c in content]))


@app.post(PREFIX + '/bulk/')
@csrf.csrf_protect
@view('admin_list', Content=Content)
def handle_bulk_create():
    errors = {}
    data = request.files.get('data')
    check = request.forms.get('check') == 'yes'

    if not data:
        errors['data'] = _('Please upload a file')

    if not errors:
        to_put = []
        rows = csv.reader(data.file)
        defer(bulk_create, [r for r in rows], check)
        finish_with_message(_('Bulk loading has been enqueued.'))

    return get_common_context(dict(vals=request.params, errors=errors))
