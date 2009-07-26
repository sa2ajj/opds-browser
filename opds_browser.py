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

'''\
A simple OPDS browser

(work in progress)\
'''

import sys

from copy import copy
import webbrowser

from PyQt4 import QtGui, QtCore

from cgi import escape
from urllib import quote_plus

from pprint import pformat

from opds import load

def data_to_icon(data):
    ''' a simple converter from set of bytes to a Pixmap

:param data: bytes
:rtype: QPixmap
'''
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(data)

    return QtGui.QIcon(pixmap)

_cached_icons = {}

def get_icon(name, data):
    '''
get icon for the specified name

Performs basic caching to speed things up
'''
    global _cached_icons

    if name not in _cached_icons:
        _cached_icons[name] = data_to_icon(data)

    return _cached_icons[name]

class OPDSGeneric(QtGui.QListWidgetItem):
    ''' ... '''

    def __init__(self, entry, type=QtGui.QListWidgetItem.Type):
        super(OPDSGeneric, self).__init__(None, type)

        self._entry = entry

        self.init_item()

    def init_item(self):
        self.setIcon(get_icon('default.png', open('images/default.png', 'rb').read()))
        self.setText(self._entry['title'][1])

    def html(self):
        result = [
            '<h1>%s</h1>' % escape(self._entry['title'][1]),
            '<small>Last updated: %s</small>' % self._entry['updated']
        ]

        result.append('<table>')

        for key in [key for key in sorted(self._entry.keys()) if key not in [ 'title', 'updated' ]]:
            result.append('<tr><td>%s</td><td>%s</td>' % (escape(key), escape(pformat(self._entry[key]))))

        result.append('</table>')

        return ''.join(result)

    def activate(self, _):
        ''' do nothing! '''

class OPDSCatalogue(OPDSGeneric):
    ''' ... '''

    def __init__(self, entry):
        super(OPDSCatalogue, self).__init__(entry, QtGui.QListWidgetItem.Type+1)

        links = [ link for link in entry['links'] if is_catalogue_link(link) ]

        assert len(links) > 0, 'Oopsy-oops.'

        if len(links) > 1:
            print >> sys.stderr, 'Got more than one catalogue link:'

            for link in links:
                print >> sys.stderr, ' ', pformat(link)

        self._link = links[0]['href']

    def activate(self, browser):
        ''' load catalogue link in the main browser '''

        browser.load_url(self._link)

class OPDSEntry(OPDSGeneric):
    ''' ... '''

    def __init__(self, entry):
        ''' constructor '''
        super(OPDSEntry, self).__init__(entry, QtGui.QListWidgetItem.Type+2)

    def html(self):
        ''' prepare HTML for showing in the right pane

FIXME: the code is actually not nice at all.  Some sort of templating engine
must be used
'''
        result = [
            '<h1>%s</h1>' % escape(self._entry['title'][1]),
            '<small>Last updated: %s</small>' % self._entry['updated']
        ]

        result.append('<h2>Author</h2>')

        if self._entry['author']:
            result.append('''\
<dl>
    <dt>Name</dt>
    <dd>%(name)s</dd>
    <dt>e-mail</dt>
    <dd>%(email)s</dd>
    <dt>URL</dt>
    <dd>%(url)s</dt>
</dl>''' % self._entry['author'])
        else:
            result.append('<p>Author is unknown</p>')

        content_type, content_body = self._entry['content'][0], self._entry['content'][1]

        if content_type and content_body:
            result.append('<h2>Content</h2>')

            if content_type == 'text':
                result.append('<p>%s</p>' % escape(content_body))
            elif content_type == 'html':        # MSS: if I understand correctly, spec requires proper escaping to be in place
                result.append(content_body)
            elif content_type == 'xhtml':
                result.append(content_body)
            else:
                result.append('<p><b>Unknown type</b>: %s</p>' % content_type)
                result.append('<p>%s</p>' % escape(content_body))

        if self._entry['dcore']:
            result.append('<h2>Dublin Core</h2>')

            result.append('<dl>')

            for tag, value, attrib in self._entry['dcore']:
                if attrib:
                    result.append('''\
<dt>%s (%s)</dt>
<dd>%s</dd>''' % (tag, pformat(attrib), value))
                else:
                    result.append('''\
<dt>%s</dt>
<dd>%s</dd>''' % (tag, value))

            result.append('</dl>')

        if self._entry['links']:
            result.append('<h2>Links</h2>')

            result.append('<ul>')

            for link in self._entry['links']:
                tempo = copy(link)

                # +++ Hack +++

                if 'title' not in tempo:
                    tempo['title'] = tempo['href']

                    if 'rel' in tempo:
                        tempo['rel'] = 'rel="%s"' % tempo['rel']
                    else:
                        tempo['rel'] = ''

                # --- Hack ---

                result.append('<li><a href="%(href)s" %(rel)s type="%(type)s">%(title)s</a></li>' % tempo)

            result.append('</ul>')

        if self._entry['others']:
            result.append('<h2>Other elements</h2>')

            for item in self._entry['others']:
                result.append('<p>%s</p>' % escape(item))

        return ''.join(result)

    def activate(self, _):
        ''' not implemented '''

        print 'Not implemented!'

def is_catalogue_link(link):
    ''' check whether the specified link points to a catalogue '''

    return link['type'] == 'application/atom+xml' and 'rel' not in link

def is_catalogue(links):
    ''' check whether the specified set of links is for a catalogue

(unfortunately, currently there's no better way to distinguish between
catalogue & book entries
'''
    return len([ link for link in links if is_catalogue_link(link) ]) > 0

