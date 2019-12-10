import sys, pygame, random, math

from config import *
from model import *

class Plane(Drawable):
	def __init__(self, model, cord, hp):
		Drawable.__init__(self, model, cord)
		self.hp = hp

	def changeHp(self, dhp):
		self.hp += dhp
		if self.hp > 100:
			self.hp = 100
		if self.hp < 0:
			self.hp = 0
	

class PlayerPlane(Plane):
	def __init__(self, cord):
		Plane.__init__(self, 'player', cord, 100)
		self.speed = CONFIG['playerSpeed']
		self.ammo = CONFIG['playerAmmo'] #Placeholder (unlimited MG), Bomb
		self.ammoCooler = [0,0] #last fire time and CD config
		self.ammoRate = CONFIG['playerAmmoRate']

	def move(self, dx, dy):
		Plane.move(self, [ dx * self.speed, dy * self.speed ])
		if self.centerXY[0] <                      0 : self.centerXY[0] = 0
		if self.centerXY[0] > CONFIG['screenSize'][0]: self.centerXY[0] = CONFIG['screenSize'][0]
		if self.centerXY[1] <                      0 : self.centerXY[1] = 0
		if self.centerXY[1] > CONFIG['screenSize'][1]: self.centerXY[1] = CONFIG['screenSize'][1]

	def fire(self, weapon):
		if self.ammoCooler[weapon] > pygame.time.get_ticks() - self.ammoRate[weapon]: #Weapon is cooling (CD time)
			return False
		self.ammoCooler[weapon] = pygame.time.get_ticks()

		if ( weapon and self.ammo[weapon] <= 0 ): #Ammo out
			return False
		if weapon:
			self.ammo[weapon] -= 1

		return True

		
def enemyPlaneGen():
	#Return: (model, (motion:(x0,x1,x2...),(y0,y1,y2...)), (fireDir,Count,Sigma,Diff,rate in frame,speed), hp)
	enemyDatasheet = [
		('gunship', ((0,),(1.2,)), (180,5,20,5,40,4,False), 400), #Std gunship
		('gunship', ((0,),(1.2,)), (180,2,10,20,10,4,False), 400), #Quick-firing gunship
		('gunship', ((0,),(0.8,)), (180,2,80,5,60,3.5,False), 350), #Heavy metal
		('gunship', ((0,),(1.2,)), (180,36,10,60,40,4,False), 120) #Real GUN ship
	]
	if random.randrange(0,100) < CONFIG['enemyHeavyMetal']:
		return enemyDatasheet[random.randrange(0,4)]
	return ('enemyStd', ((0,),(2,)), (180,1,0,2,60,4,False), 40) #enemyStd


class EnemyPlane(Plane):
	def __init__(self, pos, (model,motionExp,fireExp,hp)):
		Plane.__init__(self, model, pos, hp)
		self.lifetime = 0 #Since object create
		self.deadtime = 0 #Record dead time, display dead img for a while, then destroy object

		self.fireDir = math.radians(fireExp[0]-90) # Bearing to trigonometric to rad
		self.fireCount = fireExp[1]
		self.fireSigma = math.radians(fireExp[2]) #Angle between each beam
		self.fireDiff = math.radians(fireExp[3]) #Angle error: tureAngle = +/-FireDiff
		self.fireRate = fireExp[4]
		self.fireSpeed = fireExp[5] #Bullet speed
		self.fireAim = fireExp[6] #Do not case fireDir, always aim the player

		self.motionExp = motionExp #pos = a0 + a1*x + a2*x^2 + a3*x^3 + ...

	def step(self): #Move the plane and return bullets
		self.lifetime += 1

		#Motion
		speed = [0,0]
		for x in range(len(self.motionExp[0])):
			speed[0] += ( self.lifetime ** x ) * self.motionExp[0][x]
		for y in range(len(self.motionExp[1])):
			speed[1] += ( self.lifetime ** y ) * self.motionExp[1][y]
		self.move(speed)

		#Check HP
		if ( self.hp <= 0 and not self.deadtime ): #Record only for once
			self.deadtime = self.lifetime

		#Dead: No action
		if self.deadtime:
			return []

		#Not dead: Shoot player
		bullet = []
		if self.lifetime % self.fireRate == 0:
			for i in range(self.fireCount):
				direction = (
					self.fireDir +
					(i-0.5*self.fireCount+0.5) * self.fireSigma +
					random.randrange(-100,100)*0.01*self.fireDiff
				)
				safeZone = math.sqrt( self.size[0] ** 2 + self.size[1] ** 2 ) * 0.5
				xMag = math.cos(direction)
				yMag = math.sin(direction)
				initPos = [ self.centerXY[0] + xMag * safeZone , self.centerXY[1] + yMag * safeZone ]
				bulletSpeed = ( xMag * self.fireSpeed , yMag * self.fireSpeed )
				bullet.append((initPos,bulletSpeed))
		return bullet

	def isDmg(self):
		if self.deadtime: return self.lifetime - self.deadtime
		return 0

	def getImg(self):
		if self.isDmg(): return MODEL['boooom'][0]
		return Plane.getImg(self)
