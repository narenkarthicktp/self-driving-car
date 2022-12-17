import pygame
import numpy

distance = lambda p1,p2 : numpy.linalg.norm(numpy.array(p1) - numpy.array(p2))
SAFE = ( 0, 204, 153, 10)
DANGER = ( 204, 0, 102, 10)

class ray_caster():

	def __init__( self, coverage) -> None:

		self.nor = 5
		self.coverage = coverage
		self.alerts = [ .0, .0, .0, .0, .0]
		self.angles = [ -60, -80, -90, -100, -120]
		self.reach = [ (.0,.0) for i in range(self.nor)]

	def detect( self, position, angle, obstacles):

		self.alerts = [ .0 for i in range(self.nor)]
		for i,sensor in enumerate(self.angles):

			x = numpy.cos(numpy.radians(sensor - angle)) * self.coverage + position[0]
			y = numpy.sin(numpy.radians(sensor - angle)) * self.coverage + position[1]
			self.reach[i] = (x,y)

			for obstacle in obstacles:
				intercept = obstacle.clipline( position, (x,y))
				if intercept:
					self.alerts[i] = self.coverage - float(distance( position,intercept[0]))

		return self.alerts

	def display( self, surface, position):

		for i,alert in enumerate(self.alerts):
			if alert:
				pygame.draw.line( surface, DANGER, position, self.reach[i])
			else:
				pygame.draw.line( surface, SAFE, position, self.reach[i])



