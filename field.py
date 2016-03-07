import sys
from PyQt4 import QtGui, QtCore
from board import *
from random import randint
from battleships import *

states = ["water", "ship", "miss", "hit", "sunk"]
source = ["water.gif", "ship.gif", "miss.gif", "hit.gif", "sunk.gif"]

class Field(QtGui.QWidget):
    button = None
    x = None
    y = None
    cn = None
    state = None
    board = None
    clickList = []
    clickListEnemy = []
    
    def __init__(self, x, y, cn, board):
        super(Field, self).__init__()
        self.x = x-1
        self.y = y-1
        self.cn = cn
        self.board = board
        self.createField()

    def createField(self):
        self.state = states[0]
        self.button = QtGui.QPushButton(self)
        self.button.setIcon(QtGui.QIcon(source[0]))
        self.button.setIconSize(QtCore.QSize(20,20))
        self.button.setFixedSize(QtCore.QSize(20,20))
        if self.cn == "EnemyBoard":
            self.button.clicked.connect(lambda: self.click())
        else:
            self.button.clicked.connect(lambda: self.dummy())

    def getField(self):
        return self.button

    def click(self):
        isValidTurn = self.fire()
        
        #only enemys turn after valid click of player
        if isValidTurn:
            self.enemyTurn()

    def finish(self, text):
        msgBox = QtGui.QMessageBox()
        if text == "player":
            msgBox.setText("You won!")
        else:
            msgBox.setText("You lose!")
        msgBox.exec_()
        sys.exit()

    def enemyTurn(self):
        #print "enemy did something..."
        ex = randint(0,9)
        ey = randint(0,9)

        while self.isClicked(self.clickListEnemy, ex, ey):
            ex = randint(0,9)
            ey = randint(0,9)

        #print "enemy rolled "+str(ex)+"/"+str(ey)
        for ship in self.board.playerboard.ships:
            for coord in ship.getCoords():
                if ship.isAtPos(ex, ey):
                    self.board.playerboard.grid.itemAtPosition(ex+1,ey+1).widget().setIcon(QtGui.QIcon("hit.gif"))
                    if ship.isSunk():
                        self.board.playerboard.markShipAsSunk(ship)
                    if self.board.playerboard.allSunk():
                        self.finish("enemy")
                    self.clickListEnemy.append((ex,ey))
                    return
        else:
            self.board.playerboard.grid.itemAtPosition(ex+1,ey+1).widget().setIcon(QtGui.QIcon("miss.gif"))
            
        self.clickListEnemy.append((ex,ey))

    def fire(self):
    
        if self.isClicked(self.clickList, self.x, self.y):
            #if already clicked on field, do nothing
            return False
        else:
            for ship in self.board.ships:
                #if any ship is on this position, mark as hit
                if ship.isAtPos(self.x, self.y):
                    self.button.setIcon(QtGui.QIcon("hit.gif"))
                    #if sunk, mark ship as sunk
                    if ship.isSunk():
                        self.board.markShipAsSunk(ship)                        
                    #check if any ship is left. if not, game win
                    if self.board.allSunk():
                        self.finish("player")
                    break
            else:
                self.button.setIcon(QtGui.QIcon("miss.gif"))

            self.clickList.append((self.x ,self.y))
            return True

    def isClicked(self, list,x,y):
        for pos in list:
            if pos[0] == x and pos[1] == y:
                return True
        return False

    def dummy(self):
        pass
