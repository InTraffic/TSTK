# vi: spell spl=en
#

""" Message data structure
"""

from struct import pack, unpack

#-----------------------------------------------------------------------------

# Message types
SNDTYPE_STATUS  = 0x01
SNDTYPE_TIJD    = 0x02
SNDTYPE_PRES    = 0x03
SNDTYPE_STORING = 0x04
SNDTYPE_MCN     = 0x05
SNDTYPE_MT      = 0x06
SNDTYPE_EVENTS  = 0x07
SNDTYPE_SET_BST = 0x08
SNDTYPE_SW_DIA  = 0x09
# Error message
SNDTYPE_ERROR   = 0xFF

# Message use by OTIS
# This is not part of the official IRS
# but used by OTIS to signal a broken message.
SNDTYPE_ILLEGAL = 0x0F 


# Translate table that maps the message type number
# to a string from the IRS
message_type_string = {
        0x01:"SNDTYPE_STATUS",
        0x02:"SNDTYPE_TIJD",
        0x03:"SNDTYPE_PRES",
        0x04:"SNDTYPE_STORING",
        0x05:"SNDTYPE_MCN",
        0x06:"SNDTYPE_MT",
        0x07:"SNDTYPE_EVENTS",
        0x08:"SNDTYPE_SET_BST",
        0x09:"SNDTYPE_SW_DIA",
        0x0F:"SNDTYPE_ILLEGAL",
        0xFF:"SNDTYPE_ERROR" }

#-----------------------------------------------------------------------
# State message fields
#-----------------------------------------------------------------------
# - Bedrijftoestand (BT)
STATE_BT_DIENST_MET_CABINE      = 0x07
STATE_BT_DIENST_ZONDER_CABINE   = 0x06
STATE_BT_GEREED_CONT            = 0x05
STATE_BT_GEREED                 = 0x04
STATE_BT_REINIGEN               = 0x03
STATE_BT_BIJVULLEN              = 0x02
STATE_BT_SLUIMEREN              = 0x01

#-----------------------------------------------------------------------
# - Bestemmingsstatus (BS)
#-----------------------------------------------------------------------
STATE_BS_IDLE                   = 0x00
STATE_BS_BUSY                   = 0x01
STATE_BS_OK                     = 0x02
STATE_BS_NOK                    = 0x03

#-----------------------------------------------------------------------
# - Orientation (OR)
#-----------------------------------------------------------------------
STATE_OR_UNKNOWN                = 0x00
STATE_OR_MBVK1_NO_MST           = 0x01
STATE_OR_MBVK2_NO_MST           = 0x02
STATE_OR_MBVK1_MST              = 0x11
STATE_OR_MBVK2_MST              = 0x12
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
# Failure message fields
#-----------------------------------------------------------------------
# - Class types
FAILURE_CLASS_A                 = 'A'
FAILURE_CLASS_B                 = 'B'
FAILURE_CLASS_C                 = 'C'
FAILURE_CLASS_D                 = 'D'
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
# Error Codes
#-----------------------------------------------------------------------
ERROR_MESSAGE                   = 0x01
ERROR_PARAMS                    = 0x02
ERROR_MT                        = 0x03
ERROR_MASTER                    = 0x04
ERROR_CC                        = 0x05
ERROR_TIME                      = 0x06

# CRC table
crc16tab = (0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280,
        0xC241, 0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481,
        0x0440, 0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81,
        0x0E40, 0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880,
        0xC841, 0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81,
        0x1A40, 0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80,
        0xDC41, 0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680,
        0xD641, 0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081,
        0x1040, 0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281,
        0x3240, 0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480,
        0xF441, 0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80,
        0xFE41, 0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881,
        0x3840, 0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80,
        0xEA41, 0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81,
        0x2C40, 0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681,
        0x2640, 0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080,
        0xE041, 0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281,
        0x6240, 0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480,
        0xA441, 0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80,
        0xAE41, 0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881,
        0x6840, 0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80,
        0xBA41, 0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81,
        0x7C40, 0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681,
        0x7640, 0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080,
        0xB041, 0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280,
        0x9241, 0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481,
        0x5440, 0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81,
        0x5E40, 0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880,
        0x9841, 0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81,
        0x4A40, 0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80,
        0x8C41, 0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680,
        0x8641, 0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081,
        0x4040)


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


