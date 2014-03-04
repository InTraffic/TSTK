#!/usr/bin/env python
# vi: spell spl=en

"""Classes and functions to get pages from the OBIS web portal.
"""

import urllib2  # This does all the heavy lifting.
import logging

class Portal(object):
    """Interface to RITA Webportal
    """

    def __init__( self, portal_id = None, ):
        self.portal_url = 'http://www.nstrein_%s.ns.nl' % str( portal_id )
        self.logger     = logging.getLogger( 'otis_player.portal' )

    def fetch( self ):
        """Fetch the current version of the portal page"""
        url_file = urllib2.urlopen( self.portal_url )
        content = url_file.read()
        url_file.close()
        self.logger.info( "fetched page " + content )
        return content

