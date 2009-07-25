Open Publication Distribution System
====================================

:status: DRAFT
:License: Creative Commons

This document describes the Open Publication Distribution System (OPDS) an application of the Atom
Syndication Format intended to enable content creators and distributors to distribute digital books
via a simple catalog format. This format is designed works interoperably across multiple desktop and
device software programs for acquiring and consuming eBooks ("Reading Systems"). The focus of this
document is to outline the requirements for preparing catalogs for use by compatible Reading
Systems; formal compliance requirements for Reading Systems will be documented elsewhere.  This
application of Atom was initially defined and implemented by Lexcycle for the Stanza application.

.. contents::

The Open Publication Distribution System
----------------------------------------

Users of compatible Reading Systems, in addition to being able to access
content they have previously acquired or acquire via other means, are also able
to access a catalog (list of online sources of content). Typically, the catalog
offers a number of free titles, which may be hosted by the Reading System
vendor and/or other sites, as well as the opportunity to purchase or borrow
paid content from stores and libraries. Additional stores and libraries may be
added by the user to their personal catalog.

The mechanism through which compatible Reading Systems access the distributed
catalog has three components: eBook content, XML catalog metadata, and an HTTP
transport for the catalog. The remainder of this document will discuss each of
those components in turn.

eBook Content: EPUB
-------------------

Reading Systems are often capable of accessing content in a variety of file formats; OPDS-compatible
Reading Systems must support IDPF EPUB, and may optionally support additional formats.

EPUB, formerly known as Open eBook, is the only standardized electronic book format available that
is designed to adapt to different screen sizes. It is flexible, enjoys high compression, and
utilizes standardized technologies (XHTML, CSS, Dublin Core, and ZIP) that are familiar to many
developers. EPUB is a relatively new standard, but already has support in such products as Stanza,
Adobe Digital Editions, the Sony Reader, Calibre, FBReader, Openberg Lector, and Mobipocket. The
EPUB standard is comprised of open and freely published specifications created and managed by the
International Digital Publishing Forum (IDPF).


The Catalog Format: Atom XML
----------------------------

For catalogs, OPDS extends the standard Atom format and associated HTTP-based APIs (:RFC:`4287` – "The Atom Syndication Format").

.. note:: While compatible with Atom, OPDS catalogs are not "news feeds" and it is not expected that
    they will be usefully consumable via a generic news reader program. The use of Atom by OPDS is
    similar to other uses for access to cloud-based information, such as Google Data APIs.

The catalog is defined as a series of links. OPDS-compatible Reading Systems must support two MIME
types in such links: `application/atom+xml` (which specifies that the link goes to another
catalog file, thereby enabling hierarchical catalog structures), and `application/epub+zip`,
which specifies that the link points to a valid ePub book.

Following is an example of how a top-level catalog (which just points to other catalogs) might
look::

    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
    <title>Billy Bob's Book Catalog</title>
    <updated>2008-08-18T17:40:58-07:00</updated>
    <author>
        <name>Billy Bob</name>
        <uri>http://www.billybobsbooks.com/</uri>
        <email>billybob@billybobsbooks.com</email>
    </author>
    <subtitle>
        Online catalog of Billy Bob's Booka!
    </subtitle>
    <id>urn:uuid:60a76c80-d399-12d9-b91C-0883939e0af6</id>
    <link rel="self" type="application/atom+xml" href="http://www.example.com/catalog.atom"/>
    <entry>
        <title>Some Good Books</title>
        <id>urn:uuid:1925c615-cab8-4ebb-aaaa-81da314efc61</id>
        <updated>2008-08-18T17:40:59-07:00</updated>
        <link type="application/atom+xml" href="goodbooks.atom"/>
    </entry>
    <entry>
        <title>Short Reads</title>
        <id>urn:uuid:1925c615-cab8-4ebb-aaaa-81da314efc62</id>
        <updated>2008-08-18T17:41:00-07:00</updated>
        <link type="application/atom+xml" href="shortreads.atom"/>
    </entry>
    <entry>
        <title>Classics &amp; Epics</title>
        <id>urn:uuid:1925c615-cab8-4ebb-aaaa-81da314efc63</id>
        <updated>2008-08-18T17:41:01-07:00</updated>
        <link type="application/atom+xml" href="classicsepics.atom"/>
    </entry>
    </feed>

