import pygame as pg
import numpy as np

from brain import Brain
class Score:
	def __init__(self,name,size):
		self.x_position = size[0]
		self.y_position = size[1]
		self.color = (0,0,0)
		self.font_size = 20
		self.name = name
		
	def show(self,score,screen):
		self.message = self.name + str(score)
		self.font = pg.font.Font(None,self.font_size)
		self.text = self.font.render(self.message, 1, self.color)
		screen.blit(self.text, (self.x_position,self.y_position))


class Tree:

	def __init__(self,size):
		self.tree_type = str(np.random.randint(0,5))
		self.tree = pg.image.load("./resource/tree"+self.tree_type+".png")
		self.scale = 100
		self.tree = pg.transform.scale(self.tree, (self.scale,self.scale))
		self.x = size[0]
		self.y = 259
		self.speed = 15
		self.hitbox_color = (np.random.randint(0,255), np.random.randint(0,255),np.random.randint(0,255))

	def draw(self,screen):
		screen.blit(self.tree,(self.x,self.y))
		self.hitbox = [self.x,self.y,self.scale,self.scale]
		#pg.draw.rect(screen,self.hitbox_color,self.hitbox,2)

	def isOver(self):
		return self.x + self.scale < 0

	def update(self):
		self.x-= self.speed

class Pig:

	def __init__(self,size,brain=None):
		self.scale = 80
		self.pigframe = [pg.transform.scale(pg.image.load("./resource/pigframes/"+str(i)+".png"),(self.scale,self.scale)) for i in range(20)]
		
		if brain == None:
			self.brain = Brain(1,8,2)
		else:
			self.brain = Brain(brain=brain,flag=True)

		self.pig_state = 0
		self.isjumping_up = False
		self.isjumping_down = False
	
		self.x = size[0]/10
		self.y = 286
		self.velocity = 30
		self.accleration = 2.6363
		self.max_upper_jump = 100

		self.score = 0

		self.hitbox_color = (np.random.randint(0,255), np.random.randint(0,255),np.random.randint(0,255))

	def draw(self,screen):
		if self.isjumping_up or self.isjumping_down :
			screen.blit(self.pigframe[5],(self.x,self.y))
		else:
			screen.blit(self.pigframe[self.pig_state],(self.x,self.y))
		self.pig_state = self.pig_state + 1
		if self.pig_state == 20:
			self.pig_state = 0
		self.hitbox = [self.x,self.y,self.scale,self.scale]
		#pg.draw.rect(screen,self.hitbox_color,self.hitbox,2)


	def jump(self):
		if self.isjumping_up:
			if self.y > self.max_upper_jump:
				self.y = self.y - self.velocity
				self.velocity = self.velocity - self.accleration
			if self.y <= self.max_upper_jump:
				self.isjumping_up = False
				self.isjumping_down = True

		elif self.isjumping_down :
			if self.y < 286:
				self.y = self.y + self.velocity
				self.velocity = self.velocity + self.accleration
			if self.y >= 286:
				self.isjumping_down = False
				self.y = 286
				self.velocity = 30
		else:
			pass

	def think(self,closest_obstacle):
		input = [closest_obstacle.x-self.x]
		prediction = self.brain.predict(input)
		if prediction[1][0]>prediction[0][0]:
			if self.y == 286:
				self.isjumping_up = True