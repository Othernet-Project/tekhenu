"""
routes.py: Common functionality for all routes

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

from collections import namedtuple

QueryResult = namedtuple('QueryResult', ['items', 'count', 'page', 'pages'])
