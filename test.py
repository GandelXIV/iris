#import sys
#sys.path.insert(0, "pycharon")

import iris
from random import randint
from threading import Thread

IP = "localhost"
PORT = 53001

class MyClient(iris.client.Client):
    def update(self, delta):
        self.send(input())

    def on_packet(self, packet):
        print(packet)

class MyServer(iris.server.Server):
    def on_packet(self, client_id, packet):
        for client in self.clients:
            self.send(client, packet)


server = MyServer(PORT, 10)
client = MyClient()

def start_client():
    client.connect(IP, PORT)

def start_server():
    server.start()

client_thread = Thread(target=start_client)
server_thread = Thread(target=start_server)

server_thread.start()
client_thread.start()
