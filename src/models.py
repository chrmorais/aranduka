#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This set of MODELS are based on the discussion in the
# Aranduka mailing list about the schema.

import os
from elixir import *


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
    authors = OneToMany('Author')
    files = OneToMany('File')
    identifiers = OneToMany('Identifier')
    tags = ManyToMany('Tag')

    def __repr__(self):
        return '<book>%s - %s</book>' % (self.title, self.authors)

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
    name = Field(Unicode(30))
    # Relationships
    books = ManyToOne('Book')

    def __repr__(self):
        return '<author>%s</author>' % (self.name)

class Tag (Entity):
    using_options(tablename='tags')
    name = Field(Unicode(30))
    value = Field(Unicode(30))
    # Relationships
    book = ManyToMany('Book')

    def __repr__(self):
        return '<tag>%s: %s</Tag>' % (self.name, self.value)

class File (Entity):
    using_options(tablename='files')
    file_name = Field(Unicode(300))
    file_size = Field(Unicode(30))
    book = ManyToOne('Book')

    def __repr__(self):
        return '<file>%s</file>' %(self.file_name)