class Message( object ) :
    """ Base class for message data structure """

    def __init__ ( self ) :
        self.msg_type   = None
        self.crc        = None

    @classmethod
    def crc_check( cls, blob ):
        """ Perfom a CRC check on a message """
        crc_value = 0xFFFF
        for val in blob:
            tmp = crc_value ^ (ord(val))
            crc_value = (crc_value >> 8) ^ crc16tab[tmp & 0xFF]

        return crc_value



#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

class CBoxMessage( Message ) :
    """ Data structure message for communication between C-Box (OBIS)
        to CC.

    Attributes:

    * msg_type  -- Type of message (1 byte)
    * par_len   -- Lengt of the data (parameters) field (1 byte)
    * param     -- Data field (1 byte)
    * CRC       -- CRC of message (2 bytes)

    """

    def __init__( self, blob = None):
        Message.__init__( self )
        if blob :
            (self.msg_type, self.par_len) = unpack('>BB', blob[0:2])

            #calcsize('BB') == 2
            self.par = blob[2:(2+self.par_len)]

            #Calculate CRC of msg excluding the CRC field (last two bytes) 
            #self.crc = (ord(blob[-1]) << 8) | ord(blob[-2])
            self.crc = unpack('>H', blob[-2:])[0]
        else :
            self.par_len    = None
            self.par        = None

    def to_blob( self ):
        """Convert the message to a blob of data ready to 
            be send over TCP
        """

        if self.par :
            self.par_len = len( self.par )
        else :
            self.par_len = 0x0000
        if self.msg_type == None:
            self.msg_type = 0
        blob = pack( '>BB', self.msg_type, self.par_len)
        if self.par:
            blob = blob + self.par

        #crc_blob = self.crc_check(blob)
        crc_blob = super(CBoxMessage, self).crc_check(blob)
        blob = blob + pack('H', crc_blob)

        return blob

#-----------------------------------------------------------------------

class CBox_Request_State( CBoxMessage ) :
    """Request 'Status' from CC"""

    def __init__( self, blob = None ):
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_STATUS
            self.par_len    = 15
            self.par        = None

class CBox_Request_Time( CBoxMessage ) :
    """Request 'Tijd' from CC"""

    def __init__( self, blob = None ):
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_TIJD
            self.par_len    = 0
            self.par        = None

class CBox_Request_Pres( CBoxMessage ) :
    """Request 'Prestatietellers' from CC"""

    def __init__( self, blob = None ):
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_PRES
            self.par_len    = 0
            self.par        = None

class CBox_Request_Storing( CBoxMessage ) :
    """Request 'storingen' from CC"""

    def __init__( self, blob = None ):
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_STORING
            self.par_len    = 0
            self.par        = None

class CBox_Request_Monitor_MCN( CBoxMessage ) :
    """Request Monitor MCN""" 
    def __init__( self, blob = None ) :
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_MCN
            self.par_len    = 0
            self.par        = None

class CBox_Request_Events( CBoxMessage ) :
    """Request Events""" 
    def __init__( self, blob = None ) :
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_EVENTS
            self.par_len    = 0
            self.par        = None

class CBox_Request_Switch_DIA( CBoxMessage ) :
    """Request Switch DIA""" 
    def __init__( self, blob = None ) :
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_SW_DIA
            self.par_len    = 0
            self.par        = None

class CBox_Illegal_Message( CBoxMessage ) :
    """A way to signal an Illegal Message to the player"""
    def __init__( self, blob = None ) :
        CBoxMessage.__init__( self, blob )
        self.msg_type   = SNDTYPE_ILLEGAL
        self.par_len    = 0
        self.par        = None

