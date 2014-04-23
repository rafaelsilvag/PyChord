__author__ = 'rafaelguimaraes'

import threading
import socket
import struct
from select import select
from time import sleep

class ServerP2P(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = 1
        self.conn = None
        self.addr = None

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
        #self.conn, self.addr = s.accept()
        # Select loop for listen
        while(self.running == True):
            # Handle sockets
            data, addr = s.recvfrom(1024)
            res = data.split(' ')
            codeMessage = int(res[0])
            if codeMessage == 0:
                print "Received: Join %s" % (res[1])
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

    def kill(self):
        self.running = 0