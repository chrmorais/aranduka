#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This set of MODELS are based on the discussion in the
# Aranduka mailing list about the schema.

import os
import urllib2
from elixir import *
import utils

def initDB():
    "Create or initialize the database"
    dburl="sqlite:///%s"%(os.path.join(utils.BASEPATH,'books.sqlite'))
    print "Setting up database ", dburl
    metadata.bind = dburl
    metadata.bind.echo = False
    setup_all()
    dbpath = os.path.join(utils.BASEPATH,"books.sqlite")
    if not os.path.isfile(dbpath):
        print "Creating database", dbpath
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

        authorlist = ""
        for author in self.authors:
            authorlist += author.name + "-"

        fname = os.path.abspath(
            os.path.join(utils.BOOKPATH,
                slugify(str(self.id)+"-"+self.title+"-"+authorlist)+"."+extension))
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

    def files_for_format(self, extension):
        """Given an extension (ie: "pdf"), return a list
        of files for this book that match it."""
        extension = extension.lower()
        files = []
        for f in self.files:
            _, ext = os.path.splitext(f.file_name)
            if extension == ext.lower():
                files.append(f.file_name)
        return files

    def available_formats(self):
        """Returns what formats are available for this book, as a list
        of strings, for example: ['.epub','.pdf']"""

        extensions = set()
        for f in self.files:
            _, ext = os.path.splitext(f.file_name)
            extensions.add(ext)
        return list(extensions)

    def cover(self):
        """Returns the path for the cover image if available, or the
        default nocover picture"""
        coverfn = os.path.join(utils.COVERPATH,"%s.jpg"%(self.id))
        if os.path.isfile(coverfn):
            return coverfn
        return os.path.join(utils.SCRIPTPATH,"nocover.png")

    def fetch_cover(self, url = None):
        """Downloads and stores a cover for this book, if possible.
        
        If a url is given, it uses that. If not, it tries to get it from other
        sources.
        """
        # FIXME: make non-blocking
        # FIXME: give user feedback
        fname = os.path.join(utils.COVERPATH, str(self.id) +".jpg")
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

