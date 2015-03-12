# Plugins #

Aranduka uses [Yapsy](http://yapsy.sourceforge.net/) (Yet Another Plugin System) for this. For a pretty nice tutorial on how this system works, you can check out [Roberto Alsina's post on his blog](http://lateral.netmanagers.com.ar/weblog/posts/BB923.html).

## Plugin categories ##

Aranduka defines 5 plugins categories

  * **Guesser**: These plugins are used to guess a book's information (title, author, ISBN, etc.). This can be taken from the file itself or from an Internet database such as Google Books
  * **Device**: These plugins represent devices to read books
  * **Tool**: Adds a tool to Aranduka's Tools menu
  * **ShelfView**: Plugins to display the contents of the books database.
  * **BookStore**: Plugins to link Aranduka to different ways of book acquisition.

All these categories are defined in the `pluginmgr` module.

## Creating your plugin ##

Creating a new plugin is really easy using Yapsy. All plugins are located on the `plugins/` subdirectory.

There you will find for each plugin a `.yapsy` file and a module folder. The Yapsy file is a plain text file which defines some basic metadata of the plugin.

For example, the Google Books Guesser Yapsy file looks like:

```
[Core]
Name = Google Books Guesser
Module = guess_google

[Documentation]
Author = Roberto Alsina
Version = 0.1
Website = http://aranduka.googlecode.com
Description = Guess a book's data by looking it up at books.google.com
```

As you can see, the yapsy file defines a Module which is the name of the folder where your plugin is located. Google Books Guesser looks like this:

```
ls -1 guess_google/
guess.ui
__init__.py
```

In this case, because it's a very simple plugin, all of the action is contained on the init.py file of the module. From that file the most basic thing that you should pay attention to is:

```
from pluginmgr import Guesser

class GoogleGuesser(Guesser):
    name = "Google Books"

    def can_guess(self, book):
        return True

    def guess(self, book):
        # ... #
```

There we import the base plugin class (in this case Guesser), and overload the `can_guess` and the `guess` methods to implement the functionality of the plugin.

And that's it... plugins are loaded automatically at startup.