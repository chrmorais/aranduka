#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This set of MODELS are based on the discussion in the
# Aranduka mailing list about the schema.

import os
import urllib2
from elixir import *
from downloader import get

def initDB():
    "Create or initialize the database"
    "Setting up database"
    metadata.bind = "sqlite:///books.sqlite"
    metadata.bind.echo = False
    setup_all()
    if not os.path.isfile("./books.sqlite"):
        "Creating database"
        create_all()
        session.commit()

class Book (Entity):
    using_options(tablename='books')
    title = Field(Unicode(40))
    volumen = Field(Integer)
    url = Field(Unicode(40))
    cover = Field(Unicode(40))
    comments = Field(UnicodeText)
    # Relationships
    authors = ManyToMany('Author')
    files = OneToMany('File')
    identifiers = OneToMany('Identifier')
    tags = ManyToMany('Tag')

    def __repr__(self):
        return '<book>%s - %s</book>' % (self.title, self.authors)

    def fetch_file(self, url, extension):
        """Given a URL, and a file extension, downloads it and adds
        the file as belonging to this book"""
        # FIXME: check for name collisions and identical files
        # FIXME: make non-blocking
        # FIXME: give user feedback
        fname = os.path.abspath(
            os.path.join("ebooks", str(self.id) +"."+extension))
        print "Fetching file: ", url
        u=urllib2.urlopen(url)
        data = u.read()
        u.close()
        thumb = open(fname,'wb')
        thumb.write(data)
        thumb.close()

        print "F1", self.files
        f = File(file_name = fname)
        self.files.append(f)
        print "F2", self.files
        session.commit()
        

    def fetch_cover(self, url = None):
        """Downloads and stores a cover for this book, if possible.
        
        If a url is given, it uses that. If not, it tries to get it from other
        sources.
        """
        # FIXME: make non-blocking
        # FIXME: give user feedback
        fname = os.path.join("covers", str(self.id) +".jpg")
        if url:
            print "Fetching cover: ", url
            u=urllib2.urlopen(url)
            data = u.read()
            u.close()
            thumb = open(fname,'wb')
            thumb.write(data)
            thumb.close()
        else:
            isbns = Identifier.query.filter_by(key = 'ISBN', book = self).all()
            for isbn in isbns:
                # Try openlibrary
                try:
                    print "Trying openlibrary with ISBN: '%s'"%isbn.value
                    u=urllib2.urlopen('http://covers.openlibrary.org/b/isbn/%s-M.jpg?default=false'%isbn.value)
                    data = u.read()
                    u.close()
                    thumb = open(fname,'wb')
                    thumb.write(data)
                    thumb.close()
                    break
                except urllib2.HTTPError:
                    pass

                # Then we try LibraryThing
                # Maybe using my devkey here is not a very good idea.
                try:
                    print "Trying librarything with ISBN: '%s'"%isbn.value
                    u=urllib2.urlopen('http://covers.librarything.com/devkey/%s/large/isbn/%s'%('09fc520942eb98c27391d2b8e02f3866',isbn.value))
                    data = u.read()
                    u.close()
                    if len(data) > 1000: #A real cover
                        thumb = open(fname,'wb')
                        thumb.write(data)
                        thumb.close()
                        break
                except urllib2.HTTPError:
                    pass

class Identifier (Entity):
    using_options(tablename='identifiers')
    key = Field(Unicode(30))
    value = Field(Unicode(30))
    # Relationships
    book = ManyToOne('Book')

    def __repr__(self):
        return '<identifier>%s: %s</identifier>' % (self.key, self.value)

class Author (Entity):
    using_options(tablename='authors')
    name = Field(Unicode(250))
    # Relationships
    books = ManyToMany('Book')

    def __repr__(self):
        return '<author>%s</author>' % (self.name)

class Tag (Entity):
    using_options(tablename='tags')
    name = Field(Unicode(30))
    value = Field(Unicode(30))
    # Relationships
    books = ManyToMany('Book')

    def __repr__(self):
        return '<tag>%s: %s</Tag>' % (self.name, self.value)

class File (Entity):
    using_options(tablename='files')
    file_name = Field(Unicode(300))
    file_size = Field(Unicode(30))
    book = ManyToOne('Book')

    def __repr__(self):
        return '<file>%s</file>' %(self.file_name)