To link to the actual books in your catalog, your link tags must be of the type
`application/epub+zip`. An example catalog is as follows::

    <?xml version="1.0"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <title>Online Catalog</title>
    <id>urn:uuid:09aeccc1-c633-aa48-22ab-000052cbd81c</id>
    <updated>2008-09-12T00:44:20+00:00</updated>
    <link rel="self" type="application/atom+xml" href="http://www.billybobsbooks.com/catalog/top.atom"/>
    <link rel="search" title="Search Billy Bob's Books" type="application/atom+xml"
        href="http://www.billybobsbooks.com/catalog/search.php?search={searchTerms}"/>
    <author>
        <name>Billy Bob</name>
        <uri>http://www.billybobsbooks.com</uri>
        <email>billybob@billybobsbooks.com</email>
    </author>
    <entry>
        <title>1984</title>
        <content type="xhtml">
            <div xmlns="http://www.w3.org/1999/xhtml">
                Classic dystopian novel by English author George Orwell.
            </div>
        </content>
        <id>urn:billybobsbooks:1166</id>
        <author>
            <name>Orwell, George</name>
        </author>
        <updated>2008-09-12T00:44:20+00:00</updated>
        <link type="application/epub+zip" href="http://www.billybobsbooks.com/book/1984.epub"/>
        <link rel="http://opds-spec.org/opds-cover-image-thumbnail" type="image/png"
            href="http://www.billybobsbooks.com/book/1984.png"/>
        <link rel="http://opds-spec.org/opds-cover-image" type="image/png"
            href="http://www.billybobsbooks.com/book/1984.png"/>
    </entry>
    <entry>
        <title>The Art of War</title>
        <content type="xhtml">
            <div xmlns="http://www.w3.org/1999/xhtml">
                Chinese military treatise that was written during the 6th century BC.
            </div>
        </content>
        <id>urn:billybobsbooks:168</id>
        <author>
            <name>Sun Tzu</name>
        </author>
        <updated>2008-09-12T00:44:20+00:00</updated>
        <link type="application/epub+zip" href="http://www.billybobsbooks.com/book/artofwar.epub"/>
        <link rel="http://opds-spec.org/opds-cover-image-thumbnail" type="image/png"
            href="http://www.billybobsbooks.com/book/artofwar.png"/>
        <link rel="http://opds-spec.org/opds-cover-image" type="image/png"
            href="http://www.billybobsbooks.com/book/artofwar.png"/>
    </entry>
    </feed>

.. note:: For large and complex catalogs, it may be desirable to dynamically generate the catalog
    XML files. Compatible Reading Systems are required to make no distinction between catalogs that
    are kept statically or dynamically.

Other catalog features
----------------------

The catalog format also supports the following additional features:

