# vi: spell spl=en
#

"""Telegrams that are exchanged between FOCON and OBIS.
"""

from struct import pack, unpack

#-----------------------------------------------------------------------------
# These two are no longer used, and therefore not implemented.
ID_REQUEST_PA  = 1         # PI -> OB
ID_END_OF_PA   = 2         # PI -> OB

#-----------------------------------------------------------------------------
ID_REQUEST_DVA                 =  3 # OB -> PI
ID_END_OF_DVA                  =  4 # OB -> PI
ID_REQUEST_ESD_OBIS            =  5 # OB -> PI
ID_ESD_TEXT                    =  6 # OB -> PI
ID_RESPONSE_DVA                = 13 # PI -> OB
ID_RESPONSE_ESD_OBIS           = 14 # PI -> OB
ID_RESPONSE_END_OF_DVA         = 15 # PI -> OB
ID_RESPONSE_ESD_TEXT           = 16 # PI -> OB
ID_REQUEST_PIAES_STATUS        = 17 # OB -> PI
ID_RESPONSE_PIAES_STATUS       = 18 # PI -> OB
ID_REQUEST_VERSION             = 19 # OB -> PI
ID_RESPONSE_PIAES_VERSION      = 20 # PI -> OB

# These are not implemented
ID_UPLOAD_LIST_OF_DESTINATIONS = 7  # OB -> PI
ID_RECEIVED_LIST_OF_DESTINATIONS = 8  # PI -> OB
ID_UPLOAD_LIST_PREDEFINEDS     = 9  # OB -> PI
ID_RECEIVED_LIST_PREDEFINEDS   = 10 # PI -> OB
ID_UPLOAD_PARAMETERS           = 11 # OB -> PI
ID_RECEIVED_PARAMETERS         = 12 # PI -> OB

#-------------------------------------------------------------------------------
ADDRESS_OBIS  = 'OB'
ADDRESS_PIAES = 'PI'

class Telegram( object ):
    """The telegrams exchanged between OBIS and FOCON

    Attributes:

    * source -- Source of the telegram (two characters)
    * through -- Address of a optional via-node
    * destination -- Destination of the telegram (two characters)
    * id_message -- ID of the message
    * data_length -- length of the body
    * body -- body of the telegram (series of bytes)
    """
    def __init__( self, blob = None ):
        if blob :
            ( source0, source1, through0, through1, 
              destination0, destination1,
              self.data_length, 
              self.id_message ) = unpack( 'cccccchh', blob[0:10] )
            self.source      = source0 + source1
            self.through     = through0 + through1
            self.destination = destination0 + destination1
            if len( blob ) > 10 :
                self.body        = blob[10:]
                self.data_length = len( self.body )
            else :
                self.body = None
                self.data_length = 0
        else :
            self.source      = None
            self.through     = 'NO' # Not used so always 'NO'
            self.destination = None
            self.data_length = None
            self.id_message  = None
            self.body        = None

    def to_blob( self ):
        """Convert the telegram to a blob of data ready to be send over TCP"""
        if self.body :
            self.data_length = len( self.body )
        blob = pack( 'cccccchh', self.source[0], self.source[1],
                self.through[0], self.through[1],
                self.destination[0], self.destination[1],
                self.data_length,
                self.id_message )
        if self.body :
            blob = blob + self.body
        return blob


#-----------------------------------------------------------------------------

class Telegram_REQUEST_DVA( Telegram ):
    """Telegram from OBIS to PIAES to request use of the DVA
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.source = ADDRESS_OBIS
            self.destination = ADDRESS_PIAES
            self.id_message = ID_REQUEST_DVA
            self.body = "<request_DVA>1</request_DVA>"
            self.data_length = len( self.body )


class Telegram_RESPONSE_DVA( Telegram ):
    """Telegram from PIAES to OBIS to allow use DVA
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_OBIS
            self.source = ADDRESS_PIAES
            self.id_message = ID_REQUEST_DVA
            self.data_length = 0

    def set_available( self, available ):
        """Set availability of the DVA
        """
        if available :
            self.body = "<response_DVA>1</response_DVA>"
        else :
            self.body = "<response_DVA>0</response_DVA>"
        self.data_length = len( self.body )


class Telegram_END_DVA( Telegram ):
    """Telegram from OBIS to PIAES to release the use of the DVA
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.source      = ADDRESS_OBIS
            self.destination = ADDRESS_PIAES
            self.id_message  = ID_END_OF_DVA
            self.body = "<end_of_DVA>1</end_of_DVA>"
            self.data_length = len( self.body )


class Telegram_RESPONSE_END_DVA( Telegram ):
    """Telegram from PIAES to OBIS to acknowledge the release
    the use of the DVA.
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_OBIS
            self.source      = ADDRESS_PIAES
            self.id_message  = ID_RESPONSE_END_OF_DVA
            self.body = None
            self.data_length = 0


