from struct import pack, unpack, calcsize 
import sys

class Binary:
    BIG_ENDIAN = 0x00
    LITTLE_ENDIAN = 0x01
    ENDIANNESS = BIG_ENDIAN if sys.byteorder == "big" else LITTLE_ENDIAN
    
    @staticmethod
    def checkLength(data: bytes, expect: int):
        length = len(data)
        assert (length == expect), 'Expected ' + str(expect) + 'bytes, got ' + str(length)
    
    @staticmethod
    def readTriad(data: bytes) -> int:
        Binary.checkLength(data, 3)
        return unpack('<l', data + b'\x00')[0]

    @staticmethod
    def writeTriad(value: int) -> bytes:
        return pack('<l', value)[0:-1]
    
    @staticmethod
    def readByte(data: bytes) -> int:
        Binary.checkLength(data, 1)
        return ord(data)

    @staticmethod
    def writeByte(value: int) -> bytes:
        return chr(value).encode()
    
    @staticmethod
    def readShort(data: bytes) -> int:
        Binary.checkLength(data, 2)
        return unpack('<h', data)[0]

    @staticmethod
    def writeShort(value: int) -> bytes:
        return pack('<h', value)

    @staticmethod
    def readInt(data: bytes) -> int:
        Binary.checkLength(data, 4)
        return unpack('<l', data)[0]

    @staticmethod
    def writeInt(value: int) -> bytes:
        return pack('<l', value)