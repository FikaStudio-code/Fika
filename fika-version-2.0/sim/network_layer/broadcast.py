import socket
import json

class Broadcast:
    def __init__(self, name):
        self.name = name
        with open("/sim/ip_info_test.txt", "r") as f:
            info = json.loads(f.read())
        with open("/sim/logicnet_info_test.txt", "r") as f:
            my_info = json.loads(f.read())
        self.peer = dict()
        self.ip = info[name][0]
        self.port = info[name][1]
        my_info = my_info[name]
        for i in my_info:
            self.peer[i] = info[i]

    def get_my_info(self):
        return self.ip, self.port

    def send_message(self, message, peer):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(peer)
        s.sendall(message.encode())
        s.close()

    def broadcast(self, message, sender):
        for p in self.peer.values():
            peer = tuple(p)
            if (peer != (self.ip, self.port) and peer != sender):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(peer)
                    s.sendall(message.encode())
                    s.close()
                except:
                    with open("/sim/output/{0}_log.txt".format(self.name), "a") as f:
                        f.write("\nConnection failed...")
            else:
                continue
