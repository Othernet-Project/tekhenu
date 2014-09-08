"""
main.py: Main application module

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

import os
import sys
import logging

__version__ = '0.1a1'

# Set up directory paths and constants

PACKAGE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(PACKAGE_DIR)
LOCALES = (
    ('en', 'English'),
)
DEFAULT_LOCALE = 'en'

def in_root(path):
    return os.path.join(PROJECT_DIR, os.path.normpath(path))

def in_package(path):
    return os.path.join(PACKAGE_DIR, os.path.normpath(path))


# Set up vendors so we can import dependencies
sys.path.insert(0, in_root('vendor'))

import bottle

from bottle_utils import i18n, flash

# Setup
app = bottle.default_app()
app.config.load_config(in_package('tekhenu.ini'))
bottle.debug(app.config['debug'] == 'yes')
app.install(flash.message_plugin)

# Set up i18n
try:
    app = i18n.I18NPlugin(
        app,
        langs=LOCALES,
        default_locale=DEFAULT_LOCALE,
        locale_dir=in_package('locales'))
except IOError:
    logging.warning('Translations disabled due to loading error')

