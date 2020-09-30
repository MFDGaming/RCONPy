from rconpy.utils.BinaryStream import BinaryStream

class Packet(BinaryStream):
    type = -1

    def getString(self):
        value = self.buffer[self.offset:-2].decode("ascii")[1:]
        self.offset += len(value) + 1
        return value

    def putString(self, value):
        self.put(b"\x00" + value.encode("ascii"))

    def decodePayload(self): pass

    def encodePayload(self): pass