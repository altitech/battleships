class Ship(object):
	coords = None	#list of tuples [(x,y), ...]
	coordsHit = None	#list of tuples [(x,y), ...], will be deleted one by one, until ship sunk
	sunk = None
	length = None

	def __init__(self):
		self.sunk = False

	def isSunk(self):
		if len(self.coordsHit) == 0:
			return True
		else:
			return False

	def getCoords(self):
		if self.coords != None:
			return self.coords
		else:
			print "NO COORDS SET!"

	def setCoords(self, coords):
		self.coords = list(coords)
		self.coordsHit = list(coords)

	def getCoordsHit(self):
		return self.coordsHit
		
	def isAtPos(self, posx, posy):
		for position in self.coords:
			#if ship is hit
			if len(self.coordsHit) != 0:
			 	if(position[0] == posx and position[1] == posy):
					#remove position from coordsHit list
					self.coordsHit.remove(position)
					return True
		#if ship is missed		
		return False

class Carrier(Ship):
	length = 5		

class Battleship(Ship):
	length = 4

class Submarine(Ship):
	length = 3

class Destroyer(Ship):
	length = 3

class Patrol(Ship):
	length = 2
