import pygame
from numpy import random, array
import sys
pygame.init()
dungeonXSize = dungeonYSize = 16
bg = 255,255,255
black = 0,0,0
tileSize = 32
screen = pygame.display.set_mode((dungeonXSize*tileSize+150,dungeonYSize*tileSize))
screen.fill(bg)
myfont = pygame.font.SysFont("arial",18)
def inside(pos):
	if pos[0] >= dungeonXSize or pos[0] <= -1 or pos[1] >= dungeonYSize or pos[1] <= -1:
		return False
	return True

def updateWorld(tile, pos):
	dungeon[pos[0]][pos[1]] = tile
	surf.blit(tiles[tile], (pos[0]*32, pos[1]*32))

def newpos(pos, e):
	if e == pygame.K_UP:
		return (pos+array([0,-1]))
	elif e == pygame.K_DOWN:
		return (pos+array([0,1]))
	elif e == pygame.K_LEFT:
		return (pos+array([-1, 0]))
	elif e == pygame.K_RIGHT:
		return (pos+array([1,0]))

def passablepos(pos):
	return passable[dungeon[pos[0]][pos[1]]]

def directionalkey(e):
	return e == pygame.K_UP or e == pygame.K_DOWN or e == pygame.K_LEFT or e == pygame.K_RIGHT

class Creature():
	def __init__(self, pos):
		self.pos = array(pos)
		self.health = 1

class Hero(Creature):
	def __init__(self, pos):
		Creature.__init__(self, pos)
		self.health = 10
		self.bombs = 3
		self.bombcatch = False

	def gethealth(self):
		return self.health

	def getpos(self):
		return self.pos
	
	def setnewpos(self, newpos):
		self.pos = newpos
	
	def setpos(self, direction):
		self.pos += array(direction)

	def catchevent(self):
		return self.bombcatch

	def restevent(self, e):
		if e == pygame.K_b:
			self.bombcatch = True

	def preevent(self, e):
		if e == pygame.K_b:
			self.bombcatch = False
		if directionalkey(e):
			self.destroytile(newpos(self.pos,e))

	def getbombs(self):
		return self.bombs

	def addbomb(self, i = 1):
		self.bombs += i

	def getbombmode(self):
		return self.bombcatch

	def destroytile(self,pos):
		if inside(pos):
			if (self.bombs > 0):
				updateWorld(1, pos)
				self.bombs -= 1
		self.bombcatch = False

class Pickup:
	def __init__(self):
		self.pos = array([random.randint(0, dungeonXSize),random.randint(0, dungeonYSize)])

	def getpos(self):
		return self.pos

	def get(self, player):
		print "nothing here"

	def draw(self):
		print "nothing here"

class BombPickup(Pickup):
	image = pygame.image.load("gfx/bomb.png")
	def get(self, other):
		other.addbomb()

	def draw(self):
		screen.blit(self.image, self.pos*tileSize)

def playGame():
	global passable
	global tiles
	global dungeon
	global surf
	tilefiles = ["gfx/floor.png", "gfx/ground.png", "gfx/wall.png"]
	passable = [True, True, False]
	tiles = []
	for f in tilefiles:
		tiles.append(pygame.image.load(f))

	itemtypes = [BombPickup]
	items = []

	dungeon = []
	myhero = Hero([0,0])
	herotile = pygame.image.load("gfx/hero.png")
	for i in xrange(dungeonXSize):
		items.append(itemtypes[0]())

	for i in xrange(dungeonXSize):
		dungeon.append(random.randint(0,len(tilefiles),dungeonYSize))
	dungeon[0][0] = 0

	surf = pygame.Surface((dungeonXSize*tileSize, dungeonYSize*tileSize))
	for v in xrange(len(dungeon)):
		for i in xrange(len(dungeon[v])):
			surf.blit(tiles[dungeon[v][i]], (v*tileSize, i*tileSize))
	while 1:
		pos = myhero.getpos()
		screen.blit(surf, (0,0))
		for item in items:
			item.draw()
		for item in items:
			posi = item.getpos()
			if pos[0] == posi[0] and pos[1] == posi[1]:
				item.get(myhero)
				items.remove(item)
		label1 = myfont.render("Health: %i"%(myhero.gethealth()),1,black)
		label2 = myfont.render("Bombs: %i"% (myhero.getbombs()),1,black)
		if (myhero.getbombmode()):
			l3text = "on"
		else:
			l3text = "off"
		label3 = myfont.render("Bombmode: %s"% (l3text),1,black)
		screen.blit(label1, (dungeonXSize*tileSize,0))
		screen.blit(label2, (dungeonXSize*tileSize,24))
		screen.blit(label3, (dungeonXSize*tileSize,48))
		screen.blit(herotile, myhero.getpos()*tileSize)
		
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN:
				temppos = newpos(pos, e.key)
				if e.key == pygame.K_ESCAPE:
					sys.exit()
				if myhero.catchevent():
					myhero.preevent(e.key)
				elif temppos != None:
					if inside(temppos) and passablepos(temppos):
						myhero.setnewpos(temppos)
				else:
					myhero.restevent(e.key)
		pygame.display.flip()
		screen.fill(bg)


if __name__ == '__main__':
	playGame()
