# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 700
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
NUM_RED_APPLES = 15

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
ORANGE    = (255, 165,   0)
DARKORANGE= (255,  69,   0)
DARKYELLOW= (255, 140,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
SCOREBLUE = ( 65, 105, 225)
YELLOW    = (255, 255,   0)
BLUE      = (  0,   0, 255)
DARKBLUE  = (  0,   0,  76)
INDIGO    = ( 75,   0, 130)
LIME      = (  0, 255,   0)
BGCOLOR = BLACK




UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

NEIGHBORHOOD = 20
HEAD = 0 # syntactic sugar: index of the worm's head

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('GettingJiggyWitIt')

	showStartScreen()
	while True:
		runGame()
		showGameOverScreen()


def runGame():
	# Set a random start point.
	startx = random.randint(5, CELLWIDTH - 6)
	starty = random.randint(5, CELLHEIGHT - 6)
	
	wormCoords = getRandomStart()
	wormCoordstwo = getRandomStart()

	worms = [[wormCoords,RIGHT,GREEN,1],[wormCoordstwo,RIGHT,BLUE,2]]
	colors = [ORANGE,YELLOW, BLUE]


	#worm[0] - the worm
	#worm[1] - the direction
	#worm[2] - color
	#worm[3] - other
	# Start the apple in a random place.
	
	locs = getlist()
	applei = 0
	mode = 0
	#apple = getnextapple(applei, locs, mode)
	apple = getnextapplenomode(applei,locs)
	applei+=1

	ticker = 0
#K_KP2, K_KP4,  K_KP6, and K_KP8
	while True: # main game loop
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_KP4) and worms[0][1] != RIGHT:
					worms[0][1] = LEFT
				elif (event.key == K_a or event.key == K_KP4) and worms[1][1] != RIGHT:
					worms[1][1] = LEFT
				elif (event.key == K_RIGHT or event.key == K_KP6) and worms[0][1] != LEFT:
					worms[0][1] = RIGHT
				elif (event.key == K_d or event.key == K_KP6) and worms[1][1] != LEFT:
					worms[1][1] = RIGHT
				elif (event.key == K_UP or event.key == K_KP8) and worms[0][1] != DOWN:
					worms[0][1] = UP
				elif (event.key == K_w or event.key == K_KP8) and worms[1][1] != DOWN:
					worms[1][1] = UP
				elif (event.key == K_DOWN or event.key == K_KP2) and worms[0][1] != UP:
					worms[0][1] = DOWN
				elif (event.key == K_s or event.key == K_KP2) and worms[1][1] != UP:
					worms[1][1] = DOWN
				elif event.key == K_ESCAPE:
					terminate()
		'''
		mode = int((ticker%200)/50)

		current = 20
		if ticker%20==0:
			apple = getnextapple(applei, locs, mode)
			applei+=1
			if current % 5 == 0:
				current = 35
			elif current % 3 == 0:
				current = 25
			else:
				current = 15
		'''

		worms[0][1] = getagentDir(worms[0], apple, ticker)
		ticker+=1
		####affects directions of agent#######
		#get the centralized direction for the worms
		for i in range(len(worms)):
			if i > 0:
				worms[i][1] = centralizedDir(worms[i], apple)

		#function to avoid all the walls
		for worm in worms:
			worm[1] = avoidWalls(worm[0], worm[1])
		####affects directions of agent#######

		for worm in worms:
			worm = addsegment(worm)

		worms[0][2] = GREEN

		#add another worm if there is only one
		if len(worms) == 1:
				worms.append([getRandomStart(), RIGHT, getRandomColor(colors)])
		
		#check all worms for running into walls
		for worm in worms:
			if worm[0][HEAD]['x'] == -1 or worm[0][HEAD]['x'] == CELLWIDTH or worm[0][HEAD]['y'] == -1 or worm[0][HEAD]['y'] == CELLWIDTH:
				updatescreen(worms, apple, i)
				return
		
		#verify each worm hasn't hit himself
		#i keeps track of the index of the losing worm
		i = 0
		for worm in worms:
			for wormBody in worm[0][1:]:
				if wormBody['x'] == worm[0][HEAD]['x'] and wormBody['y'] == worm[0][HEAD]['y']:
					updatescreen(worms, apple, i)
					maxl = getmaxlength(worms)
					if i == 0:
						print("agent", len(worm[0]), maxl)
					else:
						print("other", len(worm[0]), maxl)
					return
			i+=1
		#checks all worms for apple eating
		for worm in worms:
			if worm[0][HEAD]['x'] == apple['x'] and worm[0][HEAD]['y'] == apple['y']:
				#apple = getnextapple(applei, locs, mode)
				apple = getnextapplenomode(applei,locs)
				applei+=1
			else:
				del worm[0][-1]

		worms = collision(worms)

		#split the worm if it is long enough
		i = 0
		for worm in worms:
			if len(worm[0]) > 19:
				splitworm(worm,i,worms,colors)
			i+=1

		updatescreen(worms, apple)
		FPSCLOCK.tick(FPS)

