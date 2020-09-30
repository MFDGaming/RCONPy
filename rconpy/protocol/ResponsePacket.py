from rconpy.protocol.Packet import Packet
from rconpy.protocol.PacketTypes import PacketTypes

class ResponsePacket(Packet):
    type = PacketTypes.ResponsePacket

    length = None
    id = None
    body = None

    def encodePayload(self):
        self.putInt(self.length)
        self.putInt(self.id)
        self.putTriad(self.type)
        self.putString(self.body)
        self.putShort(0)

    def decodePayload(self):
        self.length = self.getInt()
        self.id = self.getInt()
        self.offset += 3
        self.body = self.getString()
        self.offset += 2
        
