from PyQt4 import QtCore, QtGui
from pluginmgr import Tool
import sys, os, subprocess


class Plugin(Tool):

    _proc = None
    
    def action(self):
        self._action = QtGui.QAction("Scan Barcode", None)
        self._action.triggered.connect(self.scan)
        return self._action

    def scan(self): 
        if sys.platform == 'win32':
            ZBARPATH = r"C:\Program Files (x86)\ZBar\bin\zbarcam.exe"
        else:
            ZBARPATH = which('zbarcam')
        print "ZBAR is:", ZBARPATH
        p=os.popen(ZBARPATH,'r')
        p = subprocess.Popen([ZBARPATH], stdout=subprocess.PIPE).communicate()[0]
        for code in p.splitlines():
            print "scanning"
            if code:
                print 'Got barcode:', code
                isbn = code.split(':')[1]
                QtGui.QDesktopServices.openUrl('http://www.goodreads.com/search/search?q=%s'%isbn)

# This implementation of which is taken from http://bugs.python.org/file16441/which.py
        
#!/usr/bin/env python
""" Which - locate a command

    * adapted from Brian Curtin's http://bugs.python.org/file15381/shutil_which.patch
    * see http://bugs.python.org/issue444582
    * uses ``PATHEXT`` on Windows
    * searches current directory before ``PATH`` on Windows,
      but not before an explicitly passed path
    * accepts both string or iterable for an explicitly passed path, or pathext
    * accepts an explicitly passed empty path, or pathext (either '' or [])
    * does not search ``PATH`` for files that have a path specified in their name already

    .. function:: which(file [, mode=os.F_OK | os.X_OK[, path=None[, extensions=None]]])

       Return a generator which yields full paths in which the *file* name exists
       in a directory that is part of the file name, or on *path*,
       and has the given *mode*.
       By default, *mode* matches an inclusive OR of os.F_OK and os.X_OK
        - an existing executable file.
       The *path* is, by default, the ``PATH`` variable on the platform,
       or the string/iterable passed in as *path*.
       In the event that a ``PATH`` variable is not found, :const:`os.defpath` is used.
       On Windows, a current directory is searched before using the ``PATH`` variable,
       but not before an explicitly passed *path*.
       The *pathext* is only used on Windows to match files with given extensions appended as well.
       It defaults to the ``PATHEXT`` variable, or the string/iterable passed in as *pathext*.
       In the event that a ``PATHEXT`` variable is not found, :const:`defpathext` is used.
"""
__docformat__ = 'restructuredtext en'
__all__ = 'which pathsep defpath defpathext F_OK R_OK W_OK X_OK'.split()

import sys
from os import access, defpath, pathsep, environ, F_OK, R_OK, W_OK, X_OK
from os.path import exists, dirname, split, join

windows = sys.platform.startswith('win')

defpathext = windows and '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC' or ''

def which(file, mode=F_OK | X_OK, path=None, pathext=None):
    """ Locate a file in a path supplied as a part of the file name,
        or the user's path, or a supplied path.
        The function yields full paths (not necessarily absolute paths),
        in which the given file matches a file in a directory on the path.

        >>> def test_which(expected, *args, **argd):
        ...     result = list(which(*args, **argd))
        ...     assert result == expected, '%s != %s' % (result, expected)

        >>> if windows: cmd = environ['COMSPEC']
        >>> if windows: test_which([cmd], 'cmd')
        >>> if windows: test_which([cmd], 'cmd.exe')
        >>> if windows: test_which([cmd], 'cmd', path=dirname(cmd))
        >>> if windows: test_which([cmd], 'cmd', pathext='.exe')

        >>> if windows: test_which([cmd], cmd)
        >>> if windows: test_which([cmd], cmd[:-4])

        >>> if windows: test_which([], 'cmd', path='<nonexistent>')
        >>> if windows: test_which([], 'cmd', pathext='<nonexistent>')
        >>> if windows: test_which([], '<nonexistent>/cmd')

        >>> if not windows: sh = '/bin/sh'
        >>> if not windows: test_which([sh], 'sh')
        >>> if not windows: test_which([sh], 'sh', path=dirname(sh))
        >>> if not windows: test_which([sh], 'sh', pathext='<nonexistent>')

        >>> if not windows: test_which([], 'sh', mode=W_OK)  # not running as root, are you?
        >>> if not windows: test_which([], 'sh', path='<nonexistent>')
        >>> if not windows: test_which([], '<nonexistent>/sh')
    """
    filepath, file = split(file)

    if filepath:
        path = (filepath,)
    elif path is None:
        path = environ.get('PATH', defpath).split(pathsep)
        if windows:
            if '.' not in path:
                path.insert(0, '')

            # given the quite usual mess in PATH on Windows, let's rather remove duplicates
            path, orig, seen = [], path, set()
            for dir in orig:
                if not dir.lower() in seen:
                    path.append(dir)
                    seen.add(dir.lower())
    elif isinstance(path, str):
        path = path.split(pathsep)

    if windows:
        if pathext is None:
            pathext = [''] + environ.get('PATHEXT', defpathext).lower().split(pathsep)
        elif isinstance(pathext, str):
            pathext = pathext.split(pathsep)
    else:
        pathext = ('',)

    for dir in path:
        basepath = join(dir, file)
        for ext in pathext:
            fullpath = basepath + ext
            if exists(fullpath) and access(fullpath, mode):
                yield fullpath

