import socket, pickle

PICKLE_SEPARATOR = b'.'

def send(target_socket, data):
    target_socket.send(pickle.dumps(data))

def recv(target_socket, buffer=1024):
    packets = []
    try:
        raw = target_socket.recv(buffer)
    except BlockingIOError: return []
    if raw == b'':
        return packets
    for packet in raw.split(PICKLE_SEPARATOR)[:-1]:
        packets.append(pickle.loads(packet + PICKLE_SEPARATOR))
    return packets
