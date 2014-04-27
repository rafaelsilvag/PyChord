__author__ = 'Rafael S. Guimaraes'

import socket
import struct


class ServerP2P():
    def __init__(self, node):
        self.conn = None
        self.addr = None
        self.raddr = None
        self.stop = False
        self.node = node

    def ip2int(addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

    def run(self):
        HOST = ''
        PORT = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP protocol
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))

        while(self.stop == False):
            # Handle sockets
            data, addr = s.recvfrom(1024)
            try:
                codeMessage = int(data[0:1])
            except ValueError, e:
                codeMessage = 100
                continue
            if codeMessage == 0:
                self.node.updateScreen("Received: Join "+data[1:5])
            elif codeMessage == 1:
                print "Received: Leave"
            elif codeMessage == 2:
                print "Received: Lookup"
            elif codeMessage == 3:
                print "Received: Update"
            elif codeMessage == 64:
                print "Received: Join Answer"
            elif codeMessage == 65:
                print "Received: Leave Answer"
            elif codeMessage == 66:
                print "Received: Lookup Answer"
            elif codeMessage == 67:
                print "Received: Update Answer"
            else:
                print "Received: Invalid code!"