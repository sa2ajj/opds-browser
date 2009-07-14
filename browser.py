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

import webbrowser

from PyQt4 import QtCore, QtGui

from cgi import escape
from pprint import pformat

from opds import load

def data_to_icon(data):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(data)

    return QtGui.QIcon(pixmap)

def get_icon(name, data):
    # do not cache for now
    return data_to_icon(data)

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

class OPDSCatalogue(OPDSGeneric):
    ''' ... '''

    def __init__(self, entry):
        super(OPDSCatalogue, self).__init__(entry, QtGui.QListWidgetItem.Type+1)

class OPDSEntry(OPDSGeneric):
    ''' ... '''

    def __init__(self, entry):
        super(OPDSEntry, self).__init__(entry, QtGui.QListWidgetItem.Type+2)

def is_catalogue(links):
    ''' check whether the specified set of links is for a catalogue

(unfortunately, currently there's no better way to distinguish between
catalogue & book entries
'''
    for link in links:
        if link['type'] == 'application/atom+xml' and 'rel' not in link:
            return True

    return False

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
    def __init__(self):
        super(OPDSBrowser, self).__init__()

        self._create_widgets()

        splitter = QtGui.QSplitter()

        splitter.addWidget(self._items)
        splitter.addWidget(self._text_viewer)

        self.setCentralWidget(splitter)
        self.setWindowTitle('OPDS Browser')

    def _create_widgets(self):
        self._items = QtGui.QListWidget()

        self._items.currentItemChanged.connect(self.update_preview)
        self._items.itemActivated.connect(self.load_item)

        self._text_viewer = QtGui.QTextBrowser()
        self._text_viewer.setOpenExternalLinks(False)
        self._text_viewer.setOpenLinks(False)
        self._text_viewer.anchorClicked.connect(self.open_link)

    def open_link(self, link):
        ''' opens the link in an external browser '''

        webbrowser.open(link.toString())

    def load_url(self, url):
        data = load(url)

        if data['title'][0] == 'text':
            self.setWindowTitle(data['title'][1])
        else:
            self.setWindowTitle('Unknown format (%s): %s' % data['title'])

        self._items.clear()

        for entry in data['entries']:
            self._items.addItem(get_item(entry))

        self._items.setCurrentRow(0)

    def update_preview(self, current, previous):
        if current is not None:
            assert isinstance(current, OPDSGeneric), 'something went really wrong'

            self._text_viewer.setHtml(current.html())

    def load_item(self, item):
        print 'load_item', item

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    browser = OPDSBrowser()
    browser.load_url('http://www.feedbooks.com/catalog.atom')
    # browser.load_url('http://www.feedbooks.com/userbooks/downloads.atom?added=month')
    browser.show()

    sys.exit(app.exec_())
