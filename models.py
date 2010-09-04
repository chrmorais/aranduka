#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This set of MODELS are based on the discussion in the
# Aranduka mailing list about the schema.

from elixir import *

metadata.bind = "sqlite:///books.sqlite"
metadata.bind.echo = True

class Book (Entity):
    title = Field(Unicode(40))
    volumen = Field(Integer)
    url = Field(Unicode(40))
    cover = Field(Unicode(40))
    comments = Field(UnicodeText)
    # Relationships
    authors = OneToMany('Author')
    files = OneToMany('File')
    identifiers = OneToMany('Identifier')
    tags = ManyToMany('Tag')

    def __repr__(self):
        return '<book>%s - %s</book>' % (self.title, self.author)

class Identifier (Entity):
    key = Field(Unicode(30))
    value = Field(Unicode(30))
    # Relationships
    book = ManyToOne('Book')

    def __repr__(self):
        return '<identifier>%s: %s</identifier>' % (self.key, self.value)

class Author (Entity):
    name = Field(Unicode(30))
    # Relationships
    books = ManyToOne('Book')

    def __repr__(self):
        return '<author>%s</author>' % (self.name)

class Tag (Entity):
    name = Field(Unicode(30))
    value = Field(Unicode(30))
    # Relationships
    book = ManyToMany('Book')

    def __repr__(self):
        return '<tag>%s: %s</Tag>' % (self.name, self.value)

class File (Entity):
    file_name = Field(Unicode(30))
    file_size = Field(Unicode(30))
    book = ManyToOne('Book')

    def __repr__(self):
        return '<file>%s</file>' %(self.file_name)

