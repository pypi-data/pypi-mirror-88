"""

 PACKNET  -  c0mplh4cks

 ICMP

     .---.--------------.
     | 7 | Application  |
     |---|--------------|
     | 6 | Presentation |
     |---|--------------|
     | 5 | Session      |
     |---|--------------|
     | 4 | Transport    |
     #===#==============#
     # 3 # Network      #
     #===#==============#
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode, checksum







# === ICMP Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.type = 0
        self.code = 0
        self.checksum = 0
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 4 + len(self.data)

        packet.insert(0, pack( ">B", self.type ))       # Type
        packet.insert(1, pack( ">B", self.code ))       # Code
        packet.insert(3, self.data )                    # Data
        packet.insert(2, checksum( [                    # Checksum
            *packet,
            encode.ipv6( self.src[0] ),
            encode.ipv6( self.dst[0] ),
            pack( ">B", 58 ),
            pack( ">", self.length )
        ] ))

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.type        = i+1, packet[i]                            # Type
        i, self.code        = i+1, packet[i]                            # Code
        i, self.checksum    = i+2, unpack( ">H", packet[i:i+2] )[0]     # Checksum
        i, self.data        = i+len( packet[i:]), packet[i:]            # Data

        self.length = i

        return i







# === Echo === #
class Echo:
    def __init__(self, packet=b""):
        self.packet = packet

        self.id = 0
        self.seq = 0
        self.length = 0
        self.data = b""



    def build(self):
        packet = []

        self.length = 4 + len(self.data)

        packet.insert(0, pack( ">H", self.id ))             # Identifier
        packet.insert(1, pack( ">H", self.seq ))            # Sequence number
        packet.insert(3, self.data )                        # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.id          = i+2, unpack( ">H", packet[i:i+2] )[0]     # Identifier
        i, self.seq         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Sequence number
        i, self.data        = i+len( packet[i:] ), packet[i:]           # Data

        self.length = i

        return i
