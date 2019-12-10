import os, pygame

from config import *

MODEL = {}
for x in os.listdir('./img/'):
	if x[-4:] == '.png':
		img = pygame.image.load('./img/'+x)
		MODEL[x[:-4]] = (img,img.get_size())

class Drawable:
	def __init__(self, modelName, centerXY):
		self.modelName = modelName
		self.size = MODEL[modelName][1]
		self.centerXY = centerXY

	def getLUCord(self): #Left-up
		return ( self.centerXY[0]-self.size[0]/2 , self.centerXY[1]-self.size[1]/2 )

	def getRDCord(self): #Right-down
		return ( self.centerXY[0]+self.size[0]/2 , self.centerXY[1]+self.size[1]/2 )

	def getImg(self):
		return MODEL[self.modelName][0]

	def move(self, displacement):
		self.centerXY[0] += displacement[0]
		self.centerXY[1] += displacement[1]

	def move_ip(self, placement):
		self.centerXY[0] = placement[0]
		self.centerXY[1] = placement[1]

	def endLife(self): #When the object is <margin> far from the outside of the screen, the object should be killed
		if self.centerXY[0] <                      0  - CONFIG['screenMargin']: return True
		if self.centerXY[0] > CONFIG['screenSize'][0] + CONFIG['screenMargin']: return True
		if self.centerXY[1] <                      0  - CONFIG['screenMargin']: return True
		if self.centerXY[1] > CONFIG['screenSize'][1] + CONFIG['screenMargin']: return True
		return False
