import pygame
import numpy

from network import feed_forward
from sensor import ray_caster

def collision_test( rect, obstacles):

	for obstacle in obstacles:
		if rect.colliderect(obstacle):
			return True
	return False

class entity:

	def __init__( self, img : pygame.surface.Surface, xy, size = None) -> None:

		self.xy = xy
		self.size = size if size else (img.get_width(), img.get_height())

		self.surface = pygame.transform.scale( img, size) if size else img
		self.rect = pygame.Rect( self.xy, ( self.surface.get_width(), self.surface.get_height()))
		self.rect.x = xy[0]
		self.rect.y = xy[1]

	def move( self, speed):

		self.rect.y -= speed

	def display( self, surface):

		surface.blit( self.surface, ( self.rect.x, self.rect.y))

class car(entity):

	def __init__(self, img, xy, size = None, network = None, speed = 0, angle = 0, acceleration = 1, friction = 1) -> None:

		self.angle = angle
		self.speed = speed

		self.acceleration = acceleration
		self.friction = friction
		self.damaged = False

		self.ai = network if network else feed_forward([5,6,3])
		self.sensor = ray_caster(100)
		self.alerts = [ 0, 0, 0, 0, 0]

		super().__init__( img, xy, size)

	def move( self, obstacles, directions = None):

		if self.damaged:
			return True

		if not directions:
			directions = self.ai.forward(self.alerts)

		if directions[1]:

			# ACCELERATION
			self.speed += self.acceleration if self.speed < 16 else 0

			#LEFT
			if directions[0]:
					self.angle += 1
			# RIGHT
			if directions[2]:
					self.angle -= 1
		else:
			# DECELERATION
			self.speed -= self.friction if self.speed > 0 else self.speed

		self.rect.x -= numpy.sin(numpy.radians(self.angle)) * self.speed
		self.damaged = collision_test( self.rect, obstacles)

		return self.damaged

	def cast_rays( self, surface, obstacles, display_rays = True):

		self.alerts = self.sensor.detect( self.rect.center, self.angle, obstacles)
		if display_rays:
			self.sensor.display( surface, self.rect.center)
		return self.sensor.alerts

	def display( self, surface, alpha = 255):
		
		buffer = pygame.transform.rotate( self.surface, self.angle)
		buffer.set_alpha(alpha)
		self.rect = surface.blit( buffer, ( self.rect.x, self.rect.y))
