# -*- coding: utf-8 -*-
__author__ = "Rafael S. Guimarães e João Paulo de Brito Gonçalves"

import socket
import struct
from server.ClientP2P import ClientP2P


class ServerP2P(object):
    """
    Class Server P2P - Work 01
    """

    def __init__(self, node):
        self.__HOST = ""
        self.__PORT = 12345
        # Cria o Socket UDP na porta 12345
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP protocol
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.__HOST, self.__PORT))
        self.conn = None
        self.stop = False
        self.node = node
        self.client_p2p = ClientP2P("127.0.0.1", self.s)

    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

    def joinMessage(self, msg):
        # Envio da mensagem Join
        typeMSG = bytearray(msg["data"])
        if int(typeMSG[0]) == 0:
            res = struct.unpack("!BI", msg["data"])
            id_node = int(res[1])
            # Responder a mensagem Join informando os dados do sucessor a antecessor.
            # Vou atualizar o campo antecessor do nó que inserirá o novo nó no anel com o ID do novo nó.
            # Verifico se sou o unico no na rede: O antecessor e o sucessor sao iguais.
            # Responde o Join
            rmsg = {
                "dest_ip_addr": msg["addr"],
                "type": 64,
                "id_node_sucessor": self.node.code,
                "ip_node_sucessor": self.node.ipAddrNode,
                "id_node_predecessor": self.node.idPredecessor,
                "ip_node_predecessor": self.node.ipAddrPredecessor,
            }
            self.client_p2p.sendJoinMsg(rmsg)
            # Alterar valor do Antecessor
            self.node.idPredecessor = id_node
            self.node.ipAddrPredecessor = msg["addr"]
            self.node.updateScreen("Received: JOIN " + str(id_node))
        elif int(typeMSG[0]) == 64:
            # Resposta da mensagem Join
            res = struct.unpack("!BIIII", msg["data"])
            id_node_sucessor = int(res[1])
            ip_node_sucessor = self.int2ip(int(res[2]))
            id_node_predecessor = int(res[3])
            ip_node_predecessor = self.int2ip(int(res[4]))
            # Atualiza as informacoes do meu no
            self.node.idSuccessor = id_node_sucessor
            self.node.ipAddrSuccessor = ip_node_sucessor
            self.node.idPredecessor = id_node_predecessor
            self.node.ipAddrPredecessor = ip_node_predecessor
            # Enviar um msg de Update para o antecessor informando que voce e o novo sucessor no anel. (COD 3)
            rmsg = {
                "dest_ip_addr": ip_node_predecessor,
                "type": 3,
                "id_src": self.node.code,
                "id_new_sucessor": self.node.code,
                "ip_new_sucessor": self.node.ipAddrNode,
            }
            self.client_p2p.sendUpdateMsg(rmsg)

            self.node.updateScreen(
                "Received: ANSWER JOIN - UPDATE TO" + str(ip_node_sucessor)
            )

    def leaveMessage(self, msg):
        # Envio Leave
        typeMSG = bytearray(msg["data"])
        if int(typeMSG[0]) == 1:
            res = struct.unpack("!BIIIII", msg["data"])
            id_node_out = int(res[1])
            id_node_sucessor = int(res[2])
            ip_node_sucessor = self.int2ip(int(res[3]))
            id_node_predecessor = int(res[4])
            ip_node_predecessor = self.int2ip(int(res[5]))
            # Ao receber a mensagem de Leave tenho que verificar se sou o sucessor ou antecessor da origem da mensagem.
            # Se for antecessor: Atualizar o campo do sucessor com a informacao do sucessor do no que deixou o anel.
            # Se for sucessor: Atualizar o campo do antecessor com a informacao do antecessor do no que deixou o anel.
            rmsg = {
                "dest_ip_addr": msg["addr"],
                "type": 65,
                "id_src_msg": self.node.code,
            }
            if (self.node.code == id_node_sucessor) and (
                self.node.code == id_node_predecessor
            ):
                self.node.idPredecessor = id_node_predecessor
                self.node.ipAddrPredecessor = ip_node_predecessor
                self.node.idSuccessor = id_node_sucessor
                self.node.ipAddrSuccessor = ip_node_sucessor

            elif self.node.code == id_node_sucessor:
                self.node.idPredecessor = id_node_predecessor
                self.node.ipAddrPredecessor = ip_node_predecessor

            elif self.node.code == id_node_predecessor:
                self.node.idSuccessor = id_node_sucessor
                self.node.ipAddrSuccessor = ip_node_sucessor

            # Envia mensagem de resposta do Leave ( COD 65 )
            self.client_p2p.sendLeaveMsg(rmsg)
            self.node.updateScreen("Received: LEAVE IP_S:" + str(rmsg))
        elif int(typeMSG[0]) == 65:
            # Resposta Leave
            res = struct.unpack("!BI", msg["data"])
            id_src_msg = int(res[1])
            # Comparar o ID_SRC_MSG com os ID do meu sucessor e antecessor.
            if id_src_msg == self.node.idSuccessor:
                # Retira os valores do sucessor.
                self.node.idSuccessor = None
                self.node.ipAddrSuccessor = None
            elif id_src_msg == self.node.idPredecessor:
                # Retira os valores do antecessor.
                self.node.idPredecessor = None
                self.node.ipAddrPredecessor = None

            self.node.updateScreen("Received: ANSWER LEAVE " + str(id_src_msg))

    def lookupMessage(self, msg):
        # Envio Lookup
        typeMSG = bytearray(msg["data"])
        if int(typeMSG[0]) == 2:
            res = struct.unpack("!BIII", msg["data"])
            src_id_searched = int(res[1])
            src_ip_searched = self.int2ip(int(res[2]))
            id_searched = int(res[3])
            if (
                self.node.code == self.node.idSuccessor
                and self.node.code == self.node.idPredecessor
            ):
                # Sou o no inicial: Respondo o Lookup ( COD 66) com os dados do meu no
                rmsg = {
                    "dest_ip_addr": src_ip_searched,
                    "type": 66,
                    "id_searched": id_searched,
                    "id_sucessor_searched": self.node.code,
                    "ip_sucessor_searched": self.node.ipAddrNode,
                    "state": "A",
                }
                self.client_p2p.sendLookupMsg(rmsg)
            elif self.node.code < id_searched and self.node.idSuccessor > id_searched:
                # O meu antecessor é maior porem o meu sucessor eh maior
                # Repassa a Mensagem de Lookup para o meu Sucessor. (COD 2)
                rmsg = {
                    "dest_ip_addr": self.node.ipAddrSuccessor,
                    "type": 2,
                    "src_id_searched": src_id_searched,
                    "src_ip_searched": src_ip_searched,
                    "id_searched": id_searched,
                    "state": "B",
                }
                self.client_p2p.sendLookupMsg(rmsg)
            elif (
                self.node.code < id_searched
                and self.node.idPredecessor > self.node.code
            ):
                # se o meu ID é menor que o ID procurado  e o ID do meu antecessor é maior que o meu próprio ID,
                # eu respondo a mensagem de Lookup para o ID do procurado. (COD 66)
                rmsg = {
                    "dest_ip_addr": src_ip_searched,
                    "type": 66,
                    "id_searched": id_searched,
                    "id_sucessor_searched": self.node.code,
                    "ip_sucessor_searched": self.node.ipAddrNode,
                    "state": "C",
                }
                self.client_p2p.sendLookupMsg(rmsg)
            elif self.node.code >= id_searched:
                # Meu id Maior que ID do procurado = Responderei o Lookup para o ID do procurado. ( COD 66)
                rmsg = {
                    "dest_ip_addr": src_ip_searched,
                    "type": 66,
                    "id_searched": id_searched,
                    "id_sucessor_searched": self.node.code,
                    "ip_sucessor_searched": self.node.ipAddrNode,
                    "state": "D",
                }
                self.client_p2p.sendLookupMsg(rmsg)
            elif self.node.code < id_searched:
                # Repassa a Mensagem de Lookup para o meu Sucessor. (COD 2)
                rmsg = {
                    "dest_ip_addr": self.node.ipAddrSuccessor,
                    "type": 2,
                    "src_id_searched": src_id_searched,
                    "src_ip_searched": src_ip_searched,
                    "id_searched": id_searched,
                    "state": "FORWADING",
                }
                self.client_p2p.sendLookupMsg(rmsg)

            self.node.updateScreen("Received: LOOKUP " + str(rmsg))

        elif int(typeMSG[0]) == 66:
            # Resposta Lookup
            res = struct.unpack("!BIII", msg["data"])
            id_searched = int(res[1])
            id_sucessor_searched = int(res[2])
            ip_sucessor_searched = self.int2ip(int(res[3]))
            # Ao receber a resposta de lookup envio uma mensagem de Join para o IP sucessor procurado ( COD 0 )
            #
            rmsg = {
                "dest_ip_addr": ip_sucessor_searched,
                "type": 0,
                "id_node": self.node.code,
            }
            self.client_p2p.sendJoinMsg(rmsg)

            self.node.updateScreen("Received: ANSWER LOOKUP - JOIN TO " + str(rmsg))

    def updateMessage(self, msg):
        # Envio Update
        typeMSG = bytearray(msg["data"])
        if int(typeMSG[0]) == 3:
            res = struct.unpack("!BIII", msg["data"])
            id_src = int(res[1])
            id_new_sucessor = int(res[2])
            ip_new_sucessor = self.int2ip(int(res[3]))
            # Atualizar a informacao do meu No que o novo sucessor e o que esta descrito no cabecalho
            self.node.idSuccessor = id_new_sucessor
            self.node.ipAddrSuccessor = ip_new_sucessor
            # Responde o Update ( COD 67 )
            rmsg = {
                "dest_ip_addr": ip_new_sucessor,
                "type": 67,
                "id_src_msg": self.node.code,
            }
            self.client_p2p.sendUpdateMsg(rmsg)
            self.node.updateScreen("Received: UPDATE:" + str(rmsg))
        elif int(typeMSG[0]) == 67:
            # Resposta Update
            res = struct.unpack("!BI", msg["data"])
            id_src_msg = int(res[1])
            # ID_ORIGEM_MENSAGEM e igual ao valor no campo ID DO NO do meu No
            self.node.updateScreen(
                "Received: ANSWER UPDATE :ID_SRC="
                + str(id_src_msg)
                + " NODE ID="
                + str(self.node.code)
            )

    def run(self):
        while not self.stop:
            # Handle sockets
            data, addr = self.s.recvfrom(1024)
            self.client_p2p.sock = self.s
            msg = {"addr": addr[0], "data": data}
            try:
                if len(data) > 0:
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
                        print("Received: Invalid code!")
            except ValueError as e:
                continue