#-----------------------------------------------------------------------

class CBox_Request_Monitor_MT( CBoxMessage ) :
    """ Request Monitor MT digital/analogue measuring points """ 
    
    def __init__( self, blob = None ) :
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_MT
            self.par_len    = 0
            self.par        = None

#-----------------------------------------------------------------------

class CBox_Request_Destination( CBoxMessage ):
    """ Request Set destination """

    def __init__( self, blob = None ) :
        CBoxMessage.__init__( self, blob )
        if blob :
            pass
        else :
            self.msg_type   = SNDTYPE_SET_BST
            self.par_len    = 0x00
            self.par        = None


#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

class CCMessage( Message ) :
    """The messages exchanged between OBIS and CC
 )
    Attributes:

    * train_no  -- Number of train (2 bytes)
    * msg_type  -- Copy of type of message coming from OBIS
    * data_len  -- Length of the data field (2 bytes)
    * data      -- Actual data of the message
    * CRC       -- CRC of message (2 bytes)

    """

    def __init__( self, blob = None ):
        Message.__init__( self )
        if blob :
            ( self.train_no, self.msg_type, self.data_len) = \
                    unpack( '>HBH', blob[0:5] )

            #calcsize('HBH') == 6
            self.data = blob[5:(5+self.data_len)] 

            #Calculate CRC of msg excluding the CRC field (last two bytes) 
            #self.crc = (ord(blob[-1]) << 8) | ord(blob[-2])
            self.crc = unpack('>H', blob[-2:])[0]
        else :
            self.train_no   = None
            self.data_len   = None
            self.data       = None

    def to_blob( self ):
        """ Convert the message to a blob of data ready to 
            be send over TCP
        """

        if self.data :
            self.data_len = len( self.data )
        else:
            self.data_len = 0x0000

        blob = pack( '>HBH', self.train_no, self.msg_type, self.data_len )
        if self.data:
            blob = blob + self.data

        #crc_blob = self.crc_check(blob)
        crc_blob = super(CCMessage, self).crc_check(blob)
        blob = blob + pack('H', crc_blob)

        return blob


#-----------------------------------------------------------------------

class CC_Reply_State( CCMessage ):
    """ Message for synchronizing CC """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_STATUS
            self.data_len   = 0x0010
            self.data       = None

    def request_error_count( self ):
        """ Request the number of error from a State message """
        err_count = (ord(self.data[6]) << 8) | ord(self.data[7])

        return err_count

    def request_events_count( self ):
        """ Request the number of events from a State message """
        ev_count = (ord(self.data[8]) << 8) | ord(self.data[9])

        return ev_count

    def request_version( self ):
        """ Request the version number from a State message """
        sw_version = (ord(self.data[10]) << 8) | ord(self.data[11])

        return sw_version


#-----------------------------------------------------------------------    


