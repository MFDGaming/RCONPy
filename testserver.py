from rconpy.server.Server import Server
from rconpy.server.ServerInterface import ServerInterface

class TestServer(ServerInterface):
    def __init__(self):
        Server(("0.0.0.0", 25575), "12345", self)

    def onOpenConnection(self, address):
        print("Awaiting RCON connection from " + address[0] + ":" + str(address[1]))

    def onInvalidPassword(self, address):
        print("Incorrect password from " + address[0] + ":" + str(address[1]))

    def onConnected(self, address):
        print("Connection established from " + address[0] + ":" + str(address[1]))

    def onCommand(self, command):
        return command

TestServer()
