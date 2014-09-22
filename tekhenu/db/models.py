"""
models.py: Application models

Tekhenu
(c) 2014, Outernet Inc
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals, division

import re
import urllib2
import hashlib
import logging

from bottle import request
from bs4 import BeautifulSoup
from bottle_utils.i18n import lazy_gettext as _

from lib.tekhenubot import *
from lib.bottle_ndb import ndb, CachedModelMixin, UrlMixin, TimestampMixin


class Event(TimestampMixin, ndb.Model):
    """
    Stores an event about content. Each event is compiled into an event log
    which is associated with a piece of Content. The events include such things
    as upvotes, downvotes, broadcasting, and creation.

    Each event also contains information about the exact time and IP address of
    the user that created it (based on request context at the time of
    creation).

    The ``Event`` entities should always be created using ``Content`` objects
    as parents. This allows ancestor queries and strong consistency during
    retrieval.

    Entity objects don't do any formatting for the complete log entires apart
    from returning a human-readable event name (see ``title`` property) and
    formatted timestamp (see ``timestamp`` property). It is expected that the
    log entries would be further formatted and rendered in templates.
    """

    # Event name aliases, use these instead of strings for safer event creation
    UNKNOWN = None
    CREATED = 'created'
    TITLE = 'title'
    LICENSE = 'license'
    BROADCAST = 'broadcast'
    UNBROADCAST = 'unbroadcast'
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'

    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

    EVENTS = (
        # Translators, used as event label for event of unknown/obsolete type
        (UNKNOWN, _('unknown action')),
        # Translators, used in event log associated with content
        (CREATED, _('created')),
        # Translators, used in event log associated with content
        (TITLE, _('title was edited')),
        # Translators, used in event log associated with content
        (LICENSE, _('license was changed')),
        # Translators, used in event log associated with content
        (BROADCAST, _('content was broadcast')),
        # Translators, used in event log associated with content
        (UNBROADCAST, _('content taken off air')),
        # Translators, used in event log associated with content
        (UPVOTE, _('voted up')),
        # Translators, used in event log associated with content
        (DOWNVOTE, _('voted down')),
    )

    EVENT_CHOICES = [e[0] for e in EVENTS]

    #: IP address of the request during which event was created
    ip_addr = ndb.StringProperty()

    #: Event name
    event = ndb.StringProperty(choices=EVENT_CHOICES)

    @property
    def title(self):
        """
        Human-readable and translatable event name.
        """
        # Translators, used as event label for event of unknown/obsolete type
        return dict(self.EVENTS).get(self.event, _('unknown action'))

    @property
    def timestamp(self):
        """
        Formatted timestamp.
        """
        return self.created.strftime(self.TIMESTAMP_FORMAT)

    @classmethod
    def create(cls, event, content):
        """
        Create event entity for specified content and current request context.
        This class method should always be called from within a request context
        (i.e., during ongoing request). It *will* fail outside a request.

        :param event:       event name
        :param content:     ``Key`` object for the related content
        :returns:           created ``Event`` object
        """
        ip = request.remote_addr
        event = cls(ip_addr=ip, event=event, parent=content)
        return event

    @classmethod
    def get_events(cls, content, count=20):
        """
        Return query representing specified number of events for given content.

        The events are returned in reverse-chonological order according to the
        creation timestamp.

        :param content:     ``Key`` object for the related content
        :param count:       number of events to return
        :returns:           ``Query`` object
        """
        return cls.query(ancestor=content).order(-cls.created).fetch(count)


class Content(CachedModelMixin, UrlMixin, TimestampMixin, ndb.Model):
    """
    Stores content information. This class is used to store content information
    in GAE's Datastore.

    The content information includes the URL of the page, page title, licensing
    information, and metadata about the broadcast (archive to which the page
    has been broadcast, etc).

    This model class also exposes :py:mod:`~teknhenu.lib.tekhenubot` exception
    classes for convenience.
    """

    BotError = BotError
    InvalidURLError = InvalidURLError
    NotAllowedError = NotAllowedError
    FetchError = FetchError
    ContentError = ContentError

    cache_time = 18000  # 5 hours in seconds

    NW_RE = re.compile(r'[^\w ]')
    WS_RE = re.compile(r'\s')

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
        ('CC-BY-SA', _('Creative Commons Attribution-ShareAlike')),
        ('CC-BY-NC-SA', _('Creative Commons '
                          'Attribution-NonCommercial-ShareAlike')),
        ('GFDL', _('GNU Free Documentation License')),
        ('OPL', _('Open Publication License')),
        ('OCL', _('Open Content License')),
        ('ADL', _('Against DRM License')),
        ('FAL', _('Free Art License')),
        ('PD', _('Public Domain')),
        ('OF', _('Other free license')),
        ('ARL', _('All rights reserved')),
        ('ON', _('Other non-free license')),
    )

    #: List of free licenses as license keys
    FREE_LICENSES = (
        'CC-BY',
        'CC-BY-NC',
        'CC-BY-SA',
        'CC-BY-NC-SA',
        'GFDL',
        'OPL',
        'OCL',
        'ADL',
        'FAL',
        'PD',
        'OF',
    )

    NONFREE_LICENSES = set([l[0] for l in LICENSES[1:]]) - set(FREE_LICENSES)

    #: List of choices that can be used for the ``license`` property
    LICENSE_CHOICES = [l[0] for l in LICENSES]

    CORE = 'core'
    CURATED = 'curated'
    EPHEMERAL = 'ephemeral'
    SPONSORED = 'sponsored'

    #: List of Outernet archive names and translatable names
    ARCHIVES = (
        # Translators, used to mark content not part of any archive
        (None, _('off air')),
        # Translators, used as archive name
        (CORE, _('core')),
        # Translators, used as archive name
        (CURATED, _('curated')),
        # Translators, used as archive name
        (EPHEMERAL, _('ephemeral')),
        # Translators, used as archive name
        (SPONSORED, _('sponsored')),
    )

    #: List of choices that can be used for ``archive`` property
    ARCHIVE_CHOICES = [a[0] for a in ARCHIVES]

    #: List of values and labels for status drop-down
    STATI = (
        # Translators, used as status for content not being broadcast
        ('offair', _('off air')),
        # Translators, used as status for content part of any non-core archive
        ('onair', _('on air')),
        # Translators, used as status for content being braodcast as core
        ('core', _('core')),
    )

    #: List of values and labels for sort order drop-down
    VOTES = (
        # Translators, used as label for sort order drop-down
        ('desc', _('highest first')),
        # Translators, used as label for sort order drop-down
        ('asc', _('lowest first')),
    )

    LICENSES_SIMPLE = (
        # Translators, used as license type label
        ('free', _('free')),
        # Translators, used as license type label
        ('nonfree', _('non-free')),
        # Translators, used as license type label
        ('unknown', _('unknown')),
    )

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

    #: Name of the entity that sponsors or partners with outernet
    partner = ndb.StringProperty()

    #: Admin notes
    notes = ndb.StringProperty()

    #: Wheter content has notes
    has_notes = ndb.ComputedProperty(lambda self: self.notes is not None)

    #: Urlid of content this content replaces
    replaces = ndb.StringProperty()

    #: Urlid of content that replaces this one
    replaced_by = ndb.StringProperty()

    #: Whether content is replaced (read-only)
    is_replaced = ndb.ComputedProperty(
        lambda self: self.replaced_by is not None)

    #: Whether content uses a free license (read-only)
    is_free = ndb.ComputedProperty(
        lambda self: self.license in self.FREE_LICENSES)

    #: Whether content is sponsored (read-only)
    is_sponsored = ndb.ComputedProperty(
        lambda self: self.archive == self.SPONSORED)

    #: Content satus
    status = ndb.ComputedProperty(lambda self: self._status())

    #: Number of positive votes
    upvotes = ndb.IntegerProperty(default=0)

    #: Number of negative votes
    downvotes = ndb.IntegerProperty(default=0)

    #: Sum of postive and negative votes (read-only)
    votes = ndb.ComputedProperty(lambda self: self.upvotes - self.downvotes)

    #: Ratio of upvotes to downvotes
    votes_ratio = ndb.ComputedProperty(
        lambda self: self._votes_ratio())

    #: Whether voting on this content is controversial (when votes_ratio is
    #: between 0.8 and 1.2.
    is_controversial = ndb.ComputedProperty(
        lambda self: 0.8 <= self._votes_ratio() <= 1.2)

    #: Search keywords (read-only)
    keywords = ndb.ComputedProperty(
        lambda self: self.get_keywords(self.title), repeated=True)

    def _status(self):
        """
        Return broadcast status, used by computed ``status`` property
        """
        if self.archive == self.CORE:
            return 'core'
        if self.archive is not None:
            return 'onair'
        return 'offair'

    def _votes_ratio(self):
        """
        Returns the upvote-downvote ratio. Divison by zero is treated as
        division by one.
        """
        return self.upvotes / max(1, self.downvotes)

    @property
    def is_editable(self):
        """
        Whether content details can be edited by users
        """
        return self.archive is None

    @property
    def is_core(self):
        """
        Whether content is part of core archive (read-only)
        """
        return self.archive == self.CORE

    @property
    def status_title(self):
        """
        Human readable and translatable status name
        """
        return dict(self.STATI)[self.status]

    @property
    def license_title(self):
        """
        Human readable license name
        """
        return dict(self.LICENSES)[self.license]

    @property
    def archive_title(self):
        """
        Human-readable archive name
        """
        return dict(self.ARCHIVES)[self.archive]

    @property
    def license_type(self):
        """
        Return license type, used by ``license_type`` property
        """
        if self.is_sponsored:
            return 'sponsored'
        if not self.license:
            return 'unknown'
        if self.is_free:
            return 'free'
        return 'nonfree'

    @property
    def path(self):
        """
        Returns the path of the content.
        """
        return '/content/%s' % self.key.id()

    @property
    def log(self):
        if not self.key:
            return []
        return Event.get_events(self.key)

    @classmethod
    def get_keywords(self, s=''):
        """
        Extract keywords from given string
        """
        if not s:
            return []
        keywords = self.WS_RE.split(self.NW_RE.sub(' ', s.lower()))
        return [k for k in keywords if len(k) > 2]


    @classmethod
    def create(cls, url, license=None, title=None, check_url=True,
               auto_upvote=True, **kwargs):
        """
        Create new ``Content`` entity or update existing with upvote.
        """
        license_changed = False
        urlid = cls.get_urlid(url)
        existing = cls.get_cached(urlid)
        to_put = []

        if check_url and not existing:
            real_url, page_title = get_url_info(url)
            if url != real_url:
                # TODO: We need to hit the database yet again and see if
                # there's an existing entity for the ``real_url`` now that
                # we'vw got it. Ideally, we want to get rid of the overhead of
                # getting the real URL only, without processing anything.
                url = real_url
                urlid = cls.get_urlid(url)
                existing = cls.get_cached(urlid)

        if existing and not existing.is_editable:
            return existing

        if existing:
            content = existing
            for k, v in kwargs.items():
                setattr(content, k, v)
            if auto_upvote:
                content.upvotes += 1
                to_put.append(Event.create(Event.UPVOTE, content.key))
            if license and content.license != license:
                content.license = license
                to_put.append(Event.create(Event.LICENSE, content.key))
        else:
            content = cls(url=url, id=urlid, license=license, **kwargs)

        content.title = content.title or title or page_title
        to_put.append(content)

        # We need to create events here because it may not have a key when new
        if not existing:
            to_put.append(Event.create(Event.CREATED, content.key))

        ndb.put_multi(to_put)
        if content.archive:
            event = Event.create(Event.BROADCAST, content.key)
            event.put()

        return content

    @staticmethod
    def get_urlid(url):
        """
        Return MD5 hexdigest of an URL. This method returns a hexdigest of the
        specified URL, which is used as URL key.
        """
        md5 = hashlib.md5()
        md5.update(url)
        return md5.hexdigest()

