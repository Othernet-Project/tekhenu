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

PREFIX = '/content'

ALLOWED_PER_PAGE = [10, 20, 50]


def get_content_list(per_page=10):
    """
    Create a query over ``Content`` objects using query string parameters.

    :param per_page:    number of items to return per page
    :returns:           ``QueryResult`` object
    """
    # TODO: This is just a basic list
    q = Content.query()
    count = q.count()
    pages = math.floor(count / per_page)
    items = q.fetch(per_page)
    return QueryResult(items, count, 1, per_page)


@app.get(PREFIX)
def redirect_to_correct_url():
    redirect(i18n_path(PREFIX + '/'))


@app.get(PREFIX + '/')
@view('admin_list', errors={}, Content=Content)
@csrf.csrf_token
def show_content_list():
    sel = request.params.get('select', '0') == '1'
    return dict(content=get_content_list(), sel=sel, vals=request.query)
