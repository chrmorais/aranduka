# -*- coding: utf-8 -*-
import os.path
import config

from PyQt4 import QtCore

# Possible names of folders for translation files
__folder_names = ['translations', 'languages', 'lang']


def _get_translator(locale, path, prefix=None):
    """Creates a QTranslator object for a locale from path."""
    if not os.path.exists(path):
        return None

    qtTranslator = QtCore.QTranslator()
    name = u'%s_%s' % (prefix, locale) if prefix is not None else locale
    tname = prefix.capitalize() if prefix is not None else 'Plugin'
    if qtTranslator.load(name, path):
        print "Loaded %s translator for %s" % (tname, locale)
    else:
        print "Failed to load %s translator for %s" % \
              (tname, locale)
        return None
    return qtTranslator


def _get_locale():
    """Retrieves the configured locale. It attempts to get it from
    the configuration file. The default is the system's locale."""
    locale = config.getValue('i18n', 'locale', 'system')
    if locale == 'system':
        return unicode(QtCore.QLocale.system().name())
    else:
        return locale


def get_plugin_translator(name, path):
    """Creates a translator object for a plugin"""
    locale = _get_locale()
    print "Getting translator for plugin %s to %s" % (name, locale)
    for f in __folder_names:
        t = _get_translator(locale, os.path.join(path, f), None)
        if t:
            print "Loaded translator for plugin %s to %s" % (name, locale)
            return t
    return None


def get_translators():
    """Returns a list of translators to install in the QApplication"""
    translators = []
    locale = _get_locale()
    print "Loading translations for '%s'" % locale
    sources = [('qt', QtCore.QLibraryInfo.location(
                             QtCore.QLibraryInfo.TranslationsPath))]
    sources += [('aranduka', os.path.join(
                                os.path.abspath(
                                    os.path.dirname(__file__)), f))
                                for f in __folder_names]

    for name, path in sources:
        t = _get_translator(locale, path, name)
        if t:
            translators.append(t)
    return translators

if __name__ == "__main__":
    print get_translators()
