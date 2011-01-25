# -*- coding: utf-8 -*-
"""
Alibris Book Guesser

This plugin allows you to search for a book's information
using Alibris' API 

More information about the API:
http://developer.alibris.com/docs
"""
import datetime
import urllib2
import json
from urllib import urlencode
from pluginmgr import Guesser
from metadata import BookMetadata

# Base URL for Alibris' Search Method
__baseurl__ = 'http://api.alibris.com/v1/public/search?'

# Alibris API Key
__apikey__ = '9q3rk555cg4aqttx6tyehwuk'

class AlibrisGuesser(Guesser):
    name = "Alibris"

    def can_guess(self, book):
        return True

    def _translateQuery (self, query):
        q = []
        if query.title is not None:
            q.append(('qtit', query.title))
        if query.authors is not None:
            q.append(('qauth', query.authors))
        if query.identifiers is not None:
            q.append(('qisbn', query.identifiers[0]))
        return q

    def _get_url (self, query):
        query = self._translateQuery(query)
        url = __baseurl__
        url += 'outputtype=json&'
        url += urlencode(query)
        url += '&apikey=%s' % __apikey__
        return url

    def search (self, query):
        """Implements Alibris' Search Method to retrieve the
           information of a book.

           More info on this method:
           http://developer.alibris.com/docs/read/Search_Method

           JSON Response example:
           http://developer.alibris.com/files/json-freakonomics.txt.
        """
        data = urllib2.urlopen(self._get_url(query)).read()
        return json.loads(data)

    def guess(self, query):
        md = self.search(query)
        if 'status' in md \
            and md['status'] == '0': 
            if 'book' in md:
                return [BookMetadata(title=x.get('title','No Title').decode('utf-8'),
                                    thumbnail=x.get('imageurl',''),
                                    date=datetime.date(1970,1,1),
                                    subjects=[],
                                    authors=[x.get('author')], # FIXME: Check how to split this
                                    identifiers=[('isbn', x.get('isbn'))],
                                    description='')
                        for x in md['book'] ]
            else:
                return None
        else:
            raise Exception("Failed to load Alibris")
