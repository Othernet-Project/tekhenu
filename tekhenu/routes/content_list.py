"""
content_list.py: Content list request handler, and suggestion form handler

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

from bottle import view, default_app

from db.models import Content


app = default_app()


PREFIX = '/'


@app.get(PREFIX)
@view('content_list')
def show_content_list():
    # Retrieve 10 most recent content
    return dict(content=Content.get_recent())

