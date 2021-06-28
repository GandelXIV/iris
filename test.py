#import sys
#sys.path.insert(0, "pycharon")

import pycharon
from random import randint

IP = "localhost"
PORT = 53001

class MyClient(pycharon.client.Client):
    def update(self, delta):
        self.send(input())

    def on_packet(self, packet):
        print(packet)

class MyServer(pycharon.server.Server):
    def on_packet(self, client_id, packet):
        for client in self.clients:
            self.send(client, packet)


if input("server/client:") == "server":
    server = MyServer(PORT, 10)
    server.start()
else:
    client = MyClient()
    client.connect(IP, PORT)