Searching
`````````

If a catalog XML file has a link with the rel search in its header, Reading Systems should provide a
search affordance (such an iconic magnifying glass button). The user will then be able to enter
search terms into the search box that pops up, and it will be sent to the server by replacing the
instance of the string ``{searchTerms}`` in the link's href attribute.

For example, if you have the following link::

    <link rel="search" title="Search Catalog" type="application/atom+xml"
        href="http://www.billybobsbooks.com/search.php?q={searchTerms}"/>

And if the user enters ``The Great Gatsby`` into the search field and submits, a compatible Reading
System will fetch the next catalog by going to the URL
``http://www.billybobsbooks.com/search.php?q=The+Great+Gatsby``.

Reading Systems are required to not put any constraints on the search terms you enter or the meaning
of the search. For example, if your top-level catalog has an "Authors" sub-catalog, you could have
the search URL that comes up in that catalog prioritize author names. Alternatively, you could have
all search URLs always go to a single global search URL (which is the decision that most catalogs
choose).

.. note:: The template syntax for the "search" rel attribute is based on the `OpenSearch URL
    Template Syntax`_.  It is anticipated that additional OpenSearch feature compatibility may be
    introduced in future revisions to OPDS.

.. _OpenSearch URL Template Syntax: http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_URL_template_syntaxAPI

Embedded Browser
````````````````

Reading Systems handle links of type `application/atom+xml` by loading the results as another
catalog entry, and handles links of type `application/epub+zip` (and any other supported eBook
formats) by loading the URL and trying to import it as a book. Additionally, you can have links of
type `application/xhtml+xml` and `text/html` from your catalog entry, which will cause the
Reading System to open a Web browser experience. This may be an embedded web browser (which may lack
features such as bookmarks, the ability to open links in a new window, history searching, or the
ability to enter an arbitrary URL), or a separate browser window, depending on the context (PC or
device). It is a requirement that Reading Systems will arrange that EPUB links in such web pages
function properly (i.e. the MIME type is handled by the Reading System). So if you have a storefront
where people can download books, and the user loads that web page via such a link, the user will be
able to download those books directly into a compatible Reading System.

One way in which a browser session is frequently used is as a mechanism for the user to register an
account with a bookstore, or to perform the purchase transaction (as the Open Publication
Distribution System does not yet define any built-in transaction processing abilities). A book
store's catalog may allow users to browse and search for books using the familiar and efficient
catalog Atom XML interface, but then when they want to purchase and download the book, they might
enter the (embedded or separate window) browser to log in and complete the transaction. Another way
in which the browser feature is used is to provide links to other sites that might have additional
useful information like book reviews.


In addition to HTML links described above, catalogs can provide enhanced visual experience for
applications that support it, by providing links to interactive web content, such as Flash or Java
applets. An application can choose to use such link as an alternative to HTML.  Rel attribute for
such links should be set to `http://opds-spec.org/opds-content-acquisition`. This rel value can
be placed on HTML links as well to make the meaning of such link unambiguous. All applications
should be able to recognize it.


Catalog Description Page
````````````````````````

It is generally recommended that the first entry in your top-level of a catalog has an "About" link
to an XHTML page describing the catalog, its contents, and contact information for the catalog
maintainer. This can be accomplished by having a normal entry that links to an XHTML page with that
information. E.g.::

    <entry>
        <title>About this Catalog</title>
        <link type="text/html" href="about.xhtml"></link>
        <content type="text">About Billy Bob's Books</content>
    </entry>

It is recommended that the resulting XHTML page be as simple as possible, and conform to the UI
guidelines of the mobile Operating System(s) that you expect Reading Systems to utilize. As
guidance, Reading System vendors may offer suitable style sheets that you can utilize for best
results.

Links in Book Descriptions
``````````````````````````

A book description can contain one or more link elements, which will be displayed beneath the book's
description in the catalog. The rel for these links is not currently used, but the links must be of
a supported type. I.e., they need to be one of:

  * `application/atom+xml`: traverses to the specified catalog
  * `application/epub+zip`: downloads the specified link and imports the book
  * `application/xhtml+xml`: launches the embedded browser with the URL to the valid XHTML page
  * `text/html`: launches the embedded browser with the URL  (optional)

Additional types may be supported, for example if a catalog offers a format other than EPUB, that
may be made available as an additional type (e.g.  `application/pdf`, intended to download the
specified link and imports the book as a PDF file). However, there is no guarantee that an
OPDS-compatible Reading System will support such additional types; if unsupported, Reading Systems
must ignore them.

Having links in the book description is essential for providing the ability for the user to perform
additional actions for the book. For example, the book may have an `application/xhtml+xml` link
that goes to a web page that contains book reviews, an `application/atom+xml` that links to a
"People Also Purchased..." catalog of similar books, and an `application/epub+zip` link that
allows the user to download a free sample of the book.

Links to books should specify rel value `http://opds-spec.org/opds-content`. Usage of rel
attribute is optional for EPUB content, but required for all other content formats (e.g. PDF).

