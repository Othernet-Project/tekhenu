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
sys.path.insert(0, PACKAGE_DIR)

import bottle

from bottle_utils import i18n, flash, meta, html

# Setup
app = bottle.default_app()
app.config.load_config(in_package('tekhenu.ini'))
bottle.debug(app.config['debug'] == 'yes')
app.install(flash.message_plugin)
bottle.TEMPLATE_PATH.insert(0, in_package('views'))
bottle.BaseTemplate.defaults.update({
    'meta': meta.Metadata(title='Tekhenu'),
    'request': bottle.request,
    'message': flash.get_message(),
    'h': html
})

# Set up routes

from routes import content_list

# Set up i18n
try:
    app = i18n.I18NPlugin(
        app,
        langs=LOCALES,
        default_locale=DEFAULT_LOCALE,
        locale_dir=in_package('locales'))
except IOError:
except IOError as err:
    logging.warning("Translations disabled due to loading error: %s" % err)

