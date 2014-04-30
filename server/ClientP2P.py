__author__ = 'rafaelguimaraes'
import socket

class ClientP2P(object):
    def __init__(self, host):
        self.host = host
        self.port = 12345
        self.sock = None

    def sendMessage(self, msg):
        """
            Send Message UDP Protocol
        """
        # Socket Object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))
        res = self.sock.send(msg)
        self.sock.close()