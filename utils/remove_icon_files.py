"""
This module deletes all Icon\r files contained in any subdirectory of the
directory above this one (which is should be the base directory). The answer
borrows from http://goo.gl/cRbszb.
"""
import fnmatch
import os


for root, dirnames, filenames in os.walk('..'):
    for filename in fnmatch.filter(filenames, 'Icon\r'):
        os.remove((os.path.join(root, filename)))
