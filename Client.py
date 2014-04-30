__author__ = 'Rafael S. Guimaraes'

import hashlib
import struct
import socket
from server.ClientP2P import ClientP2P

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def main():
    res = hashlib.md5()
    res.update(str('192.168.0.22'))
    p2pClient = ClientP2P("192.168.1.146")

    p2pClient.sendMessage("0"+str(int(res.hexdigest(),16))[0:4])

    #+str(int(res.hexdigest(), 16))

if __name__ == "__main__":
    main()
