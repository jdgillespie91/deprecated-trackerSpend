# This script is used to remove the Icon\r files from all directories.
import fnmatch
import os


matches = []
for root, dirnames, filenames in os.walk(os.environ.get("BASE_DIRECTORY")):
    for filename in fnmatch.filter(filenames, 'Icon\r'):
        os.remove((os.path.join(root, filename)))