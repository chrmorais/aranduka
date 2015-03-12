# Introduction #

There's a bunch of stuff that would need to be done before releasing a first version of Aranduka. The idea of this page is to define a set of basic features to put us in the way of creating a first release.

## Core ##

  * Finish download manager (see [issue 6](https://code.google.com/p/aranduka/issues/detail?id=6))
  * Re-think and re-design cover handling.
  * Decide between Tags or Shelves
  * Enhance book editor/book view (book files, downloads progress, etc.).
  * CouchDB. A document-oriented database, I think it's replication ability would make Aranduka much cooler. Imagine if your books database would be always available, on a website, on all your computers, and maybe someday on your phone, tablet, etc? couchdb makes this possible and not too hard to do. The bad part is that it means rewriting a big chunck of aranduka.
  * Online archive syncing. Either using u1, or dropbox, or something else, this makes the books themselves available. It could be attached to a tag, there is already code for that kind of thing.

## Importer ##

  * Define how it should work / use cases
  * Design a GUI - a dialog, maybe with a progress bar
  * Skip search option
  * Add tags to the imported books

## eBook formats support ##

  * Support for comics formats

### ePub ###

  * Enhance ePub viewer ([issue 16](https://code.google.com/p/aranduka/issues/detail?id=16))
  * Implement RSS->ePub gateway

## Social Networks ##

  * Finish integration with GoodReads