'''
things that I still have to do:
	take a look at collision function-
	different functions for the spawning of different apples	
'''
def getmaxlength(worms):
	maxl = 0
	for worm in worms:
		if len(worm[0]) > maxl:
			maxl = len(worm[0])
	return maxl

def getnextapplenomode(i,locs):
	x = locs[i][0]
	y = locs[i][1]
	return {'x':int(x),'y':int(y)}

def getnextapple(i, locs, mode):
	x = locs[i][0]
	y = locs[i][1]
	spot = {'x':int(x), 'y':int(y)}

	if mode == 0:
		spot['x'] = int(spot['x']/2)
		spot['y'] = int(spot['y']/2)
	elif mode == 1:
		spot['x'] = int(spot['x']/2)
		spot['y'] = int(spot['y']/2 + CELLHEIGHT/2)
	elif mode == 2:
		spot['x'] = int(spot['x']/2 + CELLWIDTH/2)
		spot['y'] = int(spot['y']/2)
	else:
		spot['x'] = int(spot['x']/2 + CELLWIDTH/2)
		spot['y'] = int(spot['y']/2 + CELLHEIGHT/2)

	return spot

def getRandomStart():
	startx = random.randint(5, CELLWIDTH - 6)
	starty = random.randint(5, CELLHEIGHT - 6)
	wormCoords = [{'x': startx,     'y': starty},
				  {'x': startx - 1, 'y': starty},
				  {'x': startx - 2, 'y': starty}]
	return wormCoords

def getRandomColor(colors):
	i = random.randint(0,len(colors)-1)
	return colors[i]

#I think there is some issue with this function........
def getagentDir(worm, apple, ticker):
	dist = getdistance(worm[0][HEAD], apple)
	if dist < NEIGHBORHOOD:
		return centralizedDir(worm, apple)
	cur = worm[1]
	modulo = random.randint(1,20)
	if ticker%(modulo)==0:
		if cur == UP or cur == DOWN:
			if worm[0][HEAD]['x'] == 0:
				return getRandomDirection(RIGHT, cur)
			elif worm[0][HEAD]['x'] == CELLWIDTH-1:
				return getRandomDirection(LEFT, cur)
			else:
				return getRandomDirectionthree(LEFT, RIGHT, cur)

		elif cur == RIGHT or cur == LEFT:
			if worm[0][HEAD]['y'] == 0:
				return getRandomDirection(DOWN, cur)
			elif worm[0][HEAD]['y'] == CELLHEIGHT-1:
				return getRandomDirection(UP, cur)
			else:
				return getRandomDirectionthree(UP, DOWN, cur)
	else:
		return cur

def getdistance(head, apple):
	x = abs(head['x']-apple['x'])
	y = abs(head['y']-apple['y'])
	return float((x**2 + y**2)**.5)

def splitworm(worm,i,worms,colors):
	half = int(len(worm[0])/2)

	wormone = worm[0][:half]
	wormtwo = worm[0][half:]

	worms.append([wormone,worm[1],getRandomColor(colors)])
	worms.append([wormtwo,worm[1],getRandomColor(colors)])

	del worms[i]

	return worms

def centralizedDir(worm, apple):
	if worm[0][HEAD]['x'] < apple['x'] and worm[1] != LEFT:
		return RIGHT
	elif worm[0][HEAD]['x'] > apple['x'] and worm[1] != RIGHT:
		return LEFT
	elif worm[0][HEAD]['y'] < apple['y'] and worm[1] != UP:
		return DOWN
	elif worm[0][HEAD]['y'] > apple['y'] and worm[1] != DOWN:
		return UP
	else:
		return worm[1]

def collision(worms):
	j = k = 0
	for worm in worms:
		for other_worm in worms:
			if j != k:
				for wormBody in other_worm[0]:
					if worm[0][HEAD]['x'] == wormBody['x'] and worm[0][HEAD]['y'] == wormBody['y']:
						if len(worm[0]) > len(other_worm[0]):
							del worms[j]
						else:
							del worms[k]
				k+=1
		j+=1
	return worms

def addsegment(worm):
	if worm[1] == UP:
		newHead = {'x': worm[0][HEAD]['x'], 'y': worm[0][HEAD]['y'] - 1}
	elif worm[1] == DOWN:
		newHead = {'x': worm[0][HEAD]['x'], 'y': worm[0][HEAD]['y'] + 1}
	elif worm[1] == LEFT:
		newHead = {'x': worm[0][HEAD]['x'] - 1, 'y': worm[0][HEAD]['y']}
	elif worm[1] == RIGHT:
		newHead = {'x': worm[0][HEAD]['x'] + 1, 'y': worm[0][HEAD]['y']}
	return worm[0].insert(0, newHead)

