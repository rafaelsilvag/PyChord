# -*- coding: utf-8 -*-
import socket
import struct
from array import array
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP protocol
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',12345))
while(True):
    # Handle sockets
    data, addr = s.recvfrom(1024)
    #print int(bytearray(data)[0])
    #res = struct.unpack("bi",data)
    print data
    print addr
