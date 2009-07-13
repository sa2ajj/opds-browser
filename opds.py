#! /usr/bin/python
#
#  Copyright 2009 Mikhail Sobolev 
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

import sys

assert sys.version_info[0] > 2 or (sys.version_info[0] == 2 and sys.version_info[1] >= 5), 'Sorry, you need a more recent version of python'

from urllib2 import urlopen, Request

from xml.etree.cElementTree import parse, tostring

from pprint import pformat

ATOM_NS = 'http://www.w3.org/2005/Atom'
ATOM_NS_PREFIX = '{%s}' % ATOM_NS
ATOM_NS_PREFIX_LEN = len(ATOM_NS_PREFIX)

DC_NS = 'http://purl.org/dc/elements/1.1/'
DC_NS_PREFIX = '{%s}' % DC_NS
DC_NS_PREFIX_LEN = len(DC_NS_PREFIX)

AUTHOR_ELEM = '{%s}author' % ATOM_NS
TITLE_ELEM = '{%s}title' % ATOM_NS
LINK_ELEM = '{%s}link' % ATOM_NS
AUTHOR_ELEM = '{%s}author' % ATOM_NS
ENTRY_ELEM = '{%s}entry' % ATOM_NS
UPDATED_ELEM = '{%s}updated' % ATOM_NS
CONTENT_ELEM = '{%s}content' % ATOM_NS

def parse_link(link):
    assert link.tag == LINK_ELEM

    return link.attrib

def parse_author(author):
    assert author.tag == AUTHOR_ELEM

    result = {
        'name' : None,
        'url' : None,
        'email' : None
    }

    for child in author:
        if child.tag.startswith(ATOM_NS_PREFIX):
            property = child.tag[ATOM_NS_PREFIX_LEN:]

            if property in result:
                result[property] = child.text

    return result

def parse_entry(entry):
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
            type = child.get('type', 'text')

            if type == 'text':
                content = type, child.text
            else:
                content = type, tostring(child)
        elif child.tag.startswith(DC_NS_PREFIX):
            dcore.append((child.tag[DC_NS_PREFIX_LEN:], child.text, child.attrib))
        else:
            others.append(child)

    return {
        'author' : author,
        'title' : title,
        'links' : links,
        'dcore' : dcore,
        'content' : content,
        'others' : others,
        'updated' : updated
    }

def parse_catalog(catalog):
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

def load(url):
    ''' open the specified url, parse the data '''

    request = Request(url)
    request.add_header('User-Agent', 'OPDS Browser')

    return parse_catalog(parse(urlopen(request)).getroot())

def main(url):
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
