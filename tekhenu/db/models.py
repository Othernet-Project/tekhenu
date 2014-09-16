"""
models.py: Application models

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

import urllib2
import hashlib
import logging

from bs4 import BeautifulSoup
from bottle_utils.i18n import lazy_gettext as _

from lib.bottle_ndb import ndb, CachedModelMixin, UrlMixin, TimestampMixin
from lib.tekhenubot import get_url_info, BotError


class Content(CachedModelMixin, UrlMixin, TimestampMixin, ndb.Model):
    """
    Stores content information. This class is used to store content information
    in GAE's Datastore.

    The content information includes the URL of the page, page title, licensing
    information, and metadata about the broadcast (archive to which the page
    has been broadcast, etc).
    """

    cache_time = 18000  # 5 hours in seconds

    #: List of license keys and full license names.
    LICENSES = (
        # Translators, used as option for undetermined content license when
        # submitting suggestions or editing suggestions
        (None, _("I'm not sure")),
        ('CC-BY', _('Creative Commons Attribution')),
        ('CC-BY-ND', _('Creative Commons Attribution-NoDerivs')),
        ('CC-BY-NC', _('Creative Commons Attribution-NonCommercial')),
        ('CC-BY-ND-NC', _('Creative Commons '
                          'Attribution-NonCommercial-NoDerivs')),
        ('CC-BY-SA', _('Creative Commons ShareAlike')),
        ('CC-BY-NC-SA', _('Creative Commons '
                          'Attribution-NonCommercial-ShareAlike')),
        ('GFDL', _('GNU Free Documentation License')),
        ('OPL', _('Open Publication License')),
        ('OCL', _('Open Content License')),
        ('ADL', _('Against DRM License')),
        ('FAL', _('Free Art License')),
        ('PD', _('Public Domain')),
        ('ARL', _('All rights reserved')),
        ('OF', _('Other free license')),
        ('ON', _('Other non-free license')),
    )

    #: List of free licenses as license keys
    FREE_LICENSES = (
        'CC-BY',
        'CC-BY-NC',
        'CC-BY-SA',
        'CC-BY-NC-SA',
        'GFLD',
        'OPL',
        'OCL',
        'ADL',
        'FAL',
        'PD',
        'OF',
    )

    #: List of choices that can be used for the ``license`` property
    LICENSE_CHOICES = [l[0] for l in LICENSES]

    #: List of Outernet archive names and translatable names
    ARCHIVES = (
        (None, _('off air')),
        ('core', _('core')),
        ('curated', _('curated')),
        ('ephemeral', _('ephemeral')),
        ('expedited', _('expedited')),
    )

    #: List of choices that can be used for ``archive`` property
    ARCHIVE_CHOICES = [a[0] for a in ARCHIVES]

    #: URL of the content
    url = ndb.StringProperty()

    #: Content title
    title = ndb.StringProperty()

    #: Archive content belongs to
    archive = ndb.StringProperty(choices=ARCHIVE_CHOICES)

    #: Content license
    license = ndb.StringProperty(choices=LICENSE_CHOICES)

    #: Whether content is from a partner
    is_partner = ndb.BooleanProperty(default=False)

    #: Whether content uses a free license (read-only)
    is_free = ndb.ComputedProperty(
        lambda self: self.license in self.FREE_LICENSES)

    #: Whether content is expedited (read-only)
    is_expedited = ndb.ComputedProperty(
        lambda self: self.archive is 'expedited')

    #: Whether content is currently on air (read-only)
    on_air = ndb.ComputedProperty(lambda self: self.archive is not None)

    #: Number of positive votes
    upvotes = ndb.IntegerProperty(default=0)

    #: Number of negative votes
    downvotes = ndb.IntegerProperty(default=0)

    #: Sum of postive and negative votes (read-only)
    votes = ndb.ComputedProperty(lambda self: self.upvotes + self.downvotes)

    @property
    def license_type(self):
        """
        Returns the license type
        """
        if self.is_expedited:
            return 'expedited'
        if not self.license:
            return 'unknown'
        if self.is_free:
            return 'free'
        return 'non-free'

    @property
    def path(self):
        """
        Returns the path of the content.
        """
        return '/contnent/%s' % self.key.id()


    @staticmethod
    def get_urlid(url):
        """
        Return MD5 hexdigest of an URL. This method returns a hexdigest of the
        specified URL, which is used as URL key.
        """
        md5 = hashlib.md5()
        md5.update(url)
        return md5.hexdigest()

    @classmethod
    def get_recent(cls, start=0, count=10):
        """
        Fetch most recently updated content records. The ``start`` paramter is
        used to skip a number of items from the beginning, and ``count`` is
        used to return a limited number of items.

        The performance of this call is affected by both ``start`` and
        ``count``. Thnk of it as iteratiing ``start`` number of items before
        actually returning anything.

        :param start:   number of items to skip
        :param count:   number of items to return
        :returns:       iterable of content records
        """
        q = cls.query().order(-cls.updated).fetch(count, offset=start)

    @classmethod
    def create(cls, url, title=None, check_url=True, **kwargs):
        urlid = cls.get_urlid(url)
        existing = cls.get_cached(urlid)

        if check_url:
            try:
                real_url, page_title = get_url_info(url)
            except BotError as err:
                logging.exception("Could not get URL info for '%s': %s" % (
                    url, err))
                raise

        url = real_url
        if not title:
            title = page_title
        content = cls(url=url, title=title, id=urlid, **kwargs)
        content.put()
        return content