def get_item(entry):
    '''\
determines the entry type (catalog/book) and creates an instance of the
corresponding QListWidgetItem derivative

:param entry: list of { 'type' : <type>, 'href' : <href>, ... }
:rtype: OPDSGeneric/OPDSCatalogue/OPDSEntry
'''
    if is_catalogue(entry['links']):
        result = OPDSCatalogue(entry)
    else:
        result = OPDSEntry(entry)

    return result

class OPDSBrowser(QtGui.QMainWindow):
    def __init__(self, home_url):
        super(OPDSBrowser, self).__init__()

        self._home_url = home_url
        self._current_url = None
        self._history = []

        self._cache = {}

        self._create_widgets()

        splitter = QtGui.QSplitter()

        splitter.addWidget(self._items)
        splitter.addWidget(self._text_viewer)

        self.setCentralWidget(splitter)
        self.setWindowTitle('OPDS Browser')
        self.resize(800, 600)

        self.go_home()

    def _create_widgets(self):
        ''' create all necessary widgets '''
        self._items = QtGui.QListWidget()

        self._items.currentItemChanged.connect(self.update_preview)
        self._items.itemActivated.connect(self.load_item)

        self._text_viewer = QtGui.QTextBrowser()
        self._text_viewer.setOpenExternalLinks(False)
        self._text_viewer.setOpenLinks(False)
        self._text_viewer.anchorClicked.connect(self.open_link)

        # Among these three only _back is going to be used (when @ home,
        # there's no way back :))
        self._home = QtGui.QAction(QtGui.QIcon('images/gohome.png'), 'Home', self)
        self._home.triggered.connect(self.go_home)

        self._back = QtGui.QAction(QtGui.QIcon('images/previous.png'), 'Back', self)
        self._back.triggered.connect(self.go_back)

        self._add = QtGui.QAction(QtGui.QIcon('images/add.png'), 'Up', self)
        self._add.triggered.connect(self.add_item)

        self._search_what = QtGui.QComboBox()

        self._search = QtGui.QLineEdit(self)
        self._search.setSizePolicy(QtGui.QSizePolicy.Expanding, self._search.sizePolicy().verticalPolicy())
        self._search.returnPressed.connect(self.do_search)

        self._disable_search()

        # We do not really need this object in future, so not storing
        toolbar = self.addToolBar('main toolbar')

        toolbar.addAction(self._home)
        toolbar.addAction(self._back)
        toolbar.addSeparator()
        toolbar.addAction(self._add)

        toolbar = self.addToolBar('search toolbar')

        toolbar.addWidget(self._search_what)
        toolbar.addWidget(self._search)

    def _disable_search(self):
        ''' disable search functionality '''

        self._search_what.clear()
        self._search_what.addItem('<No search>')
        self._search_what.setDisabled(True)

        self._search.setDisabled(True)

    def _add_search_item(self, name, link):
        ''' adds a search item to the combobox '''

        # TODO: should I validate the link first (must have {searchTerms})?

        if not self._search_what.isEnabled():
            self._search_what.clear()
            self._search_what.setEnabled(True)

            self._search.setEnabled(True)

        self._search_what.addItem(name, QtCore.QVariant(link))

    def open_link(self, link):
        ''' opens the link in an external browser '''

        webbrowser.open(link.toString())

    def _cached_data(self, url):
        ''' a simple cache for downloaded data '''

        if url not in self._cache:
            self._cache[url] = load(url, True)

        return self._cache[url]

    def _load_url(self, url):
        ''' loads the provided URL '''
        self._current_url = url

        data = self._cached_data(url)

        if data['title'][0] == 'text':
            self.setWindowTitle(data['title'][1])
        else:
            self.setWindowTitle('Unknown format (%s): %s' % data['title'])

        self._items.clear()

        for entry in data['entries']:
            self._items.addItem(get_item(entry))

        self._items.setCurrentRow(0)

        self._disable_search()

        for link in [ link for link in data['links'] if link['type'] == 'application/atom+xml' and link.get('rel') == 'search' ]:
            self._add_search_item(link.get('title', 'Search'), link['href'])

    def load_url(self, url):
        '''\
loads the provided URL

This method stores the currently viewed URL in the `_history` and then calls `_load_url`.
'''
        if self._current_url is not None:
            self._history.append(self._current_url)

        self._load_url(url)

    def update_preview(self, current, previous):
        if current is not None:
            assert isinstance(current, OPDSGeneric), 'something went really wrong'

            self._text_viewer.setHtml(current.html())

    def load_item(self, item):
        ''' activate the double-clicked item '''

        item.activate(self)

    def go_home(self):
        ''' do go home! :) '''

        self._history = []  # clear the history
        self._load_url(self._home_url)

    def go_back(self):
        ''' 'back' implementation '''

        if len(self._history) > 0:
            self._load_url(self._history.pop())
        else:
            self._back.setDisabled(True)

    def add_item(self):
        print 'add'

    def do_search(self):
        ''' perform the search '''

        qv_link = self._search_what.itemData(self._search_what.currentIndex())

        if qv_link.isValid() and qv_link.canConvert(QtCore.QVariant.String):
            link = str(qv_link.toString())

            terms = unicode(self._search.text()).encode('utf-8')

            self._search.selectAll()

            self.load_url(link.replace('{searchTerms}', quote_plus(terms)))
        else:
            pass    # should I print something or show a dialog here?

def main(args):
    ''' the actual worker '''
    app = QtGui.QApplication(args)

    browser = OPDSBrowser('http://www.feedbooks.com/catalog.atom')
    browser.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)

# vim:ts=4:sw=4:et
