import socket
from datetime import datetime
from threading import Thread
import time
import iris.com


INT_TYPE = int(1)

class Server:
    def __init__(self, port, max_clients, logs_on = True):
        self.ip = ""
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

        self.running = False
        self.paused = False

        self.max_clients = max_clients
        self.logs_on = logs_on

    def log(self, message):
        if self.logs_on:
            print("[{}] ".format( datetime.now().time() ) + message)

    def send(self, client_or_id, data): # you can pass a socket or int id as arg
        if type(client_or_id) == INT_TYPE:
            iris.com.send(self.clients[client_or_id], data)
        else:
            iris.com.send(client_or_id, data)

    def start(self):
        self.log("Starting server...")

        self.socket.bind((self.ip, self.port))
        self.running = True

        handle_clients_caller_thread = Thread(target=self.__handle_clients_caller)
        update_caller_thread = Thread(target=self.__update_caller)
        handle_packets_caller_thread = Thread(target=self.__handle_packets_caller)
        handle_clients_caller_thread.start()
        update_caller_thread.start()
        handle_packets_caller_thread.start()

        self.log("Done!")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.pause()
        self.running = False

    def __handle_clients_caller(self):
        while self.running:
            while not self.paused:
                self.__handle_clients()

    def __handle_clients(self):
        if len(self.clients) < self.max_clients:
            self.socket.listen()
            c, a = self.socket.accept()
            self.log("New connection {}".format(a))
            self.clients.append(c)

    def __handle_packets_caller(self):
        while self.running:
            while not self.paused:
                self.__handle_packets()

    def __handle_packets(self):
        for cid in range(len(self.clients)):
            client = self.clients[cid]
            packets = iris.com.recv(client)
            if packets != []:
                for packet in packets:
                    self.on_packet(cid, packet)

    def on_packet(self, client_id, packet):
        self.log("New packet from client with id {}: {}".format(client_id, packet))

    def __update_caller(self):
        delta = 0
        while self.running:
            while not self.paused:
                update_start = time.time()
                self.__update(delta)
                delta = time.time() - update_start

    def __update(self, delta):
        self.update(delta)

    def update(self, delta):
        pass
