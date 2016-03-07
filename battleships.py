import sys
from PyQt4 import QtGui, QtCore
from board import *
from ships import *
from random import randint

class GameWindow(QtGui.QMainWindow):

    enemyboard = None
    playerboard = None
    playercoords = []
    shipNames = ["Carrier", "Battleship", "Submarine", "Destroyer", "Patrol"]
    labelInput = None
    button = None

    def __init__(self):
        super(GameWindow, self).__init__()        
        self.init_UI()
        
    def init_UI(self):
        #create menubar items
        new_game = QtGui.QAction('&New Game', self)
        new_game.setStatusTip('New Game')
        new_game.triggered.connect(lambda: self.init_game())

        quit_game = QtGui.QAction('&Quit', self)
        quit_game.setStatusTip('Quit Game')
        quit_game.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        #create menubar and add items to it       
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Game')
        #fileMenu.addAction(new_game)
        fileMenu.addAction(quit_game)
        
        self.init_game()
        
        self.setWindowTitle('Battleships')
        self.show()

    def createBoard(self, widget):
        widgetLayout = QtGui.QVBoxLayout(widget)
        
        #add everything to the widget
        widgetLayout.addWidget(getEnemyLabel())
        widgetLayout.addWidget(self.enemyboard)
        widgetLayout.addWidget(getDivider())
        widgetLayout.addWidget(getPlayerLabel())
        widgetLayout.addWidget(self.playerboard)
        
        #set central widget
        self.setCentralWidget(widget)

    def isCoordsColliding(self, tmpcoords, enemycoords):
        for ship in enemycoords:
            for coord in ship:
                for tmpcoord in tmpcoords:
                    if tmpcoord == coord:
                        return True
        return False

    def createRandomCoord(self, shipIndex):
        #roll if ship will be horizontal (= 1) or vertical (= 0)
        align = randint(0,1)
        tmpcoord = []

        if align:
            #create horizontal
            #roll random pos
            pos = (randint(0,9), randint(0,9-self.enemyboard.ships[shipIndex].length))
            for coord in range(self.enemyboard.ships[shipIndex].length):
                tmpcoord.append((pos[0], pos[1]+coord))
        else:
            #create vertical
            pos = (randint(0,9-self.enemyboard.ships[shipIndex].length), randint(0,9))
            for coord in range(self.enemyboard.ships[shipIndex].length):
                tmpcoord.append((pos[0]+coord, pos[1]))

        return tmpcoord

    def setShipsCoords(self):
        #FIRST RANDOMLY PLACE ENEMYSHIPS
        enemycoords = [] #list of ships containing coords
        [enemycoords.append([]) for x in range(5)]

        playercoords = [] #list of ships containing coords
        [playercoords.append([]) for x in range(5)]

        #first ship
        enemycoords[0] = self.createRandomCoord(0)
        playercoords[0] = self.createRandomCoord(0)

        for i in range(1,5):            
            #check if there are already ships on the generated coords
            tmpcoord = self.createRandomCoord(i)
            while(True):
                if self.isCoordsColliding(tmpcoord, enemycoords):
                    tmpcoord = self.createRandomCoord(i)
                else:
                    break
            enemycoords[i] = tmpcoord

        for i in range(1,5):            
            #check if there are already ships on the generated coords
            tmpcoord = self.createRandomCoord(i)
            while(True):
                if self.isCoordsColliding(tmpcoord, playercoords):
                    tmpcoord = self.createRandomCoord(i)
                else:
                    break
            playercoords[i] = tmpcoord

        #print enemycoords

        for i in range(5):
            self.enemyboard.ships[i].setCoords(enemycoords[i])
            self.playerboard.ships[i].setCoords(playercoords[i])
            
        self.playerboard.placeShips()

    def clickEvent(self):
        pass

    def start_game(self):
        #create the widget (aka board)
        self.playerboard = PlayerBoard()
        self.enemyboard = EnemyBoard(self.playerboard)
        widget = QtGui.QWidget()
        self.createBoard(widget)

        #set coords of the all the ships
        self.setShipsCoords()       

    def init_game(self):
        print "New Game..."
        self.start_game()        
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = GameWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
