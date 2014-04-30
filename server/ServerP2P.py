__author__ = 'Rafael S. Guimaraes'

import socket
from ClientP2P import ClientP2P

class ServerP2P():
    def __init__(self, node):
        self.__HOST = ''
        self.__PORT = 12345
        self.conn = None
        self.stop = False
        self.node = node
        self.client_p2p = ClientP2P("127.0.0.1")

    def lookupMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Lookup
        if(typeMSG == 2 ):
            src_id_searched = int(msg['data'][1:5])
            src_ip_searched = int(msg['data'][5:9])
            id_search = int(msg['data'][9:13])
            self.node.updateScreen("Received: SEND UPDATE "+msg['data'][1:])
        elif(typeMSG == 66):
            #Resposta Lookup
            id_searched = int(msg['data'][1:5])
            id_sucessor_searched = int(msg['data'][5:9])
            ip_sucessor_searched = int(msg['data'][9:13])
            self.node.updateScreen("Received: ANSWER UPDATE "+msg['data'][1:])

    def leaveMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Leave
        if(typeMSG == 1 ):
            id_node_out = int(msg['data'][1:5])
            id_node_sucessor = int(msg['data'][5:9])
            ip_node_sucessor = int(msg['data'][9:13])
            id_node_predecessor = int(msg['data'][13:17])
            ip_node_predecessor = int(msg['data'][17:21])
            self.node.updateScreen("Received: SEND LEAVE "+msg['data'][1:])
        elif(typeMSG == 65):
            #Resposta Leave
            id_src_msg = int(msg['data'][1:5])
            self.node.updateScreen("Received: ANSWER LEAVE "+msg['data'][1:])

    def updateMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Update
        if(typeMSG == 3 ):
            id_src = int(msg['data'][1:5])
            id_new_sucessor = int(msg['data'][5:9])
            ip_new_sucessor = int(msg['data'][9:13])
            self.node.updateScreen("Received: SEND UPDATE "+msg['data'][1:])
        elif(typeMSG == 67):
            #Resposta Update
            id_src_msg = int(msg['data'][1:5])
            self.node.updateScreen("Received: ANSWER UPDATE "+msg['data'][1:])

    def joinMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Join
        if(typeMSG == 0 ):
            id_node = int(msg['data'][1:5])
            self.node.updateScreen("Received: JOIN "+msg['data'][1:])
        elif(typeMSG == 64):
            #Resposta Join
            id_node_sucessor = int(msg['data'][5:9])
            ip_node_sucessor = int(msg['data'][9:13])
            id_node_predecessor = int(msg['data'][13:17])
            ip_node_predecessor = int(msg['data'][17:21])
            self.node.updateScreen("Received: ANSWER JOIN "+msg['data'][1:])

    def run(self):
        ## Cria o Socket UDP na porta 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP protocol
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.__HOST,self.__PORT))

        while(self.stop == False):
            # Handle sockets
            data, addr = s.recvfrom(1024)
            msg = {'addr':addr, 'data':data}
            try:
                codeMessage = int(data[0:1])
                if codeMessage == 0:
                    self.joinMessage(msg)
                elif codeMessage == 1:
                    self.leaveMessage(msg)
                elif codeMessage == 2:
                    self.lookupMessage(msg)
                elif codeMessage == 3:
                    self.updateMessage(msg)
                elif codeMessage == 64:
                    self.joinMessage(msg)
                elif codeMessage == 65:
                    self.leaveMessage(msg)
                elif codeMessage == 66:
                    self.lookupMessage(msg)
                elif codeMessage == 67:
                    self.updateMessage(msg)
                else:
                    print "Received: Invalid code!"
            except ValueError, e:
                continue