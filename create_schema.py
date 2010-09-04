#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def createDataBase():
    if os.path.isfile("./books.sqlite"):
        print "looks like the database all ready exists."
        return False
    print "This file will create the schema"

    from models import *
    setup_all()
    create_all()
    return True

if __name__ == "__main__":
    createDataBase()

