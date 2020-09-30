from rconpy.protocol.Packet import Packet
from rconpy.protocol.PacketTypes import PacketTypes

class AuthResponsePacket(Packet):
    type = PacketTypes.AuthResponsePacket

    length = None
    id = None

    def encodePayload(self):
        self.putInt(self.length)
        self.putInt(self.id)
        self.putTriad(self.type)
        self.putString("\x00")
        self.putShort(0)

    def decodePayload(self):
        self.length = self.getInt()
        self.id = self.getInt()
        self.offset += 5