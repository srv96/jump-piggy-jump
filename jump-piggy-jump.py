import pygame as pg
import numpy as np

from sprite import Score,Tree,Pig


class App:
	def __init__(self):
		self.window_width,self.window_height = 700, 400
		self.size = (self.window_width,self.window_height)
		self.clock_tick_rate=20
		self.exit = False
		self.trees = []
		self.clock = pg.time.Clock()
		self.background_image_path = "./resource/background.jpg"

		self.min_appear_time,self.max_appear_time =30,60
		self.obstacle_appear_time = 0

		self.population = 50
		self.oldPigs = []
		self.pigs = []
		self.remaining = self.population

		self.gen = 0
		self.generation = Score("gen :",(self.window_width-100,0))
		self.score = 0
		self.scoreboard = Score("gen score :",(self.window_width-100,15))
		self.highestScore = 0
		self.highestscoreboard = Score("high score :",(self.window_width-100,30))
		

	def on_init(self):
		pg.init()
		self.screen = pg.display.set_mode(self.size)

	def on_cleanup(self):
		pg.quit()

	def resetState(self):
		self.score = 0
		self.pigs =[]
		self.trees=[]
		self.interval=0

	def is_hit(self,pig,obstacle):
		if ((pig.x + pig.scale >= obstacle.x and pig.x +pig.scale <= obstacle.x + pig.scale) or (pig.x>=obstacle.x and pig.x<=obstacle.x+obstacle.scale)) and ((pig.y >= obstacle.y - obstacle.scale and pig.y <= obstacle.y) or (pig.y - pig.scale >= obstacle.y - obstacle.scale and pig.y -pig.scale <= obstacle.y)) :
			return True

	def on_render(self):
		self.screen.blit(self.background_image,[0,0])

		for pig in self.pigs:
			pig.draw(self.screen)

		for tree in self.trees:
			tree.draw(self.screen)
			tree.update()

		if len(self.trees)>0:
			if self.trees[0].isOver():
				self.trees.remove(self.trees[0])

		self.generation.show(self.gen,self.screen)
		self.scoreboard.show(self.score,self.screen)
		self.highestscoreboard.show(self.highestScore,self.screen)
		

	def on_execute(self):
		self.on_init()
		pg.display.set_caption("Jump Piggy Jump")
		self.background_image = pg.image.load(self.background_image_path).convert()
		self.background_image = pg.transform.scale(self.background_image,self.size)

		while(self.exit==False):
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.exit = True
				if event.type == pg.K_SPACE:
					self.pigs[0].isjumping_up = True

			if len(self.pigs) == 0:
				self.nextGeneration()

			pg.display.flip()
			closest = self.closest_obstacle()

			for pig in self.pigs:
				pig.jump()

			if self.obstacle_appear_time == 0:
				self.trees.append(Tree(self.size))
				self.obstacle_appear_time = np.random.randint(self.min_appear_time,self.max_appear_time)

			if closest != None:
				for pig in self.pigs:
					pig.think(closest)
					if self.is_hit(pig,closest):
						self.oldPigs.append(pig)
						self.pigs.remove(pig)
					else:
						pig.score = self.score

			if len(self.pigs) == 0 :
				self.nextGeneration()

			self.clock.tick(self.clock_tick_rate)
			self.score = self.score+1
			self.obstacle_appear_time-=1

			self.on_render()

		self.on_cleanup()

	def closest_obstacle(self):
		for tree in self.trees:
			if tree.x + tree.scale < self.pigs[0].x:
				continue
			else:
				return tree

	def best_score(self):
		max_score= 0
		if len(self.oldPigs) != 0:
			for pig in self.oldPigs:
				if pig.score > max_score:
					max_score = pig.score
		if max_score > self.highestScore:
			self.highestScore = max_score
		return self.highestScore

	def nextGeneration(self):
		self.resetState()
		if len(self.oldPigs)==0:
			for i in range(self.population):
				self.pigs.append(Pig(self.size))
		else:
			self.normalize_fitness()
			for i in range(self.population):
				self.pigs.append(self.poolSelection())
		self.highestScore = self.best_score()
		self.gen+=1
		self.oldPigs=[]

	def normalize_fitness(self):
		total = 0
		for pig in self.oldPigs:
			total+=pig.score 
			
		for pig in self.oldPigs:
			pig.fitness = pig.score/total

	def poolSelection(self):
		threshold = 0
		for pig in self.oldPigs:
			if pig.fitness > threshold:
				mother_pig = pig
				threshold = pig.fitness

		child = Pig(size = self.size,brain = mother_pig.brain)
		child.brain.mutate()

		return child


if __name__=="__main__": 
	app = App()
	app.on_execute()



		
