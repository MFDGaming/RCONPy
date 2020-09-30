from rconpy.protocol.AuthPacket import AuthPacket
from rconpy.protocol.AuthResponsePacket import AuthResponsePacket
from rconpy.protocol.ExecCommandPacket import ExecCommandPacket
from rconpy.protocol.ResponsePacket import ResponsePacket
from rconpy.server.ServerSocket import ServerSocket
from threading import Thread

class Server(Thread):
    address = None
    password = None
    socket = None

    def __init__(self, address, password):
        super().__init__()
        self.address = address
        self.password = password
        self.start()
        
    def handleAuthPacket(self, data):
        print("CONNECTING...")
        decodedPacket = AuthPacket()
        decodedPacket.buffer = data
        decodedPacket.decodePayload()
        if decodedPacket.body != self.password:
            id = -1
            print("INVALID PASSWORD!")
        else:
            id = decodedPacket.id
        packet = AuthResponsePacket()
        packet.length = decodedPacket.length
        packet.id = id
        packet.encodePayload()
        print("CONNECTED!")
        return packet.buffer

    def handleExecCommandPacket(self, data):
        decodedPacket = ExecCommandPacket()
        decodedPacket.buffer = data
        decodedPacket.decodePayload()
        packet = ResponsePacket()
        packet.length = decodedPacket.length
        packet.id = decodedPacket.id
        packet.body = decodedPacket.body
        packet.encodePayload()
        print(packet.body)
        return packet.buffer

    def handle(self, data, connection, address):
        type = int.from_bytes(data[8:11], "little")
        if type == AuthPacket.type:
            self.socket.sendBuffer(self.handleAuthPacket(data), connection)
        elif type == ExecCommandPacket.type:
            self.socket.sendBuffer(self.handleExecCommandPacket(data), connection)
        else:
            raise Exception(f"Received unknown packet type: {str(type)}")
        
    def run(self):
        self.socket = ServerSocket(self.address)
        while True:
            connection, clientAddress = self.socket.socket.accept()
            while True:
                data = self.socket.receiveBuffer(connection)
                if data:
                    self.handle(data, connection, address)
                else:
                    break
