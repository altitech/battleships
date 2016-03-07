import sys
from PyQt4 import QtGui, QtCore
from field import Field
from ships import *

size = 10
row_label = ["A","B","C","D","E","F","H","J","I","J"]
col_label = ["1","2","3","4","5","6","7","8","9","10"]

class Board(QtGui.QWidget):

    grid = None
    ships = None

    def createShips(self):
        self.ships.append(Carrier())
        self.ships.append(Battleship())
        self.ships.append(Submarine())
        self.ships.append(Destroyer())
        self.ships.append(Patrol())

    def initFields(self):
        self.grid.setHorizontalSpacing(1)
        self.grid.setVerticalSpacing(1)

        #add the fields to the EnemyField
        for row in range(size+1):
            for col in range(size+1):
                if col == 0 and row < size:
                    self.grid.addWidget(QtGui.QLabel(col_label[row], self), row+1, col, QtCore.Qt.AlignCenter)
                if row == 0 and col < size:
                    self.grid.addWidget(QtGui.QLabel(row_label[col], self), row, col+1, QtCore.Qt.AlignCenter)
                if row > 0 and col > 0:
                    self.grid.addWidget(Field(row, col, self.cn, self).getField(), row, col)

        self.setLayout(self.grid)

    def allSunk(self):
        for ship in self.ships:
            if ship.isSunk() == False:
                return False
        else:
            return True

    def markShipAsSunk(self,ship):
        for pos in ship.getCoords():
            self.grid.itemAtPosition(pos[0]+1,pos[1]+1).widget().setIcon(QtGui.QIcon("sunk.gif"))

class EnemyBoard(Board):

    grid = QtGui.QGridLayout()
    ships = []
    playerboard = None
    
    def __init__(self, playerboard):
        super(EnemyBoard, self).__init__()
        self.cn = self.__class__.__name__
        self.playerboard = playerboard
        self.initFields()
        self.createShips()

class PlayerBoard(Board):

    grid = QtGui.QGridLayout()
    ships = []

    def __init__(self):
        super(PlayerBoard, self).__init__()
        self.cn = self.__class__.__name__
        self.initFields()
        self.createShips()
        playerboard = self.grid

    def placeShips(self):
        for row in range(size+1):
            for col in range(size+1):
                for ship in self.ships:
                    for coord in ship.getCoords():
                        if coord == (row-1, col-1):
                            self.grid.itemAtPosition(row,col).widget().setIcon(QtGui.QIcon("ship.gif"))

def getEnemyLabel():
    return QtGui.QLabel("Enemy Field")

def getPlayerLabel():
    return QtGui.QLabel("Your Field")

def getDivider():
    hLine = QtGui.QFrame()
    hLine.setFrameStyle(QtGui.QFrame.HLine)
    hLine.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
    return hLine