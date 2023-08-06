"""

 PACKNET  -  c0mplh4cks

 MQTT

     #===#==============#
     # 7 # Application  #
     #===#==============#
     | 6 | Presentation |
     |---|--------------|
     | 5 | Session      |
     |---|--------------|
     | 4 | Transport    |
     |---|--------------|
     | 3 | Network      |
     |---|--------------|
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from struct import pack, unpack
from .standards import encode, decode







# === MQTT Header === #
class Header:
    def __init__(self, packet=b""):
        self.packet = packet

        self.type = 0
        self.flags = 0b0000
        self.length = 0
        self.payloadlen = 0
        self.data = b""



    def build(self):
        packet = []

        hf = (self.type << 4) + (self.flags)

        self.payloadlen = len(self.data)
        self.length = 2 + len(self.data)

        packet.insert(0, pack( ">B", hf ))              # Header flags
        packet.insert(1, pack( ">B", self.payloadlen )) # Payload length

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, hf               = i+1, packet[i]    # Header flags
        i, self.payloadlen  = i+1, packet[i]    # Payload length

        self.type = hf >> 4
        self.flags = hf - (self.type << 4)

        self.length = i
        return i







# === Connect === #
class Connect:
    def __init__(self, packet=b""):
        self.packet = packet

        self.version = 0
        self.flags = 0b00000000
        self.keepalive = 0
        self.protocollen = 0
        self.protocol = ""
        self.idlen = 0
        self.id = ""
        self.length = 0



    def build(self):
        packet = []

        self.protocollen = len(self.protocol)
        self.idlen = len(self.id)
        self.length = 8 + self.protocollen + self.idlen

        packet.insert(0, pack( ">H", self.protocollen ))    # Protocol length
        packet.insert(1, self.protocol.encode() )           # Protocol
        packet.insert(2, pack( ">B", self.version ))        # Version
        packet.insert(3, pack( ">B", self.flags ))          # Flags
        packet.insert(4, pack( ">H", self.keepalive ))      # Keep alive
        packet.insert(5, pack( ">H", self.idlen ))          # ID length
        packet.insert(6, self.id.encode() )                 # ID

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, plen             = i+2, unpack( ">H", packet[i:i+2] )[0]     # Protocol length
        i, self.protocol    = i+plen, packet[i:i+plen].decode()         # Protocol
        i, self.version     = i+1, packet[i]                            # Version
        i, self.flags       = i+1, packet[i]                            # Flags
        i, self.keepalive   = i+2, unpack( ">H", packet[i:i+2] )[0]     # Keep alive
        i, idlen            = i+2, unpack( ">H", packet[i:i+2] )[0]     # ID length
        i, self.id          = i+idlen, packet[i:i+idlen].decode()       # ID

        self.protocollen = plen
        self.idllen = idlen

        self.length = i

        return i







# === ConnectACK === #
class ConnectACK:
    def __init__(self, packet=b""):
        self.packet = packet

        self.flags = 0b00000000
        self.returncode = 0
        self.length = 0



    def build(self):
        packet = []

        self.length = 2

        packet.insert(0, pack( ">B", self.flags ))      # Flags
        packet.insert(1, pack( ">B", self.returncode )) # Return code

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.flags       = i+1, packet[i]    # Flags
        i, self.returncode  = i+1, packet[i]    # Return code

        self.length = i

        return i







# === Subscribe === #
class Subscribe:
    def __init__(self, packet=b""):
        self.packet = packet

        self.id = 0
        self.topiclen = 0
        self.topic = ""
        self.reqqos = 0
        self.length = 0



    def build(self):
        packet = []

        self.topiclen = len(self.topic)
        self.length = 5 + self.topiclen

        packet.insert(0, pack( ">H", self.id ))         # Message identifier
        packet.insert(1, pack( ">H", self.topiclen ))   # Topic length
        packet.insert(2, self.topic.encode() )          # Topic
        packet.insert(4, pack( ">B", self.reqqos ))     # Requested QoS

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.id      = i+2, unpack( ">H", packet[i:i+2] )[0]     # Message identifier
        i, tlen         = i+2, unpack( ">H", packet[i:i+2] )[0]     # Topic length
        i, self.topic   = i+tlen, packet[i:i+tlen].decode()         # Topic
        i, self.reqqos  = i+1, packet[i]                            # Requested QoS

        self.topiclen = tlen

        self.length = i

        return i







# === SubscribeACK === #
class SubscribeACK:
    def __init__(self, packet=b""):
        self.packet = packet

        self.id = 0
        self.grantqos = 0
        self.length = 0



    def build(self):
        packet = []

        self.length = 3

        packet.insert(0, pack( ">H", self.id ))         # Message identifier
        packet.insert(1, pack( ">B", self.grantqos ))   # Granted QoS

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, self.id          = i+2, unpack( ">H", packet[i:i+2] )[0]     # Message identifier
        i, self.grantqos    = i+1, packet[i]                            # Granted QoS

        self.length = i

        return i







# === Publish === #
class Publish:
    def __init__(self, packet=b""):
        self.packet = packet

        self.topiclen = 0
        self.topic = ""
        self.msg = ""
        self.length = 0



    def build(self):
        packet = []

        self.topiclen = len(self.topic)
        self.length = 2 + len(self.msg) + self.topiclen

        packet.insert(0, pack( ">H", self.topiclen ))
        packet.insert(1, self.topic.encode() )
        packet.insert(2, self.msg.encode() )

        self.packet = b"".join(packet)

        return self.packet



    def read(self):
        packet = self.packet
        i = 0

        i, tlen         = i+2, unpack( ">H", packet[i:i+2] )[0]         # Topic length
        i, self.topic   = i+tlen, packet[i:i+tlen].decode()             # Topic
        i, self.msg     = i+len( packet[i:] ), packet[i:].decode()      # Message

        self.topiclen = tlen

        self.length = i

        return i
