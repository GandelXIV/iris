import socket
from threading import Thread
import time
import pycharon.com

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, ip, port):
        self.socket.connect((ip, port))
        self.connected = True
        t = Thread(target=self.__update_caller)
        t.start()

    def __update_caller(self):
        delta = 0
        while self.connected:
            start_update = time.time()
            self.__update(delta)
            delta = time.time() - start_update

    def __update(self, delta):
        packets = pycharon.com.recv(self.socket)
        if packets != []:
            for packet in packets:
                self.on_packet(packet)

        self.update(delta)

    def on_packet(self, packet):
        print(packet)

    def update(self, delta):
        pass