def avoidWalls(wormCoords, direction):
	if wormCoords[HEAD]['x'] == 0 and wormCoords[HEAD]['y'] == 0 and direction == UP:
		return RIGHT
	elif wormCoords[HEAD]['x'] == 0 and wormCoords[HEAD]['y'] == CELLHEIGHT-1 and direction == DOWN:
		return RIGHT
	elif wormCoords[HEAD]['x'] == 0 and wormCoords[HEAD]['y'] == 0 and direction == LEFT:
		return DOWN
	elif wormCoords[HEAD]['x'] == 0 and wormCoords[HEAD]['y'] == CELLHEIGHT-1 and direction == LEFT:
		return UP
	elif wormCoords[HEAD]['x'] == CELLWIDTH-1 and wormCoords[HEAD]['y'] == 0 and direction == RIGHT:
		return DOWN
	elif wormCoords[HEAD]['x'] == CELLWIDTH-1 and wormCoords[HEAD]['y'] == 0 and direction == UP:
		return LEFT
	elif wormCoords[HEAD]['x'] == CELLWIDTH-1 and wormCoords[HEAD]['y'] == CELLHEIGHT-1 and direction == RIGHT:
		return UP
	elif wormCoords[HEAD]['x'] == CELLWIDTH-1 and wormCoords[HEAD]['y'] == CELLHEIGHT-1 and direction == DOWN:
		return LEFT 
	elif wormCoords[HEAD]['x'] == 0 and direction == LEFT:
		return getRandomDirection(UP, DOWN)
	elif wormCoords[HEAD]['x'] == CELLWIDTH-1 and direction == RIGHT:
		return getRandomDirection(UP, DOWN)
	elif wormCoords[HEAD]['y'] == 0 and direction == UP:
		return getRandomDirection(LEFT, RIGHT)
	elif wormCoords[HEAD]['y'] == CELLHEIGHT-1 and direction == DOWN:
		return getRandomDirection(LEFT, RIGHT)
	else:
		return direction

def getRandomDirection(DIR1, DIR2):
	if random.randint(0,1) == 1:
		return DIR1
	else:
		return DIR2

def getRandomDirectionthree(DIR1, DIR2, DIR3):
	direct = random.randint(0,2)
	if direct == 0:
		return DIR1
	elif direct == 1:
		return DIR2
	else:
		return DIR3

def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def updatescreen(worms, apple, lost=-1):
	scores = []
	#get the score for all the worms, subtract the loser, give color to function too
	for worm in worms:
		scores.append([len(worm[0])-3, worm[2]])
	if lost == -1:
		pass
	else:
		scores[lost][0]-=2

	DISPLAYSURF.fill(BGCOLOR)
	drawGrid()
	for worm in worms:
		drawWorm(worm[0], worm[2])
	drawApple(apple, RED)

	drawScore(scores)

	pygame.display.update()


def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()

	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key


def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('SQUIRMY', True, DARKGREEN, RED)
	titleSurf2 = titleFont.render('SQUIRMY', True, DARKBLUE)

	degrees1 = 0
	degrees2 = 0
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
		DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

		drawPressKeyMsg()

		if checkForKeyPress():
			pygame.event.get() # clear event queue
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		degrees1 += 3 # rotate by 3 degrees each frame
		degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
	pygame.quit()
	sys.exit()

def fillrandomlist():
	file = open("xandy.txt", 'w')
	for i in range(800):
		x = random.randint(0, CELLWIDTH - 1)
		y = random.randint(0, CELLHEIGHT - 1)
		file.write(str(x)+","+str(y)+"\n")

def getlist():
	file = open("xandy.txt",'r')
	locs = []
	for line in file:
		loc = line.strip().split(",")
		locs.append(loc)
	return locs



def getRandomLocation():
	return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen():
	gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
	gameSurf = gameOverFont.render('Game', True, WHITE)
	overSurf = gameOverFont.render('Over', True, WHITE)
	gameRect = gameSurf.get_rect()
	overRect = overSurf.get_rect()
	gameRect.midtop = (WINDOWWIDTH / 2, 10)
	overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

	DISPLAYSURF.blit(gameSurf, gameRect)
	DISPLAYSURF.blit(overSurf, overRect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress() # clear out any key presses in the event queue

	while True:
		if checkForKeyPress():
			pygame.event.get() # clear event queue
			return

def drawScore(scores):
	h = 10
	for score in scores:
		scoreSurf = BASICFONT.render('Score: %s' % (score[0]), True, score[1])
		scoreRect = scoreSurf.get_rect()
		scoreRect.topleft = (WINDOWWIDTH - 120, h)
		h+=20
		DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, color):
	for coord in wormCoords:
		if color == GREEN:
			DARKCOLOR = DARKGREEN
		elif color == BLUE:
			DARKCOLOR = DARKBLUE
		elif color == YELLOW:
			DARKCOLOR = DARKYELLOW
		else:
			DARKCOLOR = DARKORANGE

		x = coord['x'] * CELLSIZE
		y = coord['y'] * CELLSIZE
		wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
		pygame.draw.rect(DISPLAYSURF, DARKCOLOR, wormSegmentRect)
		wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
		pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)

def drawApple(coord, color):
	x = coord['x'] * CELLSIZE
	y = coord['y'] * CELLSIZE
	appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
	pygame.draw.rect(DISPLAYSURF, color, appleRect)


def drawGrid():
	for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
	for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
		pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
	main()