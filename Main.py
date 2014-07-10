# -*- coding: utf-8 -*-
__author__ = 'Rafael S. Guimarães e João Paulo de Brito Gonçalves'

from server.ServerP2P import ServerP2P
from server.ClientP2P import ClientP2P
from threading import Thread
from domain import Node
import curses
import hashlib

def get_param(prompt_string, screen):
    screen.clear()
    y, x = screen.getmaxyx()
    screen.border(0)
    screen.addstr(15, 40, prompt_string, curses.color_pair(1))
    screen.refresh()
    input = screen.getstr(17, 40, 60)
    return input

def main():
    ## Inicia o Screen
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    ## Cria o No com um Hash Inicial
    node = Node.Node(screen)

    ## Codifica o codigo do no
    node.ipAddrNode = get_param("Enter Node IP Address", screen)
    codeHash = hashlib.md5(node.ipAddrNode)
    node.code = int(str(int(codeHash.hexdigest(),16))[0:4])
    ## Inicia e cria uma thread do servidor
    p2pServer = ServerP2P(node)
    p2pClient = ClientP2P("127.0.0.1", p2pServer.s)
    processo=Thread(target=p2pServer.run)
    processo.start()

    opc = 0
    while opc != ord('4'):
        # Get window dimensions
        y, x = screen.getmaxyx()

        screen.clear()
        screen.border(0)
        ## Exibe o No
        screen.addstr(2, (x-40),"----------------------------------")
        screen.addstr(3, (x-40),"CODE: "+str(node.code),curses.color_pair(2))
        screen.addstr(4, (x-40),"IP Node: "+str(node.ipAddrNode),curses.color_pair(2))
        screen.addstr(5, (x-40),"ID Successor: "+str(node.idSuccessor),curses.color_pair(2))
        screen.addstr(6, (x-40),"IP Successor: "+str(node.ipAddrSuccessor),curses.color_pair(2))
        screen.addstr(7, (x-40),"ID Predecessor: "+str(node.idPredecessor),curses.color_pair(2))
        screen.addstr(8, (x-40),"IP Predecessor: "+str(node.ipAddrPredecessor),curses.color_pair(2))
        screen.addstr(9, (x-40),"----------------------------------")
        ###
        screen.addstr(10, 40, "###    PyChord   -   P2P Node    ###",curses.color_pair(1))
        screen.addstr(12, 40, "1 - Initializing Ring",curses.color_pair(5))
        screen.addstr(13, 40, "2 - Leave Node",curses.color_pair(5))
        screen.addstr(14, 40, "3 - Lookup Node",curses.color_pair(5))
        screen.addstr(15, 40, "4 - Exit",curses.color_pair(5))
        screen.refresh()

        opc = screen.getch()

        if opc == ord('1'):
            ## Inicializando No
            if(node.idSuccessor == None and node.idPredecessor == None):
                node.idSuccessor = node.code
                node.idPredecessor = node.code
                node.ipAddrSuccessor = node.ipAddrNode
                node.ipAddrPredecessor = node.ipAddrNode
                ###
                screen.clear()
                screen.border(0)
                screen.addstr(15,40,"Ring Initialized with node: "+str(node.code),curses.color_pair(4))
                screen.refresh()
                res = screen.getch()
                curses.endwin()
            else:
                ###
                screen.clear()
                screen.border(0)
                screen.addstr(15,40,"Ring can not be initialized...",curses.color_pair(3))
                screen.refresh()
                res = screen.getch()
                curses.endwin()

        if opc == ord('2'):
            if node.ipAddrPredecessor and node.ipAddrSuccessor:
                screen.clear()
                screen.border(0)
                rmsg_sucessor = {
                    'dest_ip_addr': node.ipAddrSuccessor,
                    'type': 1,
                    'id_node_out': node.code,
                    'id_node_sucessor': node.idSuccessor,
                    'ip_node_sucessor': node.ipAddrSuccessor,
                    'id_node_predecessor': node.idPredecessor,
                    'ip_node_predecessor': node.ipAddrPredecessor,
                }
                rmsg_predecessor = {
                    'dest_ip_addr': node.ipAddrPredecessor,
                    'type': 1,
                    'id_node_out': node.code,
                    'id_node_sucessor': node.idSuccessor,
                    'ip_node_sucessor': node.ipAddrSuccessor,
                    'id_node_predecessor': node.idPredecessor,
                    'ip_node_predecessor': node.ipAddrPredecessor,
                }
                screen.addstr(15,40,"LEAVE to Sucessor: "+str(rmsg_sucessor['dest_ip_addr']), curses.color_pair(4))
                screen.addstr(20,40,"LEAVE to Predecessor:"+str(rmsg_predecessor['dest_ip_addr']), curses.color_pair(4))
                screen.refresh()
                p2pClient.sendLeaveMsg(rmsg_sucessor)
                p2pClient.sendLeaveMsg(rmsg_predecessor)
                res = screen.getch()
                curses.endwin()
            else:
                ###
                screen.clear()
                screen.border(0)
                screen.addstr(15,40,"IP ADDRESS OF SUCESSOR AND PREDECESSOR IS NULL",curses.color_pair(3))
                screen.refresh()
                res = screen.getch()
                curses.endwin()

        if opc == ord('3'):
            ipaddress = get_param("Enter the IP Address", screen)
            screen.clear()
            screen.border(0)
            screen.addstr(15,40,"LOOKUP to "+ipaddress,curses.color_pair(4))
            screen.refresh()
            res = screen.getch()
            rmsg = {
                'dest_ip_addr': ipaddress,
                'type': 2,
                'src_id_searched': node.code,
                'src_ip_searched': node.ipAddrNode,
                'id_searched': node.code,
            }
            p2pClient.sendLookupMsg(rmsg)
            curses.endwin()

        if opc == ord('4'):
            screen.clear()
            screen.border(1)
            screen.addstr(15,40,"[ PRESS ENTER TO EXIT ]",curses.color_pair(2))
            screen.refresh()
            p2pServer.stop = True
            p2pClient.sendMessage("FIM")
            res = screen.getch()
            curses.endwin()
    curses.endwin()

if __name__ == "__main__":
    main()