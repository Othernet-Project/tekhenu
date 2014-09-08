"""
bottle_ndb.py: Mixins and helpers for Bottle and GAE NDB

Copyright 2014 Outernet Inc <hello@outernet.is>
All rights reserved.
"""

import os
import base64
import hashlib

from google.appengine.ext import ndb
from google.appengine.api import memcache
from bottle import request


def generate_code(message, length=10):
    sha256 = hashlib.sha256()
    sha256.update(message)
    sha256.update(os.urandom(8))
    return base64.b64encode(sha256.hexdigest())[:length]


class CacheError(Exception):
    pass


class CachedModelMixin(object):
    cache_key_prefix = ''
    cache_time = 60

    @property
    def cache_id(self):
        return self.key.id()

    @property
    def cache_key(self):
        return self.get_cache_key(self.cache_id)

    def cache(self, time=cache_time, force_update=True):
        if not memcache.set(self.cache_key, self, time):
            raise CacheError("Failed to cache %s" % self.cache_key)

    def clear_cache(self):
        if not memcache.delete(self.cache_key):
            raise CacheError("Failed to clear %s" % self.cache_key)

    @classmethod
    def lookup(cls, id):
        key = ndb.Key(cls.__name__, id)
        return key and key.get()

    @classmethod
    def get_cached(cls, id):
        key = cls.get_cache_key(id)
        entity = memcache.get(key)
        if not entity:
            entity = cls.lookup(id)
        if entity:
            try:
                entity.cache()
            except CacheError:
                pass
        return entity

    @classmethod
    def is_cached(cls, id):
        key = cls.get_cache_key(id)
        return memcache.get(key) is not None

    @classmethod
    def get_cache_key(cls, id):
        return '%s:%s' % (cls.cache_key_prefix, id)

    @classmethod
    def get_all_cached(cls):
        return memcache.get_multi(key_prefix=cls.cache_key_prefix + ':')

    def _pre_put_hook(self):
        self.cache()

    @classmethod
    def _pre_delete_hook(cls, key):
        memcache.delete(cls.get_cache_key(key.id()))


class UrlMixin(object):
    path = ''

    @property
    def url(self):
        u = request.urlparts.scheme + '://' + request.urlparts.hostname
        if request.urlparts.port:
            u += ':%s' % request.urlparts.port
        return u + self.path



