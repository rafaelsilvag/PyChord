__author__ = 'Rafael S. Guimaraes'

from server.ServerP2P import ServerP2P
from server.ClientP2P import ClientP2P
from threading import Thread
from domain import Node
import sys
import curses
import hashlib


def get_param(prompt_string, screen):
    screen.clear()
    y, x = screen.getmaxyx()
    screen.border(0)
    screen.addstr(8, (y/2), prompt_string)
    screen.refresh()
    input = screen.getstr(10, (y/2), 60)
    return input

def main():
    ## Inicia o Screen
    screen = curses.initscr()

    ## Cria o No com um Hash Inicial
    node = Node.Node(screen)

    ## Codifica o codigo do no
    node.ipAddrNode = get_param("Enter Node IP Address", screen)
    codeHash = hashlib.md5(node.ipAddrNode)
    node.code = str(int(codeHash.hexdigest(),16))[0:4]
    ## Inicia e cria uma thread do servidor
    p2pClient = ClientP2P("127.0.0.1")
    p2pServer = ServerP2P(node)
    processo=Thread(target=p2pServer.run)
    processo.start()

    opc = 0
    while opc != ord('5'):
        # Get window dimensions
        y, x = screen.getmaxyx()

        screen.clear()
        screen.border(0)
        ## Exibe o No
        screen.addstr(2, (x-40),"----------------------------------")
        screen.addstr(3, (x-40),"CODE: "+str(node.code))
        screen.addstr(4, (x-40),"IP Node: "+str(node.ipAddrNode))
        screen.addstr(5, (x-40),"ID Successor: "+str(node.idSuccessor))
        screen.addstr(6, (x-40),"IP Successor: "+str(node.ipAddrSuccessor))
        screen.addstr(7, (x-40),"ID Predecessor: "+str(node.idPredecessor))
        screen.addstr(8, (x-40),"IP Predecessor: "+str(node.ipAddrPredecessor))
        screen.addstr(9, (x-40),"----------------------------------")
        ###
        screen.addstr(2, (y/2), "PyChord - P2P Node")
        screen.addstr(4, (y/2), "1 - Initializing Node")
        screen.addstr(5, (y/2), "2 - Join Node")
        screen.addstr(6, (y/2), "3 - Leave Node")
        screen.addstr(7, (y/2), "4 - Lookup Node")
        screen.addstr(8, (y/2), "5 - Exit")
        screen.refresh()

        opc = screen.getch()

        if opc == ord('1'):
            ## Inicializando No
            node.idSuccessor = node.code
            node.idPredecessor = node.code
            node.ipAddrSuccessor = node.ipAddrNode
            node.ipAddrPredecessor = node.ipAddrNode
            ###
            screen.clear()
            screen.border(0)
            screen.addstr(7,7,"Node Initialized...")
            screen.refresh()
            res = screen.getch()
            curses.endwin()

        if opc == ord('2'):
            ipaddress = get_param("Enter the IP Address", screen)
            screen.clear()
            screen.border(0)
            screen.addstr(7,7,"Joined to "+ipaddress)
            screen.refresh()
            res = screen.getch()
            curses.endwin()

        if opc == ord('3'):
            ipaddress = get_param("Enter the IP Address", screen)
            screen.clear()
            screen.border(0)
            screen.addstr(7,7,"Joined to "+ipaddress)
            screen.refresh()
            res = screen.getch()
            curses.endwin()

        if opc == ord('4'):
            ipaddress = get_param("Enter the IP Address", screen)
            screen.clear()
            screen.border(0)
            screen.addstr(7,7,"Joined to "+ipaddress)
            screen.refresh()
            res = screen.getch()
            curses.endwin()

        if opc == ord('5'):
            screen.clear()
            screen.border(1)
            screen.addstr(7,7,"[ PRESS ENTER TO EXIT ]")
            screen.refresh()
            p2pServer.stop = True
            p2pClient.sendMessage("FIM")
            res = screen.getch()
            curses.endwin()
    curses.endwin()

if __name__ == "__main__":
    main()