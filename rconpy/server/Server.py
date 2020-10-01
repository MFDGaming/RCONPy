from rconpy.protocol.AuthPacket import AuthPacket
from rconpy.protocol.AuthResponsePacket import AuthResponsePacket
from rconpy.protocol.ExecCommandPacket import ExecCommandPacket
from rconpy.protocol.ResponsePacket import ResponsePacket
from rconpy.server.ServerInterface import ServerInterface
from rconpy.server.ServerSocket import ServerSocket
from threading import Thread

class Server(Thread):
    address = None
    password = None
    interface = None
    socket = None

    def __init__(self, address, password, interface = None):
        super().__init__()
        self.address = address
        self.password = password
        if interface != None:
            self.interface = interface
        else:
            self.interface = ServerInterface()
        self.start()
        
    def handleAuthPacket(self, data, connection, address):
        self.interface.onOpenConnection(address)
        decodedPacket = AuthPacket()
        decodedPacket.buffer = data
        decodedPacket.decodePayload()
        if decodedPacket.body != self.password:
            id = -1
            self.interface.onInvalidPassword(address)
        else:
            id = decodedPacket.id
        packet = AuthResponsePacket()
        packet.length = decodedPacket.length
        packet.id = id
        packet.encodePayload()
        self.interface.onConnected(address)
        return packet.buffer

    def handleExecCommandPacket(self, data, connection, address):
        decodedPacket = ExecCommandPacket()
        decodedPacket.buffer = data
        decodedPacket.decodePayload()
        packet = ResponsePacket()
        packet.length = decodedPacket.length
        packet.id = decodedPacket.id
        packet.body = self.interface.onCommand(decodedPacket.body)
        packet.encodePayload()
        return packet.buffer

    def handle(self, data, connection, address):
        type = int.from_bytes(data[8:11], "little")
        if type == AuthPacket.type:
            self.socket.sendBuffer(self.handleAuthPacket(data, connection, address), connection)
        elif type == ExecCommandPacket.type:
            self.socket.sendBuffer(self.handleExecCommandPacket(data, connection, address), connection)
        else:
            print(f"Received unknown packet type: {str(type)}")
        
    def run(self):
        self.socket = ServerSocket(self.address)
        while True:
            connection, clientAddress = self.socket.socket.accept()
            while True:
                data = self.socket.receiveBuffer(connection)
                if data:
                    self.handle(data, connection, clientAddress)
                else:
                    break
