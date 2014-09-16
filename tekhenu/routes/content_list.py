"""
content_list.py: Content list request handler, and suggestion form handler

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

import logging

from bottle import view, default_app, request, response, redirect
from bottle_utils import csrf
from bottle_utils.i18n import lazy_gettext as _

from db.models import Content

app = default_app()

PREFIX = '/'


def get_content_list():
    """
    Create a query over ``Content`` objects using query string parameters.

    :returns:   ``google.appengine.ext.ndb.Query`` object
    """
    return Content.get_recent()


@app.get(PREFIX)
@csrf.csrf_token
@view('content_list', vals={}, errors={}, licenses=Content.LICENSES)
def show_content_list():
    """
    Show a list of 10 last-updated pieces of content and a suggestion form.
    """
    logging.debug(list(get_content_list()))
    return dict(content=get_content_list())


@app.post(PREFIX)
@csrf.csrf_protect
@view('content_list', licenses=Content.LICENSES)
def add_content_suggestion():
    """
    Handle a content suggestion request.
    """
    url = request.forms.get('url', '').strip()
    license = request.forms.get('license')

    errors = {}
    if license:
        license = license.strip().upper()
        if license not in Content.LICENSE_CHOICES:
            # Translators, used as error message on failure to submit
            # suggestion
            errors['license'] = _('Please select a license from provided '
                                  'choices')
    else:
        license = None

    if not url:
        # Translators, used as error message on failure to submit suggestion
        errros['url'] = _('Please type in a valid URL')

    if not errors:
        try:
            content = Content.create(url=url, license=license)
            logging.info("Created content for '%s' (real url: '%s')", url,
                         content.url)
            response.flash(_('Your suggestion has been added'))
            redirect(content.path)
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
            errors['url'] = _('The page is hosted on a server that does not '
                              'allow us to reach it')
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

    return dict(vals=request.forms, errors=errors, content=get_content_list())

