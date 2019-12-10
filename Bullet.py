import sys, pygame, random

from config import *
from model import *

class BulletBase(Drawable):
	def __init__(self, model, cord, speed):
		Drawable.__init__(self, model, cord)
		self.speed = speed
		self.power = 10

	def move(self):
		Drawable.move(self, self.speed)

	def getPower(self):
		return self.power
		
class Bullet(BulletBase):
	def __init__(self, cord, speed):
		BulletBase.__init__(self, 'bullet', cord, speed)
		self.power = 12

class Bomb(BulletBase):
	def __init__(self, cord, speed):
		BulletBase.__init__(self, 'bomb', cord, speed)
		self.power = 250


def createBulletGroup():
	return 0
