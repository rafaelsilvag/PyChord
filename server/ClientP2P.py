__author__ = 'Rafael S. Guimaraes'
import socket
import struct

class ClientP2P(object):
    def __init__(self, host):
        self.host = host
        self.port = 12345
        self.sock = None

    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

    def sendJoinMsg(self, msg):
        # Envio Update
        if(msg['type'] == 0 ):
            sendMsg = struct.pack("!BI",int(msg('type')),int(msg['id_node']))
        elif(msg['type'] == 64):
            #Resposta Join
            sendMsg = struct.pack("!BIIII",int(msg('type')),int(msg['id_node_sucessor']),
                                  self.ip2int(msg['ip_node_sucessor']),int(msg['id_node_predecessor']),
                                  self.ip2int(msg['ip_node_predecessor']))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendLeaveMsg(self, msg):
        # Envio Leave
        if(msg['type'] == 1):
            sendMsg = struct.pack("!BIIIII",int(msg('type')),int(msg['id_node_out']),
                                  int(msg['id_node_sucessor']),self.ip2int(msg['ip_node_sucessor']),
                                  int(msg['id_node_predecessor'],self.ip2int(msg['ip_node_predecessor'])))
        elif(msg['type'] == 65):
            #Resposta Leave
            sendMsg = struct.pack("!BI",int(msg('type')),int(msg['id_src_msg']))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendLookupMsg(self, msg):
        # Envio Lookup
        if(msg['type'] == 2):
            sendMsg = struct.pack("!BIII",int(msg('type')),int(msg['src_id_searched']),
                                  self.ip2int(msg['src_ip_searched']),int(msg['id_searched']))
        elif(msg['type'] == 66):
            #Resposta Lookup
            sendMsg = struct.pack("!BIII",int(msg('type')),int(msg['id_searched']),
                                  int(msg['id_sucessor_searched']),self.ip2int(msg['ip_sucessor_searched']))


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendUpdateMsg(self, msg):
        # Envio Join
        if(msg['type'] == 3):
            #Resposta Join
            sendMsg = struct.pack("!BIII",int(msg('type')),int(msg['id_src']),
                                  int(msg['id_new_sucessor']),self.ip2int(msg['ip_new_sucessor']))
        elif(msg['type'] == 67):
            sendMsg = struct.pack("!BI",int(msg('type')),int(msg['id_src_msg']))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendMessage(self, msg):
        """
            Send Message using UDP Protocol
        """
        # Socket Object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))
        res = self.sock.send(msg)
        self.sock.close()