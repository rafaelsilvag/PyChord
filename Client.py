__author__ = 'rafaelguimaraes'

from client.ClientP2P import ClientP2P
import hashlib
import struct
import socket

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

def main():
    res = hashlib.md5()
    res.update(str(ip2int('127.0.0.1')))
    p2pClient = ClientP2P("127.0.0.1")

    p2pClient.sendMessage("0 "+str(ip2int('127.0.0.2')))

    #+str(int(res.hexdigest(), 16))

if __name__ == "__main__":
    main()