Links to book samples (a incomplete variant of the book) must specify rel value
`http://opds-spec.org/opds-content-sample`.

Links to subcatalogs and additional book information must specify title attribute with the
human-readable description of the content (e.g. "Other books by this author" or "Reviews on
acmebooks.com").

Results Pagination
``````````````````

Since users may be on slow cellular networks when accessing your catalog, you should avoid sending
very large batches of responses to any requests. In general, we recommend paginating results in
batches of 20 or 30. As defined by the Atom specifications, if a catalog has a link with
`rel='next'`, then that will cause OPDS-compatible Reading Systems to display an interface
element that allows the user to load the additional results. When traversed, the URL in the link
will be hit, and additional results will be loaded and presented to the user.

Catalog Subdescriptions
```````````````````````

Sub-catalogs can have a small piece of descriptive text that appears below the catalog name. This is
useful for summarizing the catalog contents or providing additional hints. This is accomplished by
using code like::

    <entry>
        <title>Andersen, Hans Christian</title>
        <link type="application/atom+xml" href="http://www.billybobsbooks.com/anderson.atom"></link>
        <content type="text">11 books by this author</content>
    </entry>

Icons
`````

Catalog developers should use icons for book descriptions as well as catalog and sub-catalog
entries. Links with a rel of http://opds-spec.org/opds-cover-image-thumbnail will be displayed in
the catalog list, and links with a rel of http://opds-spec.org/opds-cover-image will be displayed as
the cover image in book description detail view. The thumbnail image for a book should have a
maximum width & height of 125 pixels, with a recommended aspect ratio of 2:3 (width:height). It is
recommended that thumbnail sizes stay consistent within a catalog. If a thumbnail image has a width
or height greater than 125 pixels, Reading Systems may rescale. However, since users may open a
large list of books, it is important to make efficient use of bandwidth by keeping the size of the
images as small as possible. Reading Systems are required to support images in the PNG format; other
formats, such as JPEG and GIF, may optionally be supported.

In addition to thumbnail and full sized cover images, Reading Systems also support images attached
to sub-catalogs. This, in combination with using catalog sub-descriptions, can provide a useful hint
to the user about the meaning of a particular catalog entry. As with cover images, there are no
restrictions on the particular size of a catalog icon, but care should be taken to keep the image
size as small as possible, and to keep the size consistent across all entries in the catalog.

When the href attribute of an image or icon is a URL, Reading Systems should asynchronously fetch
that URL whenever the book is displayed. This makes efficient use of bandwidth, since if a user
brings up a catalog page with 25 books, only the first books that are displayed will have their
covers automatically fetched. As the user scrolls down the list, the covers will dynamically be
fetched for those books (provided they are not already cached). In some cases, however, it might
make more sense to pre-load the image by embedded it directly into the catalog page. This might be
used for, say, the top-level view of the catalog where you will always have the same icons for the
page. In these cases, you can instead use a URL of the form "data:image/png;base64,..." to embed the
Base-64 encoded image data directly into the XML, thereby removing the need for Reading Systems to
asynchronously request the image. A good description of the Data URL scheme, as well as links to
tools that can generate a data: URI for your images, can be found at Wikipedia.

The Catalog Transport: HTTP, Compression, Authentication
--------------------------------------------------------

The last step of making your content available online is hosting it. Reading Systems access catalogs
via standard HTTP; that is, you need to host your catalogs and books on a web server. Setting up a
web server or hosting options is well beyond the scope of this documentation, but in short, if you
are able to create and upload a web page so it is available on the internet, you are able to create
a public catalog that Reading Systems can use. There are a wide variety of Atom publishing tools
available, most of which we expect to be compatible with OPDS-compatible Reading Systems. You may
wish to investigate using some of these tools to create catalogs.

OPDS-compatible Reading Systems must support HTTP-level gzip compression for all catalog
interactions. It is highly recommended that you enable this feature on your web server, as it can
dramatically speed up catalog access, especially for people using Reading Systems over slow cellular
networks.

OPDS-compatible Reading Systems must support basic HTTP authentication, which catalog providers can
use to deliver catalog information specific to the user. If a "401 Unauthorized" code is sent back
for any requests, then Reading System must pop-up a username/password dialog which enabled the user
to enter a username and password. This information is useful if, say, your catalog has a "bookshelf"
feature that can list all the books that a user has purchased.

Adding Catalogs to a Reading System
-----------------------------------

An OPDS-compatible Reading System must enable users to add additional catalogs to their online
catalog listing, by specifying a full URL. The specific UI affordance(s) for managing such
user-added catalogs are Reading System dependent.

If an HTML link's href attribute utilizes the `http://` URL scheme, the remainder of the URL
represents an OPDS catalog endpoint. OPDS-compatible Reading Systems should, as allowed by
platforms/browsers, register to handle this URL scheme, which will result in, when the link is
activated, launching the Reading System application which will add the specified address a new
custom catalog. For example, if your catalog located at
`http://www.billybobsbooks.com/catalog.atom`, accessing a link of the format
"http://www.billybobsbooks.com/catalog.atom" on a system where a compatible OPDS Reading System has
been installed will result in that catalog being added to the user's catalog listing. Reading
Systems are required to support HTTP access; they may, optionally, support other protocols using
schemes like `https://` for HTTP over SSL and `ftp://` for FTP access.

An OPDS-compatible Reading System should support auto-discovery of such OPDS catalog endpoints by
enabling a user to type in a partial URL (typically a domain name) and retrieving and searching the
HTML file for intances of links with the `http://` URL scheme defined above. This handles the
situation where the platform/browser may not support binding to custom URL schemes, and the
situation where multiple OPDS-compatible Reading Systems are installed. This auto-discovery
convention is based on to the de facto standard for RSS feed auto-discovery in HTML web pages (see
`How to add RSS Autodiscovery to your site`_).

.. _How to add RSS Autodiscovery to your site: http://www.petefreitag.com/item/384.cfm

In additional to statically declared or manually entered OPDS catalogs, OPDS catalogs can be
"discoverable" by being advertized on a local network using DNS based Service Discovery (DNS-SD),
which is a "ZeroConf" technique that has many free and popular implementations, such as Bonjour on
Apple Macintosh and Avahi on Linux/UNIX. Reading Systems that support DNS-SD will discover catalogs
on the local network by searching for DNS-SD records of type `_opds._tcp`, and using the "path"
attribute to specify the HTTP URL path of the catalog. Discoverable catalogs can be useful in the
following scenarios:

  * Public libraries that want to allow local users to browse and download books without requiring
    them to perform manual configuration steps.
  * Book stores wanting to provide sample chapters, free promotional books, or materials in
    conjunction with special events like guest author speaking engagements.
  * Desktop software acting as a companion for a dedicated reading device that wants to enable
    synchronization of libraries without requiring physical device tethering.

Finally, Reading Systems will typically also provide the ability for some catalogs to be listed in
their default Online Catalog section. Mechanisms for handling such default listings are Reading
System dependent and outside the scope of the OPDS specification.

Summary of Atom Compatibility in OPDS
-------------------------------------

Most of the OPDS features described above simply represent a particular set of conventions for using
Atom and HTTP, compatible with the Atom specifications.  These include:

  * the overall catalog format
  * catalog hierarchy (links to sub-catalogs)
  * HTTP transport including gzip compression and authentication
  * Support for catalog descriptions, links in book descriptions, and book sub-descriptions as
    standard Atom link and content types.

Data URL support in thumbnail image definitions A few OPDS features represent extensions to Atom, these include:

  * Searching: the OpenSearch-based URL template syntax is not defined by the Atom specifications.
    As "{" and "}" are designated as "unsafe" characters which must be encoded in URLs (per :RFC:`1738`),
    Atom-conforming processing software may not successfully process search links in catalogs.
  * Icons: the use of new link "rel" attribute types is a conformant extension to the base Atom
    specification and such links are required to be ignored by Atom software that does not support
    them.

.. vim:tw=100:ts=4:sw=4:et
