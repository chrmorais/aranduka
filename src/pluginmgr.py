"""Plugin manager for Aranduka, using Yapsy"""

import os
from yapsy.PluginManager import PluginManager
from yapsy.IPlugin import IPlugin

# These classes define our plugin categories
class ShelveView(object): pass
class BookStore(object): pass

manager = PluginManager(
    categories_filter={
        "ShelveView": ShelveView,
        "BookStore": BookStore,
    })

plugindir = os.path.join(
            os.path.abspath(
            os.path.dirname(__file__)),'plugins')

manager.setPluginPlaces([plugindir])