class CC_Reply_Time( CCMessage ):
    """ Reply Time to C-Box (OBIS) """

    def __init__ ( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_TIJD
            self.data_len   = 0x0006
            self.data       = None

#-----------------------------------------------------------------------------

class CC_Reply_Pres( CCMessage ):
    """ Reply 'prestatietellers' to C-Box 
        The order of sending is equal to the order of the list,
        'if' these are sorted by name
    """
    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_PRES
            self.data_len   = 0x0000
            self.data       = None

    #def request_pres_list()
    #lenght of list * 4
    #    return len(self.data) * 4


class CC_Reply_Storing( CCMessage ):
    """ Reply a failure assertion """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_STORING
            self.data_len   = 0x0000
            self.data       = None

class CC_Reply_Monitor_MCN( CCMessage ):
    """ Reply monitor data to C-Box (OBIS)
        Requesting these data is only possible in the master train
        For each request a 'copy' of the data is sent back to the C-Box
    """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_MCN
            self.data_len   = 0x0000
            self.data       = None

    def reply_monitor_mcn( self ):
        """ Returns MCN data """ 
        return self.data

class CC_Reply_Monitor_MT( CCMessage ):
    """ Reply monitor measure points
        This message contains analog and digital measuring points
    """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_MT
            self.data_len   = 0x0000
            self.data       = None


class CC_Reply_Events( CCMessage ):
    """Reply events to C-Box (OBIS)
    CC can have 40 events in total, which can be sent all
    at once in one message, but not necessarily
    """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no = None
            self.msg_type = SNDTYPE_EVENTS
            self.data     = None
            self.data_len = 1


class CC_Reply_Destination( CCMessage ):
    """Reply Set Destination """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_SET_BST
            self.data_len   = 0x0001
            self.data       = None

class CC_Reply_Switch_DIA( CCMessage ):
    """ Reply diagnosis data """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_SW_DIA
            self.data_len   = 0x0001
            self.data       = None

class CC_Reply_Error( CCMessage ):
    """Reply Error message

       This message is returned by an unknown request or in case of an
       incorrect request
    """

    def __init__( self, blob = None ):
        CCMessage.__init__( self, blob )
        if blob:
            pass
        else:
            self.train_no   = None
            self.msg_type   = SNDTYPE_ERROR
            self.data_len   = 0x0001
            self.data       = str( bytearray( ERROR_MESSAGE ) ) #default 0x01 (FOUT_BERICHT)

#-----------------------------------------------------------------------------


def request_factory( blob ):
    """Create an object of the proper class
    based on a blob of data c-box data
    """
    msg_type = (unpack( 'B', blob[0] ))[0]
    if   msg_type == SNDTYPE_STATUS :
        message = CBox_Request_State( blob )
    elif msg_type == SNDTYPE_TIJD :
        message = CBox_Request_Time( blob )
    elif msg_type == SNDTYPE_PRES :
        message = CBox_Request_Pres( blob )
    elif msg_type == SNDTYPE_STORING :
        message = CBox_Request_Storing( blob )
    elif msg_type == SNDTYPE_MCN :
        message = CBox_Request_Monitor_MCN( blob )
    elif msg_type == SNDTYPE_MT :
        message = CBox_Request_Monitor_MT( blob )
    elif msg_type == SNDTYPE_EVENTS :
        message = CBox_Request_Events( blob )
    elif msg_type == SNDTYPE_SET_BST :
        message = CBox_Request_Destination( blob )
    elif msg_type == SNDTYPE_SW_DIA :
        message = CBox_Request_Switch_DIA( blob )
    else :
        message = CBox_Illegal_Message( blob )

    return message


def response_factory( blob ):
    """Create an object of the proper class
    based on a blob of cc-data.
    """
    msg_type = (unpack( 'B', blob[2] ))[0]
    message = None
    if   msg_type == SNDTYPE_STATUS :
        message = CC_Reply_State( blob )
    elif msg_type == SNDTYPE_TIJD :
        message = CC_Reply_Time( blob )
    elif msg_type == SNDTYPE_PRES :
        message = CC_Reply_Pres( blob )
    elif msg_type == SNDTYPE_STORING :
        message = CC_Reply_Storing( blob )
    elif msg_type == SNDTYPE_MCN :
        message = CC_Reply_Monitor_MCN( blob )
    elif msg_type == SNDTYPE_MT :
        message = CC_Reply_Monitor_MT( blob )
    elif msg_type == SNDTYPE_EVENTS :
        message = CC_Reply_Events( blob )
    elif msg_type == SNDTYPE_SET_BST :
        message = CC_Reply_Destination( blob )
    elif msg_type == SNDTYPE_SW_DIA :
        message = CC_Reply_Switch_DIA( blob )
    elif msg_type  == SNDTYPE_ERROR:
        message = CC_Reply_Error( blob )
    else :
        pass

    return message


if __name__ == "__main__":
    pass

