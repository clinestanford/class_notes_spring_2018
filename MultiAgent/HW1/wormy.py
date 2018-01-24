# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 700
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
NUM_RED_APPLES = 5
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
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
	wormCoords = [{'x': startx,     'y': starty},
				  {'x': startx - 1, 'y': starty},
				  {'x': startx - 2, 'y': starty}]

	start_two_x = random.randint(5, CELLWIDTH - 6)
	start_two_y = random.randint(5, CELLHEIGHT - 6)
	wormCoordstwo = [{'x': start_two_x,     'y': start_two_y},
				  {'x': start_two_x - 1, 'y': start_two_y},
				  {'x': start_two_x - 2, 'y': start_two_y}]
	direction = RIGHT
	directiontwo = RIGHT

	# Start the apple in a random place.
	yellow_apple = []
	apple = []
	yellow_apple.append(getRandomLocation())

	for i in range(NUM_RED_APPLES):
		loc = getRandomLocation()
		while loc == yellow_apple:
			loc = getRandomLocation()
		apple.append(loc)
	
#K_KP2, K_KP4,  K_KP6, and K_KP8
	while True: # main game loop
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_KP4) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_a or event.key == K_KP4) and directiontwo != RIGHT:
					directiontwo = LEFT
				elif (event.key == K_RIGHT or event.key == K_KP6) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_d or event.key == K_KP6) and directiontwo != LEFT:
					directiontwo = RIGHT
				elif (event.key == K_UP or event.key == K_KP8) and direction != DOWN:
					direction = UP
				elif (event.key == K_w or event.key == K_KP8) and directiontwo != DOWN:
					directiontwo = UP
				elif (event.key == K_DOWN or event.key == K_KP2) and direction != UP:
					direction = DOWN
				elif (event.key == K_s or event.key == K_KP2) and directiontwo != UP:
					directiontwo = DOWN
				elif event.key == K_ESCAPE:
					terminate()


		#check to see if all the apples are off the screen
		are_gone = True
		for i in range(len(apple)):
			if apple[i] != {'x': -1, 'y': -1}:
				are_gone = False

		if are_gone:
			for i in range(3):
				yellow_apple.append(getRandomLocation())
			for i in range(len(apple)):
				loc = getRandomLocation()
				for j in range(len(yellow_apple)):
					if loc == yellow_apple[j]:
						loc = getRandomLocation()
				while yellow_apple == loc:
					loc = getRandomLocation()
				apple[i] = loc

		drawScore(len(wormCoords) - 3, LIME)


		if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
			update_screen(wormCoords, wormCoordstwo, apple, yellow_apple, len(wormCoords)-5, len(wormCoordstwo)-3)
			return # game over

		for wormBody in wormCoords[1:]:
			if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
				update_screen(wormCoords, wormCoordstwo, apple, yellow_apple, len(wormCoords)-3, len(wormCoordstwo)-5)
				return

		#check if the second worm has hit itself
		if wormCoordstwo[HEAD]['x'] == -1 or wormCoordstwo[HEAD]['x'] == CELLWIDTH or wormCoordstwo[HEAD]['y'] == -1 or wormCoordstwo[HEAD]['y'] == CELLHEIGHT:
			update_screen(wormCoords, wormCoordstwo, apple, yellow_apple, len(wormCoords)-3, len(wormCoordstwo)-5)
			return

		for wormBody in wormCoordstwo[1:]:
			if wormBody['x'] == wormCoordstwo[HEAD]['x'] and wormBody['y'] == wormCoordstwo[HEAD]['y']:
				update_screen(wormCoords, wormCoordstwo, apple, yellow_apple, len(wormCoords)-3, len(wormCoordstwo)-5)
				return

		# check if first worm has eaten an apply
		got_apple = False
		for i in range(len(apple)):
			if wormCoords[HEAD]['x'] == apple[i]['x'] and wormCoords[HEAD]['y'] == apple[i]['y']:
				# don't remove worm's tail segment
				apple[i] = {'x': -1, 'y': -1} # set a new apple somewhere
				got_apple = True
		if got_apple:
			pass
		else:
			del wormCoords[-1] # remove worm's tail segment         
		
		#second worm getting the apple
		got_apple_two = False
		for i in range(len(apple)):
			if wormCoordstwo[HEAD]['x'] == apple[i]['x'] and wormCoordstwo[HEAD]['y'] == apple[i]['y']:
				apple[i] = {'x': -1, 'y': -1}
				got_apple_two = True
		if got_apple_two:
			pass
		else:
			del wormCoordstwo[-1]
				

		#check to see if it has eaten a yellow apple
		for i in range(len(yellow_apple)):
			if wormCoords[HEAD]['x'] == yellow_apple[i]['x'] and wormCoords[HEAD]['y'] == yellow_apple[i]['y']:

				return

		#check to see if second worm has eaten a yellow apple
		for i in range(len(yellow_apple)):
			if wormCoordstwo[HEAD]['x'] == yellow_apple[i]['x'] and wormCoordstwo[HEAD]['y'] == yellow_apple[i]['y']:
				return

		# move the worm by adding a segment in the direction it is moving
		if direction == UP:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
		elif direction == DOWN:
			newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
		elif direction == LEFT:
			newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
		elif direction == RIGHT:
			newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

		#move the second worm
		if directiontwo == UP:
			newHeadtwo = {'x': wormCoordstwo[HEAD]['x'], 'y': wormCoordstwo[HEAD]['y'] - 1}
		elif directiontwo == DOWN:
			newHeadtwo = {'x': wormCoordstwo[HEAD]['x'], 'y': wormCoordstwo[HEAD]['y'] + 1}
		elif directiontwo == LEFT:
			newHeadtwo = {'x': wormCoordstwo[HEAD]['x'] - 1, 'y': wormCoordstwo[HEAD]['y']}
		elif directiontwo == RIGHT:
			newHeadtwo = {'x': wormCoordstwo[HEAD]['x'] + 1, 'y': wormCoordstwo[HEAD]['y']}

			
		wormCoords.insert(0, newHead)
		wormCoordstwo.insert(0, newHeadtwo)
		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords, GREEN)
		drawWorm(wormCoordstwo, BLUE)
		for i in range(len(apple)):
			drawApple(apple[i], RED)
		for i in range(len(yellow_apple)):
			drawApple(yellow_apple[i], YELLOW)
		drawScore(len(wormCoords) - 3, LIME)
		drawScore(len(wormCoordstwo) - 3, SCOREBLUE)
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def update_screen(wormCoords, wormCoordstwo, apple, yellow_apple, score1, score2):
		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords, GREEN)
		drawWorm(wormCoordstwo, BLUE)
		for i in range(len(apple)):
			drawApple(apple[i], RED)
		for i in range(len(yellow_apple)):
			drawApple(yellow_apple[i], YELLOW)
		drawScore(score1, LIME)
		drawScore(score2, SCOREBLUE)
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

def drawScore(score, color):
	scoreSurf = BASICFONT.render('Score: %s' % (score), True, color)
	scoreRect = scoreSurf.get_rect()
	if color == LIME:
		scoreRect.topleft = (WINDOWWIDTH - 120, 10)
	else:
		scoreRect.topleft = (WINDOWWIDTH - 120, 30)
	DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, color):
	for coord in wormCoords:
		if color == GREEN:
			DARKCOLOR = DARKGREEN
		else:
			DARKCOLOR = DARKBLUE
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