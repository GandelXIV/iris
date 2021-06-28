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
        self.socket.setblocking(False)
        self.connected = True
        update_caller_thread = Thread(target=self.__update_caller)
        handle_packets_caller_thread = Thread(target=self.__handle_packets_caller)
        update_caller_thread.start()
        handle_packets_caller_thread.start()

    def send(self, data):
        pycharon.com.send(self.socket, data)

    def __handle_packets_caller(self):
        while self.connected:
            self.__handle_packets()

    def __handle_packets(self):
        packets = pycharon.com.recv(self.socket)
        if packets != []:
            for packet in packets:
                self.on_packet(packet)

    def on_packet(self, packet):
        print(packet)

    def __update_caller(self):
        delta = 0
        while self.connected:
            start_update = time.time()
            self.__update(delta)
            delta = time.time() - start_update

    def __update(self, delta):
        self.update(delta)

    def update(self, delta):
        pass