class Telegram_RESPONSE_ESD_OBIS( Telegram ):
    """Telegram from PIAES to OBIS to allow control over BBA.
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_OBIS
            self.source      = ADDRESS_PIAES
            self.id_message  = ID_RESPONSE_ESD_OBIS
            self.body = None
            self.data_length = 0

    def set_available( self, available ):
        """Set availability of the Text Display (BBA)
        """
        if available :
            self.body = "<response_ESD_OBIS>1</response_ESD_OBIS>"
        else :
            self.body = "<response_ESD_OBIS>0</response_ESD_OBIS>"
        self.data_length = len( self.body )


class Telegram_REQUEST_ESD_OBIS( Telegram ):
    """Telegram from OBIS to PIAES to request control over BBA.
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_PIAES
            self.source      = ADDRESS_OBIS 
            self.id_message  = ID_REQUEST_ESD_OBIS
            self.body = None
            self.data_length = 0


class Telegram_ESD_TEXT( Telegram ):
    """Telegram from OBIS to PIAES to set the destination.
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_PIAES 
            self.source      = ADDRESS_OBIS
            self.id_message  = ID_ESD_TEXT
            self.body = None
            self.data_length = 0


class Telegram_RESPONSE_ESD_TEXT( Telegram ):
    """Telegram from PIAES to OBIS to acknowledge setting the destination.
    """
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_OBIS
            self.source      = ADDRESS_PIAES
            self.id_message  = ID_RESPONSE_ESD_TEXT
            self.body = None
            self.data_length = 0


class Telegram_REQUEST_PIAES_STATUS( Telegram ):
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_PIAES 
            self.source      = ADDRESS_OBIS
            self.id_message  = ID_REQUEST_PIAES_STATUS
            self.body = None
            self.data_length = 0


class Telegram_RESPONSE_PIAES_STATUS( Telegram ):
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_OBIS 
            self.source      = ADDRESS_PIAES 
            self.id_message  = ID_RESPONSE_PIAES_STATUS
            self.body = None
            self.data_length = 0


class Telegram_REQUEST_VERSION( Telegram ):
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_PIAES
            self.source      = ADDRESS_OBIS 
            self.id_message  = ID_REQUEST_VERSION
            self.body = None
            self.data_length = 0


class Telegram_RESPONSE_PIAES_VERSION( Telegram ):
    def __init__( self, blob = None ):
        Telegram.__init__( self, blob )
        if blob :
            pass
        else :
            self.destination = ADDRESS_OBIS
            self.source      = ADDRESS_PIAES 
            self.id_message  = ID_RESPONSE_PIAES_VERSION
            self.body = None
            self.data_length = 0


#------------------------------------------------------------------------
def factory( blob ):
    """Telegram factory.

    Makes a telegram of the correct type (class) based
    on the data in the blob of bytes.
    """
    ( unused1, id_message ) = unpack( 'hh', blob[6:10] )
    if id_message == ID_REQUEST_DVA :
        return Telegram_REQUEST_DVA( blob )
    elif id_message == ID_REQUEST_DVA :
        return Telegram_RESPONSE_DVA( blob )
    elif id_message == ID_END_OF_DVA :
        return Telegram_END_DVA( blob )
    elif id_message == ID_RESPONSE_END_OF_DVA :
        return Telegram_RESPONSE_END_DVA( blob )
    elif id_message == ID_ESD_TEXT :
        return Telegram_ESD_TEXT( blob )
    elif id_message == ID_RESPONSE_ESD_TEXT :
        return Telegram_RESPONSE_ESD_TEXT( blob )
    elif id_message == ID_REQUEST_ESD_OBIS:
        return Telegram_REQUEST_ESD_OBIS( blob )
    elif id_message == ID_RESPONSE_ESD_OBIS:
        return Telegram_REQUEST_ESD_OBIS( blob )
    elif id_message == ID_REQUEST_VERSION:
        return Telegram_REQUEST_VERSION( blob )
    elif id_message == ID_RESPONSE_PIAES_VERSION:
        return Telegram_RESPONSE_PIAES_VERSION( blob )
    elif id_message == ID_REQUEST_PIAES_STATUS:
        return Telegram_REQUEST_PIAES_STATUS( blob )
    elif id_message == ID_RESPONSE_PIAES_STATUS:
        return Telegram_RESPONSE_PIAES_STATUS( blob )
    else :
        return None

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    pass


