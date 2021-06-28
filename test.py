#import sys
#sys.path.insert(0, "pycharon")

import pycharon
from socket import gethostname
from random import randint

IP = gethostname()
PORT = 53000 + randint(0, 100)

server = pycharon.server.Server(PORT, 10)
client = pycharon.client.Client()

server.start()
client.connect(IP, PORT)
