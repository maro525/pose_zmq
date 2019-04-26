import zmq
import json

socket = None


class ZMQ_SENDER():

    def __init__(self):
        self.context = None

    def initialize(self, ip, port):
        global socket
        if socket is not None or self.context is not None:
            self.close()
        self.context = zmq.Context()
        socket = self.context.socket(zmq.PUB)
        socket.connect("tcp://" + ip + ":" + str(port))
        print("zmq connected to", ip, port)

    def send(self, d):
        global socket
        sd = json.dumps(d)
        socket.send_string(sd)
        # print("send json", sd)
        # socket.send_string("hello abcde")
        # print("send hello")

    def close(self):
        global socket
        socket.close()
        self.context.destroy()
        socket = None
        self.context = None
