"""

 PACKNET  -  c0mplh4cks

 IPv6

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
from .standards import encode, decode







# === IPv6 Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.src = ["", 0, ""]
        self.dst = ["", 0, ""]
        self.version = 6
        self.traffic = 0b00000000
        self.flowlabel = 0b00010111010011101110
        self.nextheader = 58
        self.hop = 64
        self.length = 0
        self.payloadlen = 0
        self.data = b""



    def build(self):
        packet = []

        vtf = (self.version << 24) + (self.traffic << 20) + (self.flowlabel)

        self.payloadlen = len(self.data)
        self.length = 40 + self.payloadlen

        packet.insert(0, pack( ">L", vtf ))             # Version, Traffic class & Flowlabel
        packet.insert(1, pack( ">H", self.payloadlen )) # Data length
        packet.insert(2, pack( ">B", self.nextheader )) # Next header
        packet.insert(3, pack( ">B", self.hop ))        # Hop limit
        packet.insert(4, encode.ipv6( self.src[0] ))    # Source IP
        packet.insert(5, encode.ipv6( self.dst[0] ))    # Target IP
        packet.insert(6, self.data )                    # Data

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, vtf              = i+4, unpack( ">L", packet[i:i+4] )[0]     # Version, Traffic class & Flowlabel
        i, self.payloadlen  = i+2, unpack( ">H", packet[i:i+2] )[0]     # Data length
        i, self.nextheader  = i+1, packet[i]                            # Next header
        i, self.hop         = i+1, packet[i]                            # Hop limit
        i, self.src[0]      = i+16, decode.ipv6( packet[i:i+16] )       # Source IP
        i, self.dst[0]      = i+16, decode.ipv6( packet[i:i+16] )       # Target IP
        i, self.data        = i+len( packet[i:] ), packet[i:]           # Data

        self.version = vtf >> 24
        self.traffic = (vtf - self.version) >> 20
        self.flowlabel = (vtf - self.version - self.traffic)

        self.length = i

        return i
