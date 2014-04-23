__author__ = 'rafaelguimaraes'

from server.ServerP2P import ServerP2P
from client.ClientP2P import ClientP2P

def main():
    p2pServer = ServerP2P()

    if(p2pServer):
        print "Starting Node P2P\t\t\t\t\t\t[  OK  ]"
        p2pServer.start()

    #p2pClient.start()
if __name__ == "__main__":
    main()