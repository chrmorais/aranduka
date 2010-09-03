#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from models import *

def createDataBase():
    setup_all()
    if os.path.isfile("books.sqlite"):
        print "looks like the database already exists."
        return False
    print "This file will create the schema"

    create_all()
    return True

if __name__ == "__main__":
    createDataBase()

