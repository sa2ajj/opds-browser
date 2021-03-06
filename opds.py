#! /usr/bin/python
#
#  Copyright (C) 2009 Mikhail Sobolev
#  Contact: Mikhail Sobolev <mss@mawhrin.net>
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
#  License for the specific language governing permissions and limitations
#  under the License.

"""
A simple wrapper over urllib2 & ElementTree to extract data from OPDS catalogs
"""

import sys

assert sys.version_info[0] > 2 or \
       (sys.version_info[0] == 2 and sys.version_info[1] >= 5),\
       'Sorry, you need a more recent version of python'

from urllib2 import urlopen, Request
from urlparse import urljoin

from xml.etree.cElementTree import parse, tostring

from pprint import pformat

__all__ = [ 'load' ]

ATOM_NS = 'http://www.w3.org/2005/Atom'
ATOM_NS_PREFIX = '{%s}' % ATOM_NS
ATOM_NS_PREFIX_LEN = len(ATOM_NS_PREFIX)

DC_NS = 'http://purl.org/dc/elements/1.1/'
DC_NS_PREFIX = '{%s}' % DC_NS
DC_NS_PREFIX_LEN = len(DC_NS_PREFIX)

XHTML_NS = 'http://www.w3.org/1999/xhtml'
XHTML_NS_PREFIX = '{%s}' % XHTML_NS
XHTML_NS_PREFIX_LEN = len(XHTML_NS_PREFIX)

AUTHOR_ELEM = '{%s}author' % ATOM_NS
TITLE_ELEM = '{%s}title' % ATOM_NS
LINK_ELEM = '{%s}link' % ATOM_NS
AUTHOR_ELEM = '{%s}author' % ATOM_NS
ENTRY_ELEM = '{%s}entry' % ATOM_NS
UPDATED_ELEM = '{%s}updated' % ATOM_NS
CONTENT_ELEM = '{%s}content' % ATOM_NS

def parse_link(link):
    """
    a simple "parser" for the <link>

    basically just returns the attirbutes
    """
    assert link.tag == LINK_ELEM

    return link.attrib

def parse_author(author):
    """extracts textual information from pre-defined children"""

    assert author.tag == AUTHOR_ELEM

    result = {
        'name' : None,
        'url' : None,
        'email' : None
    }

    for child in author:
        if child.tag.startswith(ATOM_NS_PREFIX):
            construct = child.tag[ATOM_NS_PREFIX_LEN:]

            if construct in result:
                result[construct] = child.text

    return result

def remove_qualifaction(root, namespace):
    """removes the specified namespace"""

    namespace_len = len(namespace)

    for elem in root.getiterator():
        if elem.tag.startswith(namespace):
            elem.tag = elem.tag[namespace_len:]

    return root

def parse_entry(entry):
    """parses the entry"""

    author = None
    title = None
    links = []
    dcore = []
    others = []
    content = None, None
    updated = None

    for child in entry:
        if child.tag == LINK_ELEM:
            links.append(parse_link(child))
        elif child.tag == AUTHOR_ELEM:
            author = parse_author(child)
        elif child.tag == TITLE_ELEM:
            title = child.get('type', 'text'), child.text
        elif child.tag == UPDATED_ELEM:
            updated = child.text
        elif child.tag == CONTENT_ELEM:
            content_type = child.get('type', 'text')

            if content_type == 'text':
                content = content_type, child.text
            elif content_type == 'xhtml':
                content = content_type, unicode(tostring(remove_qualifaction(child[0], XHTML_NS_PREFIX), 'utf-8'), 'utf-8')
            else:
                content = content_type, unicode(tostring(child, 'utf-8'), 'utf-8')
        elif child.tag.startswith(DC_NS_PREFIX):
            dcore.append((child.tag[DC_NS_PREFIX_LEN:], child.text, child.attrib))
        else:
            others.append(unicode(tostring(remove_qualifaction(child, ATOM_NS_PREFIX), 'utf-8'), 'utf-8'))

    return {
        'author': author,
        'title': title,
        'links': links,
        'dcore': dcore,
        'content': content,
        'others': others,
        'updated': updated
    }

def parse_catalog(catalog):
    """parses an atom feed thinking that it is OPDS compliant"""

    author = None
    title = None
    links = []
    entries = []
    updated = None

    for child in catalog:
        if child.tag == LINK_ELEM:
            links.append(parse_link(child))
        elif child.tag == ENTRY_ELEM:
            entries.append(parse_entry(child))
        elif child.tag == AUTHOR_ELEM:
            author = parse_author(child)
        elif child.tag == UPDATED_ELEM:
            updated = child.text
        elif child.tag == TITLE_ELEM:
            title = child.get('type', 'text'), child.text

    return {
        'author' : author,
        'title' : title,
        'links' : links,
        'entries' : entries,
        'updated' : updated
    }

def load(url, normalize_links=False):
    """open the specified url, parse the data"""

    request = Request(url)
    request.add_header('User-Agent', 'OPDS Browser')

    root = parse(urlopen(request)).getroot()

    if normalize_links:
        for child in root.getiterator(LINK_ELEM):
            child.attrib['href'] = urljoin(url, child.attrib['href'])

    return parse_catalog(root)

def main(url):
    """pretty much test code"""

    print url
    print '='*len(url)

    data = load(url)

    print 'Author:', data['author']
    print 'Title:', data['title']
    print 'Updated:', data['updated']
    print 'Links:', pformat(data['links'])
    print 'Entries:', pformat(data['entries'])

if __name__ == '__main__':
    main('http://www.feedbooks.com/catalog.atom')
    print
    main('http://www.feedbooks.com/userbooks/downloads.atom?added=month')
