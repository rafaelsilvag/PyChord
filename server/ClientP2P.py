# -*- coding: utf-8 -*-
__author__ = "Rafael S. Guimarães e João Paulo de Brito Gonçalves"

import socket
import struct


class ClientP2P(object):
    def __init__(self, host, sock):
        self.host = host
        self.port = 12345
        self.sock = sock

    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(addr))[0]

    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", addr))

    def sendJoinMsg(self, msg):
        # Envia da mensagem de Update com código 0 e
        # Identificador do novo nó do anel
        if msg["type"] == 0:
            sendMsg = struct.pack("!BI", int(msg["type"]), int(msg["id_node"]))
        elif msg["type"] == 64:
            # Resposta da mensagem Join com o código 64
            # e com os campos Identificador do Sucessor,
            # Endereço IP do Sucessor,
            # Identificador do nó predecessor e Endereço IP do nó predecessor
            sendMsg = struct.pack(
                "!BIIII",
                int(msg["type"]),
                int(msg["id_node_sucessor"]),
                self.ip2int(msg["ip_node_sucessor"]),
                int(msg["id_node_predecessor"]),
                self.ip2int(msg["ip_node_predecessor"]),
            )
        # Socket Object
        self.sock.sendto(sendMsg, (msg["dest_ip_addr"], self.port))

    def sendLeaveMsg(self, msg):
        # Envio da mensagem Leave com o código 1 e os campos ID do nó saindo da rede, ID do nó Sucessor, ID do nó
        # antecessor, Endereço IP do nó sucessor e endereço IP do nó antecessor.
        if msg["type"] == 1:
            sendMsg = struct.pack(
                "!BIIIII",
                int(msg["type"]),
                int(msg["id_node_out"]),
                int(msg["id_node_sucessor"]),
                self.ip2int(msg["ip_node_sucessor"]),
                int(msg["id_node_predecessor"]),
                self.ip2int(msg["ip_node_predecessor"]),
            )
        elif msg["type"] == 65:
            # Resposta  da mensagem Leave com o código 65 e o campo ID da Origem da Mensagem
            sendMsg = struct.pack("!BI", int(msg["type"]), int(msg["id_src_msg"]))

        # Socket Object
        self.sock.sendto(sendMsg, (msg["dest_ip_addr"], self.port))

    def sendLookupMsg(self, msg):
        # Envio da mensagem  de Lookup com o código 2 e os campos correspondentes
        if msg["type"] == 2:
            sendMsg = struct.pack(
                "!BIII",
                int(msg["type"]),
                int(msg["src_id_searched"]),
                self.ip2int(msg["src_ip_searched"]),
                int(msg["id_searched"]),
            )
        elif msg["type"] == 66:
            # Resposta da mensagem Lookup com o código 66 e os campos correspondentes
            sendMsg = struct.pack(
                "!BIII",
                int(msg["type"]),
                int(msg["id_searched"]),
                int(msg["id_sucessor_searched"]),
                self.ip2int(msg["ip_sucessor_searched"]),
            )
        # Socket Object
        self.sock.sendto(sendMsg, (msg["dest_ip_addr"], self.port))

    def sendUpdateMsg(self, msg):
        # Envio da mensagem Update  com código 3 e ID da Origem da Procura
        if msg["type"] == 3:
            # Resposta da mensagem Update com código 67 e campos ID do novo sucessor, IP do novo sucessor e Identificador da origem
            sendMsg = struct.pack(
                "!BIII",
                int(msg["type"]),
                int(msg["id_src"]),
                int(msg["id_new_sucessor"]),
                self.ip2int(msg["ip_new_sucessor"]),
            )
        elif msg["type"] == 67:
            sendMsg = struct.pack("!BI", int(msg["type"]), int(msg["id_src_msg"]))

        # Socket Object
        self.sock.sendto(sendMsg, (msg["dest_ip_addr"], self.port))

    def sendMessage(self, msg):
        """
        Send Message using UDP Protocol
        """
        # Socket Object
        self.sock.connect((self.host, self.port))
        self.sock.send(msg)
        self.sock.close()
