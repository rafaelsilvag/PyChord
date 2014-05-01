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
    p2pClient = ClientP2P("127.0.0.1")

    ## ENVIO
    #data = struct.pack("!BI",0,2323)
    #p2pClient.sendMessage(data)
    #data = struct.pack("!BIIIII",1,2222,2323,ip2int("192.168.0.1"),2424,ip2int("192.168.0.2"))
    #p2pClient.sendMessage(data)
    #data = struct.pack("!BIII",2,2222,ip2int("127.0.0.22"),2323)
    #p2pClient.sendMessage(data)
    #data = struct.pack("!BIII",3,2222,2424,ip2int("177.2.2.1"))
    #p2pClient.sendMessage(data)

    ## RECEBIMENTO
    #data = struct.pack("!BIIII",64,2323,ip2int("177.2.2.1"),2424,ip2int("177.2.2.33"))
    #p2pClient.sendMessage(data)
    #data = struct.pack("!BI",65,2323)
    #p2pClient.sendMessage(data)
    data = struct.pack("!BIII",66,2323,2424,ip2int("177.2.2.1"))
    p2pClient.sendMessage(data)
    #data = struct.pack("!BI",67,2323)
    #p2pClient.sendMessage(data)
        #bytes("64"+str(int(res.hexdigest(),16))[0:]))

    #+str(int(res.hexdigest(), 16))

if __name__ == "__main__":
    main()
