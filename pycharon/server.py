import socket
from datetime import datetime
from threading import Thread
import time
import pycharon.com


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

    def start(self):
        self.log("Starting server...")

        self.socket.bind((self.ip, self.port))
        self.running = True

        tl = Thread(target=self.__listen_caller)
        tm = Thread(target=self.__update_caller)
        tl.start()
        tm.start()

        self.log("Done!")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.pause()
        self.running = False

    def __listen_caller(self):
        while self.running:
            while not self.paused:
                self.__listen()

    def __update_caller(self):
        delta = 0
        while self.running:
            while not self.paused:
                update_start = time.time()
                self.__update(delta)
                delta = time.time() - update_start

    def __listen(self):
        if len(self.clients) < self.max_clients:
            self.socket.listen()
            c, a = self.socket.accept()
            self.log("New connection {}".format(a))
            self.clients.append(c)

    def __update(self, delta):
        for cid in range(len(self.clients)):
            client = self.clients[cid]
            responses = pycharon.com.recv(client)
            if responses != []:
                for response in responses:
                    self.on_packet(cid, response)

        self.update(delta)

    def on_packet(self, client_id, packet):
        self.log("New packet from client with id {}: {}".format(client_id, packet))

    def update(self, delta):
        pass
