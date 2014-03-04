#!/usr/bin/env python2
#
"""
Module to get and set the OTIS version.

This module is used to show the current OTIS version in the
logging of the various modules, and to set the new version
when release a new version of OTIS.
"""
import os, sys


usage = """
Usage
    Set OTIS version
    ./otis_version.py update <version string>

    Get OTIS version
    ./otis_version.py
"""

#------------------------------------------------------------------

def version_file():
    """Construct name of the version file"""
    return 'version.txt'

def get_version():
    """Read otis version from version file"""
        try:
            verf = file( version_file(), 'r')
            current_version = verf.read().strip()
            verf.close()
        except IOError:
            current_version = 'Unknown'


    return current_version

def set_version( new_version ):
    """Write new version to version file"""
    try:
        file(version_file(),'w+').write("%s\n" % new_version )
    except IOError:
        sys.stderr.write( "Update failed!" )
        sys.exit(1)

#------------------------------------------------------------------

if __name__ == "__main__":
    path = 'version.txt'
        if len(sys.argv) == 3:
            if 'update' == sys.argv[1]:
                set_otis_version( sys.argv[2] )
            else:
                message = "Unknown command %s" 
                sys.stderr.write( message % sys.argv[1] )
                sys.exit(1)
        else:
            print otis_version()

