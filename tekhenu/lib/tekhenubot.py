"""
tekhenubot.py: (hopefully) well-behaved Tehkenu bot

Tekhenu
2014, Outernet Inc <hello@outernet.is>
All rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import unicode_literals

import logging

from urlparse import urlparse
from httplib import HTTPException
from HTMLParser import HTMLParseError
from urllib2 import URLError, HTTPError, Request, urlopen

from bs4 import BeautifulSoup
from robotexclusionrulesparser import RobotExclusionRulesParser as RobotParser

__version__ = '0.1-dev'

UA_STRING = 'Tekhenubot/%s (+https://www.outernet.is/)' % __version__


class BotError(Exception):
    pass


class InvalidURLError(BotError):
    pass


class NotAllowedError(BotError):
    pass


class FetchError(BotError):
    def __init__(self, msg, original_error):
        self.error = original_error
        super(FetchError, self).__init__(msg)


class ContentError(BotError):
    def __init__(self, original_error):
        self.error = original_error
        super(ContentError, self).__init__('Error parsing content')


def get_url_base(url):
    """
    Return base URL for given URL. This function returns the base URL, with
    scheme and netloc of the specified URL. This can be used to construct URLs
    for different paths on the same host.

    :param url:     source URL
    :returns:       base URL
    """
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise InvalidURLError("URL is incomplete ('%s')" % url)
    return '{}://{}'.format(parsed.scheme, parsed.netloc)


def get_host(url):
    """
    Return the host name with port if any. This function returns the netloc
    part of the specified URL. This is mostly useful for 'Host' header.
    """
    parsed = urlparse(url)
    hostname = parsed.netloc
    if not hostname:
        raise InvalidURLError("URL is incomplete ('%s')" % url)
    return hostname


def get_robots_url(url):
    """
    Return the robots.txt URL for a host at given URL. This function returns
    the full URL of robots.txt for specified URL. It only returns the URL
    without actually parsing the file.
    """
    return '{}/robots.txt'.format(get_url_base(url))


def is_url_allowed(url):
    """
    Returns ``True`` if robots.txt rules for given URL allow fetching it. This
    function parses the robots rules for given URL (if any) and returns a
    boolean flag that tells you whether fetching it is allowed. Note that it
    doesn't test whether the URL exists on the host.

    :param url:     URL to test
    :returns:       ``True`` if URL can be fetched, ``False`` otherwise
    """
    robots = RobotParser()
    robots.user_agent = UA_STRING
    robots.fetch(get_robots_url(url))
    if robots.response_code != 200:
        return True
    return robots.is_allowed(UA_STRING, url)


def make_request(url):
    """
    Make a GET request as Tekhenubot. This function makes a request as
    Tekhenubot and returns a response object.

    This function raises :py:class:`tekhenu.lib.tekhenubot.FetchError` if there
    are any errors while fetching the URL.

    :param url:     URL to fetch
    :raises:        FetchError
    :returns:       response object
    """
    req = Request(url)
    req.add_header('User-Agent', UA_STRING)
    req.add_header('Host', get_host(url))
    try:
        res = urlopen(req)
    except (IOError, HTTPError) as err:
        raise FetchError("Resource could not be fetched ('%s')" % url, err)
    code = res.getcode()
    if code != 200:
        raise FetchError("Status code was not OK ('%s')" % url, code)
    return res


def get_title(data):
    """
    Return a title of the document from given data. Data is either a string or
    response object from ``urlopen()`` call.

    :param data:    string or ``urlopen()`` return value
    :raises:        ContentError
    :returns:       title as tring or ``None`` if no title is found
    """
    try:
        soup = BeautifulSoup(data)
    except HTMLParseError as err:
        raise ContentError('Could not parse content', err)
    if soup.title:
        return soup.title.string
    elif soup.h1:
        return soup.h1.string
    return None


def get_url_info(url):
    """
    Retrieve basic information about the URL. This function retrieves basic
    information about the URL like the actual URL of used in the request, and
    page title.

    Actual URL may be different from the specified URL if the server requested
    us to perform a redirect, which is transparently handled by ``urllib2``.

    The page is retrieved and parsed using BeautifulSoup, and title is
    extracted from the page. The page's ``<title>`` tag is looked up to
    retrieve the title, and ``<h1>`` is used as fallback. Title may also be
    ``None`` if page contains no usable title.

    If the URL cannot be fetched, ``FetchError`` is raised. If the URL cannot
    be fetched because of robot rules, ``NotAllowedError`` is raised instead.
    This function does not keep track of these failures. It is your
    responsibility to track them and ensure that requests to bad URLs are not
    repeated.

    :param url:     URL to get info for
    :raises:        FetchError, NotAllowedError
    :returns:       tuple containing actual URL, page title, response object
    """
    try:
        if not is_url_allowed(url):
            raise NotAllowedError("'%s' is not allowed by robots.txt" % url)
    except HTTPException as err:
        raise FetchError('Could not fetch robots.txt', err)
    res = make_request(url)
    real_url = res.geturl()
    title = get_title(res)
    return real_url, title



