"""
This script is used to remove the Icon\r files from all directories within the
base directory. The answer borrows from http://goo.gl/cRbszb.
"""
import fnmatch
import os
from configs.base_config import base_dir


for root, dirnames, filenames in os.walk(base_dir):
    for filename in fnmatch.filter(filenames, 'Icon\r'):
        os.remove((os.path.join(root, filename)))