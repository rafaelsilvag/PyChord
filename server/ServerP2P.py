__author__ = 'Rafael S. Guimaraes'

import socket
import struct


class ServerP2P():
    def __init__(self, node):
        self.conn = None
        self.stop = False
        self.node = node

    def lookupMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Lookup
        if(typeMSG == 2 ):
            self.node.updateScreen("Received: SEND UPDATE "+msg['data'][1:])
        elif(typeMSG == 66):
            #Resposta Lookup
            self.node.updateScreen("Received: ANSWER UPDATE "+msg['data'][1:])

    def leaveMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Leave
        if(typeMSG == 1 ):
            self.node.updateScreen("Received: SEND LEAVE "+msg['data'][1:])
        elif(typeMSG == 65):
            #Resposta Leave
            self.node.updateScreen("Received: ANSWER LEAVE "+msg['data'][1:])

    def updateMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Update
        if(typeMSG == 3 ):
            self.node.updateScreen("Received: SEND UPDATE "+msg['data'][1:])
        elif(typeMSG == 67):
            #Resposta Update
            self.node.updateScreen("Received: ANSWER UPDATE "+msg['data'][1:])

    def joinMessage(self, msg):
        ## Desmembrando mensagem de envio
        typeMSG = int(msg['data'][0:1])
        # Envio Join
        if(typeMSG == 0 ):
            self.node.updateScreen("Received: JOIN "+msg['data'][1:])
        elif(typeMSG == 64):
            #Resposta Update
            self.node.updateScreen("Received: ANSWER JOIN "+msg['data'][1:])

    def run(self):
        HOST = ''
        PORT = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP protocol
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))

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