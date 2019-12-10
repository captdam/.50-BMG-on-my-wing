import os, sys, pygame, random, binascii

from config import *
from model import *
from Plane import *
from Bullet import *

pygame.init()

pygame.display.set_caption(CONFIG['screenName'])
pygame.display.set_icon(pygame.image.load(CONFIG['screenIcon']))
screen = pygame.display.set_mode(CONFIG['screenSize'])

clock = pygame.time.Clock()

uiFont = pygame.font.SysFont('Courier',14)

playerPlane = PlayerPlane([ CONFIG['screenSize'][0]/2 , CONFIG['screenSize'][1]-20 ])

bullets = {}
enemyPlanes = {}
def createRandomKey(testSet):
	while True:
		randomKey = binascii.b2a_base64(os.urandom(36)).strip() #64-byte base64 key
		if random not in testSet.keys():
			return randomKey

frame = 0
score = 0
gameover = False
while 1:
	clock.tick(CONFIG['FPS'])
	frame += 1

	# Sys event
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT: sys.exit()

	userInput = pygame.key.get_pressed()

	if gameover:
		screen.fill((0,45,80))
		txt = uiFont.render('GAMEOVER ({}) Score: {}'.format( gameover, score ), False, (255,255,255))
		screen.blit(txt,(20,100))
		pygame.display.flip()
		continue
	
	# User action
	playerAction = [0,0,0] #dx, dy, fire[bomb,gun]
	
	# User move
	if userInput[pygame.K_a]: playerAction[0] -= 1
	if userInput[pygame.K_d]: playerAction[0] += 1
	if userInput[pygame.K_w]: playerAction[1] -= 1
	if userInput[pygame.K_s]: playerAction[1] += 1
	playerPlane.move(playerAction[0],playerAction[1])
	if frame % CONFIG['hpAutoHeal'] == 0:
		playerPlane.changeHp(1)

	# User fire
	if userInput[pygame.K_k]: #Machine gun
		if playerPlane.fire(0):
			bullets[ createRandomKey(bullets) ] = Bullet(
				[ playerPlane.centerXY[0], playerPlane.getLUCord()[1] ], 
				(0,-5)
			)
			score -= CONFIG['firingCost']

	if userInput[pygame.K_l]: #Bomb
		if playerPlane.fire(1):
			bullets[ createRandomKey(bullets) ] = Bomb(
				[ playerPlane.centerXY[0], playerPlane.getLUCord()[1] ], 
				(0,-3)
			)
			score -= CONFIG['firingCost']

	# New enemy
	if frame & CONFIG['enemyGenInterval'] == 0: #Add enemy every 0bxxxx+1 frame
		if random.randrange(100) < CONFIG['enemyGenPosib']:
			enemyPlanes[ createRandomKey(enemyPlanes) ] = EnemyPlane(
				[ random.randrange(30,CONFIG['screenSize'][0]-30) , -30 ], #Create obj out of screen but in margin
				enemyPlaneGen()
			)

	# Enemy move and fire
	for enemyID, enemyObj in enemyPlanes.items():
		newEnemyBullets = enemyObj.step()
		if enemyObj.endLife(): del enemyPlanes[enemyID] #Out of screen
		if enemyObj.isDmg() > CONFIG['displayAfterDmg']: del enemyPlanes[enemyID] #Killed by bullet

		for x in newEnemyBullets:
			bullets[ createRandomKey(bullets) ] = Bullet(x[0],x[1])

	# Bullet move
	for bulletID, bulletObj in bullets.items():
		bulletObj.move()
		if bulletObj.endLife(): del bullets[bulletID] #Out of screen

	# Hit
	for bulletID, bulletObj in bullets.items():
		for enemyID, enemyObj in enemyPlanes.items():
			if (
				bulletObj.centerXY[0] > enemyObj.getLUCord()[0] and
				bulletObj.centerXY[0] < enemyObj.getRDCord()[0] and
				bulletObj.centerXY[1] > enemyObj.getLUCord()[1] and
				bulletObj.centerXY[1] < enemyObj.getRDCord()[1]
			):
				del bullets[bulletID]
				enemyObj.changeHp(-bulletObj.getPower())
				score += CONFIG['hitBonus']
	
	for bulletID, bulletObj in bullets.items():
		if (
			bulletObj.centerXY[0] > playerPlane.getLUCord()[0] and
			bulletObj.centerXY[0] < playerPlane.getRDCord()[0] and
			bulletObj.centerXY[1] > playerPlane.getLUCord()[1] and
			bulletObj.centerXY[1] < playerPlane.getRDCord()[1]
		):
			del bullets[bulletID]
			playerPlane.changeHp(-bulletObj.getPower())

	#GAMEOVER: RAM
	for enemyID, enemyObj in enemyPlanes.items():
		if (
			enemyObj.centerXY[0] > playerPlane.getLUCord()[0] and
			enemyObj.centerXY[0] < playerPlane.getRDCord()[0] and
			enemyObj.centerXY[1] > playerPlane.getLUCord()[1] and
			enemyObj.centerXY[1] < playerPlane.getRDCord()[1]
		):
			gameover = 'AIR COLLISION'

	#GAMEOVER: SHOT DOWN
	if playerPlane.hp <= 0:
		gameover = 'KILLED BY ENEMY'
							

	# Display refresh
	bulletsCount = len(bullets)
	enemyCount = len(enemyPlanes)

	screen.fill((0,45,80))

	header = uiFont.render('HP: {} Bomb: {} Score: {}'.format( playerPlane.hp, playerPlane.ammo[1], score ), False, (255,255,255))
	screen.blit(header,(10,10))
	footer = uiFont.render('Debug: Frame {}; BulletCount {}; EnemyCount {};'.format(frame, bulletsCount, enemyCount), False, (255,255,255))
	screen.blit(footer,(10,CONFIG['screenSize'][1]-20))

	screen.blit( playerPlane.getImg(),playerPlane.getLUCord() )
	for bulletID, bulletObj in bullets.items(): screen.blit( bulletObj.getImg(),bulletObj.getLUCord() )
	for enemyID, enemyObj in enemyPlanes.items():screen.blit( enemyObj.getImg(), enemyObj.getLUCord() )


	pygame.display.flip()

	
