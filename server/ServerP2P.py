__author__ = 'Rafael S. Guimaraes e Joao Paulo de Brito Goncalves'

import socket
import struct
from ClientP2P import ClientP2P

class ServerP2P(object):
    def __init__(self, node):
        self.__HOST = ''
        self.__PORT = 12345
        self.conn = None
        self.stop = False
        self.node = node
        self.client_p2p = ClientP2P("127.0.0.1")

    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

    def joinMessage(self, msg):
        # Envio Join
        typeMSG = bytearray(msg['data'])
        if(int(typeMSG[0]) == 0 ):
            res = struct.unpack("!BI",msg['data'])
            id_node = int(res[1])
            # Responder o Join informando os dados do sucessor a antecessor.
            self.node.updateScreen("Received: JOIN "+str(id_node))
        elif(int(typeMSG[0]) == 64):
            #Resposta Join
            res = struct.unpack("!BIIII",msg['data'])
            id_node_sucessor = int(res[1])
            ip_node_sucessor = self.int2ip(int(res[2]))
            id_node_predecessor = int(res[3])
            ip_node_predecessor = self.int2ip(int(res[4]))
            # Enviar um msg de Update para o antecessor informando que voce e o novo sucessor no anel.
            # Enviar um msg de Updata para o sucessor informando que voce e o novo antecessor no anel.
            self.node.updateScreen("Received: ANSWER JOIN "+str(ip_node_sucessor))

    def leaveMessage(self, msg):
        # Envio Leave
        typeMSG = bytearray(msg['data'])
        if(int(typeMSG[0]) == 1):
            res = struct.unpack("!BIIIII",msg['data'])
            id_node_out = int(res[1])
            id_node_sucessor = int(res[2])
            ip_node_sucessor = self.int2ip(int(res[3]))
            id_node_predecessor = int(res[4])
            ip_node_predecessor = self.int2ip(int(res[5]))
            # Ao receber a mensagem de Leave tenho que verificar se sou o sucessor ou antecessor da origem da mensagem.
            # Se for antecessor: Atualizar o campo do sucessor com a informacao do sucessor do no que deixou o anel.
            # Se for sucessor: Atualizar o campo do antecessor com a informacao do antecessor do no que deixou o anel.
            self.node.updateScreen("Received: LEAVE IP_S:"+str(ip_node_sucessor)+
                                   " IP_P:"+str(ip_node_predecessor))
        elif(int(typeMSG[0]) == 65):
            #Resposta Leave
            res = struct.unpack("!BI",msg['data'])
            id_src_msg = int(res[1])
            # Comparar o ID_SRC_MSG com os ID do meu sucessor e antecessor.
            self.node.updateScreen("Received: ANSWER LEAVE "+str(id_src_msg))

    def lookupMessage(self, msg):
        # Envio Lookup
        typeMSG = bytearray(msg['data'])
        if(int(typeMSG[0]) == 2):
            res = struct.unpack("!BIII",msg['data'])
            src_id_searched = int(res[1])
            src_ip_searched = self.int2ip(int(res[2]))
            id_searched = int(res[3])
            if(self.node.code == self.node.idSuccessor and self.node.code == self.node.idPredecessor ):
                # Sou o no inicial
                pass
            elif(self.node.code < src_id_searched and self.node.idPredecessor > self.node.code):
                # Eu respondo o Lookup para o ID do procurado.
                pass
            elif(self.node.code >= src_id_searched):
                # Meu id Maior que ID do procurado = Responderei o Lookup para o ID do procurado.
                pass
            else:
                # Repassa a Mensagem de Lookup para o Sucessor.
                pass

            self.node.updateScreen("Received: LOOKUP "+str(src_ip_searched))
        elif(int(typeMSG[0]) == 66):
            #Resposta Lookup
            res = struct.unpack("!BIII",msg['data'])
            id_searched = int(res[1])
            id_sucessor_searched = int(res[2])
            ip_sucessor_searched = self.int2ip(int(res[3]))
            ## Ao receber a resposta de lookup envio uma mensagem de Join para o IP sucessor procurado
            #
            self.node.updateScreen("Received: ANSWER LOOKUP "+str(ip_sucessor_searched))

    def updateMessage(self, msg):
        # Envio Update
        typeMSG = bytearray(msg['data'])
        if(int(typeMSG[0]) == 3 ):
            res = struct.unpack("!BIII",msg['data'])
            id_src = int(res[1])
            id_new_sucessor = int(res[2])
            ip_new_sucessor = self.int2ip(int(res[3]))
            # Atualizar a informacao do meu No que o novo sucessor e o que esta descrito no cabecalho
            self.node.updateScreen("Received: UPDATE ID_S:"+str(id_new_sucessor)+
                                   " IP_S:"+str(ip_new_sucessor))
        elif(int(typeMSG[0]) == 67):
            #Resposta Update
            res = struct.unpack("!BI",msg['data'])
            id_src_msg = int(res[1])
            # ID_ORIGEM_MENSAGEM e igual ao valor no campo ID_ANTECESSOR do meu No
            self.node.updateScreen("Received: ANSWER UPDATE "+str(id_src_msg))

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
                codeMessage = bytearray(data)
                if int(codeMessage[0]) == 0:
                    self.joinMessage(msg)
                elif int(codeMessage[0]) == 1:
                    self.leaveMessage(msg)
                elif int(codeMessage[0]) == 2:
                    self.lookupMessage(msg)
                elif int(codeMessage[0]) == 3:
                    self.updateMessage(msg)
                elif int(codeMessage[0]) == 64:
                    self.joinMessage(msg)
                elif int(codeMessage[0]) == 65:
                    self.leaveMessage(msg)
                elif int(codeMessage[0]) == 66:
                    self.lookupMessage(msg)
                elif int(codeMessage[0]) == 67:
                    self.updateMessage(msg)
                else:
                    print "Received: Invalid code!"
            except ValueError, e:
                continue
