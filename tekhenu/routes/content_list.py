"""
content_list.py: Content list request handler, and suggestion form handler

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals, division

import math
import logging
from urlparse import urlparse

from bottle_utils import csrf
from bottle_utils.i18n import i18n_path
from google.appengine.ext import ndb
from bottle_utils.i18n import lazy_gettext as _
from bottle import view, default_app, request, response, redirect

from db.models import Content

from . import QueryResult

app = default_app()

PREFIX = '/'


def get_content_list(per_page=20):
    """
    Create a query over ``Content`` objects using query string parameters.

    :param per_page:    number of items to return per page
    :returns:           ``QueryResult`` object
    """
    search = request.params.getunicode('q', '').strip()
    status = request.params.get('status')
    license = request.params.get('license')
    votes = request.params.get('votes')
    page = int(request.params.get('p', '1'))

    q = Content.query()
    if search:
        keywords = Content.get_keywords(search)
        if len(keywords) > 1:
            q = q.filter(ndb.AND(*[Content.keywords == kw for kw in keywords]))
        else:
            q = q.filter(Content.keywords == keywords[0])
    if status:
        q = q.filter(Content.status == status)
    if license == 'free':
        q = q.filter(Content.is_free == True)
    elif license == 'nonfree':
        q = q.filter(Content.is_free == False)
    elif license == 'unknown':
        q = q.filter(Content.license == None)
    if votes == 'asc':
        q = q.order(+Content.votes)
    elif votes == 'desc':
        q = q.order(-Content.votes)
    q = q.order(-Content.updated)

    count = q.count()

    if not count:
        return QueryResult([], count, 1, 1)

    npages = int(math.ceil(count / per_page))

    if page * per_page > count:
        page = npages

    offset = int(per_page * (page - 1))
    return QueryResult(q.fetch(per_page, offset=offset), count, page, npages)


@app.get(PREFIX)
@csrf.csrf_token
@view('content_list', errors={}, Content=Content)
def show_content_list():
    """
    Show a list of 10 last-updated pieces of content and a suggestion form.
    """
    return dict(vals=request.params, content=get_content_list())


@app.post(PREFIX)
@csrf.csrf_protect
@view('content_list', Content=Content)
def add_content_suggestion():
    """
    Handle a content suggestion request.
    """
    # TODO: Handle Unicode URLs
    url = Content.validate_url(request.forms.get('url', ''))
    license = request.forms.get('license') or None

    errors = {}

    if not url:
        # Translators, used as error message on failure submit suggestion
        errors['url'] = _('This URL is invalid')

    if license:
        license = license.strip().upper()
        if license not in Content.LICENSE_CHOICES:
            # Translators, used as error message on failure to submit
            # suggestion
            errors['license'] = _('Please select a license from provided '
                                  'choices')

    if not url:
        # Translators, used as error message on failure to submit suggestion
        errors['url'] = _('Please type in a valid URL')

    if not errors:
        try:
            content = Content.create(url=url, license=license)
            logging.info("Created content for '%s' (real url: '%s')", url,
                         content.url)
            response.flash(_('Your suggestion has been added'))
            redirect(i18n_path(content.path))
        except Content.InvalidURLError as err:
            logging.debug("URL error while parsing '%s': %s", url, err)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('This URL is invalid')
        except Content.FetchError as err:
            logging.debug("Fetch error while parsing '%s': %s (%s)",
                          url, err, err.error)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('The page at specified URL does not exist or '
                              'the domain cannot be reached.')
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
        except Exception as err:
            logging.debug("Unknown error fetching '%s': %s", url, err)
            # Translators, used as error message on failure submit suggestion
            errors['url'] = _('There was an unknown error with the URL')

    return dict(vals=request.forms, errors=errors, Content=Content,
                content=get_content_list())

