#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This set of MODELS are based on the discussion in the
# Aranduka mailing list about the schema.

from elixir import *

metadata.bind = "sqlite:///books.sqlite"
metadata.bind.echo = False

class Book (Entity):
    title = Field(Unicode(40))
    author = Field(Unicode(40))
    serie_number = Field(Unicode(40))
    volumen = Field(Integer)
    url = Field(Unicode(40))
    cover = Field(Unicode(40))
    comments = Field(UnicodeText)
    # Relationships
    files = OneToMany('File')
    tags = ManyToMany('Tag')

    def __repr__(self):
        return '<book>%s - %s</book>' % (self.title, self.author)

class Tag (Entity):
    name = Field(Unicode(30))
    value = Field(Unicode(30))
    # Relationships
    books = ManyToMany('Book')

    def __repr__(self):
        return '<tag>%s: %s</Tag>' % (self.name, self.value)

class File (Entity):
    file_name = Field(Unicode(300))
    file_size = Field(Unicode(30))
    book = ManyToOne('Book')

    def __repr__(self):
        return '<file>%s</file>' %(self.file_name)

