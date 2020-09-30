from rconpy.utils.Binary import Binary

class BinaryStream:
    offset = 0
    buffer = b""
    
    def __init__(self, buffer: bytes = b"", offset: int = 0):
        self.offset = offset
        self.buffer = buffer
       
    def reset(self):
        self.buffer = b""
        self.offset = 0
       
    def rewind(self):
        self.offset = 0
       
    def setOffset(self, offset: int):
        self.offset = offset
      
    def setBuffer(self, buffer: bytes = b"", offset: int = 0):
        self.buffer = buffer
        self.offset = offset
        
    def getOffset(self) -> int:
        return self.offset
      
    def getBuffer(self) -> bytes:
        return self.buffer
       
    def get(self, length) -> bytes:
        if length < 0:
            self.offset = len(self.buffer) - 1
            return ""
        length = min(length, len(self.buffer) - self.offset)
        self.offset += length
        return self.buffer[self.offset - length:self.offset]
       
    def getRemaining(self) -> str:
        s = self.buffer[self.offset:]
        if s == False:
            raise Exception("No bytes left to read")
        self.offset = len(self.buffer)
        return s
    
    def put(self, data: bytes):
        self.buffer += data
      
    def getByte(self):
        return Binary.readByte(self.get(1))
    
    def putByte(self, value):
        self.put(Binary.writeByte(value))
      
    def getTriad(self):
        return Binary.readTriad(self.get(3))
    
    def putTriad(self, value):
        self.put(Binary.writeTriad(value))
    
    def getShort(self):
        return Binary.readShort(self.get(2))
    
    def putShort(self, value):
        self.put(Binary.writeShort(value))
      
    def getInt(self):
        return Binary.readInt(self.get(4))
    
    def putInt(self, value):
        self.put(Binary.writeInt(value))
      
    def feof(self):
        return self.offset < 0 or self.offset >= len(self.buffer)
