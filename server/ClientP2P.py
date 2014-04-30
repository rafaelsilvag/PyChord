__author__ = 'Rafael S. Guimaraes'
import socket

class ClientP2P(object):
    def __init__(self, host):
        self.host = host
        self.port = 12345
        self.sock = None

    def sendLookupMsg(self, msg):
        # Envio Lookup
        if(msg['type'] == 2):
            sendMsg = str(msg('type'))+str(msg['src_id_search'])+\
                      str(msg['src_ip_search'])+str(msg['id_search'])
        elif(msg['type'] == 66):
            #Resposta Lookup
            sendMsg = str(msg('type'))+str(msg['id_searched'])+\
                      str(msg['id_sucessor_searched'])+str(msg['ip_sucessor_searched'])

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendLeaveMsg(self, msg):
        # Envio Leave
        if(msg['type']== 1 ):
            sendMsg = str(msg('type'))+str(msg['id_node_out'])+\
                      str(msg['id_node_sucessor'])+str(msg['ip_node_sucessor'])+\
                      str(msg['id_node_predecessor'])+str(msg['ip_node_predecessor'])
        elif(msg['type'] == 65):
            #Resposta Leave
            sendMsg = str(msg('type'))+str(msg['id_src_msg'])

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendJoinMsg(self, msg):
        # Envio Update
        if(msg['type'] == 3 ):
            sendMsg = str(msg('type'))+str(msg['id_src'])+\
                      str(msg['id_new_sucessor'])+str(msg['ip_new_sucessor'])
        elif(msg['type'] == 67):
            #Resposta Update
            sendMsg = str(msg('type'))+str(msg['id_src_msg'])

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((msg['dest_ip_addr'], self.port))
        res = self.sock.send(sendMsg)
        self.sock.close()

    def sendUpdateMsg(self, msg):
        # Envio Join
        if(msg['type'] == 0 ):
            sendMsg = str(msg('type'))+str(msg['id_node'])
        elif(msg['type'] == 64):
            #Resposta Join
            sendMsg = str(msg('type'))+str(msg['id_node_sucessor'])+\
                      str(msg['ip_node_sucessor'])+str(msg['id_node_predecessor'])+\
                      str(msg['ip_node_predecessor'])

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