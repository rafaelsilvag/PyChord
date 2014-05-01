__author__ = 'Rafael S. Guimaraes e Joao Paulo de Brito Goncalves'

class Node(object):

    def __init__(self, screen):
        self.code = None
        self.ipAddrNode = None
        self.idSuccessor = None
        self.idPredecessor = None
        self.ipAddrSuccessor = None
        self.ipAddrPredecessor = None
        self.__screen = screen

    def updateScreen(self, msg):
        """
            Update Screen
        """
        self.__screen.clear()
        self.__screen.border(0)
        self.__screen.addstr(5,10,msg)
        self.__screen.refresh()
