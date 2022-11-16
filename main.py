import pygame
import numpy
from car import car, entity
from menu import button, toggle, text
from network import load
from random import choice

pygame.init()

state = 'RUN'
SCREEN_SIZE = ( 450, 700)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Autodriven')
pygame.display.set_icon(pygame.image.load('./assets/favicon.png'))

MARK_FILL = 20
MARK_GAP = 10
lane_onset = -(MARK_FILL+MARK_GAP)
# manual = False

ROAD = pygame.Rect( 100, lane_onset, 300, 800)
SIDEWALL_LEFT = pygame.Rect( 90, lane_onset, 10, 800)
SIDEWALL_RIGHT = pygame.Rect( 400, lane_onset, 10, 800)

PLAYER_IMG = pygame.image.load('./assets/vehicles/yellow.png')
players = []
traffic = []

reload = button( (32,32), (40,120), './assets/sidebar/refresh.png', 'RELOAD')
save = button( (32,32), (40,200), './assets/sidebar/save.png', 'SAVE')
pause = toggle( (32,32), (40,280), './assets/sidebar/pause.png', './assets/sidebar/play.png', 'PAUSE', 'PLAY')

# TRAFFIC_XY = [ (350,-100), (240,-100), (130,-100), (180,-100), (290,-100) ]
TRAFFIC_XY = [ (350,-100), (240,-100), (130,-100) ]

TRAFFIC_IMG = [ './assets/vehicles/orange.png', './assets/vehicles/red.png', './assets/vehicles/truck.png',
				'./assets/vehicles/orange.png', './assets/vehicles/red.png', './assets/vehicles/cyan.png',
				'./assets/vehicles/semi.png', './assets/vehicles/white.png', './assets/vehicles/cyan.png',
				'./assets/vehicles/semi.png', './assets/vehicles/white.png']

TRAFFIC_IMG = list(map( pygame.image.load, TRAFFIC_IMG))
crowd_control = 1

TRAFFIC_EVENT = pygame.USEREVENT
pygame.time.set_timer( TRAFFIC_EVENT, 2000)

# MUTATION_EVENT = pygame.USEREVENT
# pygame.time.set_timer( MUTATION_EVENT, 2000)

def reset():
	global traffic, lane_onset, players, survivor

	# manual = False
	traffic = [ ]
	try:
		players = [ car( PLAYER_IMG, (240,600), network=load('./exp.pickle')) ]
	except(FileNotFoundError):
		players = [ car( PLAYER_IMG, (240,600)) ]
	survivor = players[0]
	for i in range(49):
		players.append( car( PLAYER_IMG, (240,600), network=players[0].ai.mutate(0.2)))
	lane_onset = -(MARK_FILL+MARK_GAP)

def mark_lanes( surface, color, start, end, length, gap):

	marks = [ (i,i+length) for i in range( start[1], end[1], length+gap)]
	for mark in marks:
		pygame.draw.line( surface, color, ( start[0], mark[0]), ( end[0], mark[1]))

user_info = text( (50,16), (250,650))
info_time_window = 0
reset()
survivor = players[0]

# SIMULATION LOOP
while state != 'END':

	# UPDATES
	pygame.time.delay(60)
	pygame.display.update()
	keys = pygame.key.get_pressed()
	clicked = False

	for event in pygame.event.get():

		# print(event)

		# CLOSE
		if event.type == pygame.QUIT:
			state = 'END'

		# MOUSE CLICK [ FOR SIDEBAR ]
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True

		# EVOLVE NETWORK
		# if event.type == MUTATION_EVENT and len(players):
			# for new_cars in range(3):
				# players.append( car( PLAYER_IMG, ( survivor.rect.x, survivor.rect.y),
					# network = survivor.ai.mutate(0.15),
					# speed = survivor.speed,
					# angle = survivor.angle))

		# INCREASE TRAFFIC
		if event.type == TRAFFIC_EVENT and state != 'PAUSED':

			# ELIMINATE OLD TRAFFIC
			for obstacle in traffic:
				if obstacle.rect.y > 800 or obstacle.rect.y < -40:
					traffic.remove(obstacle)

			new_row = TRAFFIC_XY.copy()
			for i in range(crowd_control):
				new_row.remove(choice(new_row))
			for place in new_row:
				traffic.append( entity( choice(TRAFFIC_IMG), place))

	# if manual:
		# LEFT = keys[pygame.K_LEFT] or keys[pygame.K_KP4]
		# UP = keys[pygame.K_UP] or keys[pygame.K_KP8]
		# RIGHT = keys[pygame.K_RIGHT] or keys[pygame.K_KP6]

	if reload.listen(clicked):
		reset()

	if save.listen(clicked):
		# survivor.ai.serialize('./test.pickle')
		survivor.ai.serialize('./exp.pickle')
		info_time_window = 20

	if keys[pygame.K_SPACE] or pause.listen(clicked):

		if state == 'RUN':
			state = 'PAUSED'

		elif state == 'PAUSED':
			state = 'RUN'

	elif state == 'PAUSED':
		continue

	if not len(players):
		continue

	# UPDATE SURVIVOR
	lead = min( [ player.rect.y for player in players ] )
	if survivor not in players or survivor.rect.y != lead:
		for player in players:
			if player.rect.y == lead:
					survivor = player

	# MOVEMENT
	if players:

		lane_onset += int(numpy.cos(numpy.radians(survivor.angle))*survivor.speed)
		if lane_onset > 0:
			lane_onset = -( MARK_FILL + MARK_GAP)

	for obstacle in traffic:
		obstacle.move( 8-survivor.speed)

	# BG
	SCREEN.fill((0,0,0))

	# SIDEBAR
	save.display(SCREEN)
	reload.display(SCREEN)
	pause.display( SCREEN, state != 'PAUSED')

	# ROAD AND SIDEWALL
	pygame.draw.rect( SCREEN, ( 32, 32, 32), ROAD)
	pygame.draw.rect( SCREEN, ( 255, 255, 255), SIDEWALL_LEFT)
	pygame.draw.rect( SCREEN, ( 255, 255, 255), SIDEWALL_RIGHT)

	# LANE MARKINGS
	mark_lanes( SCREEN, ( 255, 255, 0), ( 200, lane_onset), ( 200, 900), 20, 10)
	mark_lanes( SCREEN, ( 255, 255, 0), ( 300, lane_onset), ( 300, 900), 20, 10)

	# CAR
	for player in players:

		# MOVEMENT
		player.move([ SIDEWALL_LEFT, SIDEWALL_RIGHT] + [ i.rect for i in traffic])

		# SENSOR
		if player == survivor:
			player.cast_rays( SCREEN, [ SIDEWALL_LEFT, SIDEWALL_RIGHT] + [ i.rect for i in traffic])
			player.display(SCREEN)
		else:
			player.cast_rays( SCREEN, [ SIDEWALL_LEFT, SIDEWALL_RIGHT] + [ i.rect for i in traffic], False)
			player.display( SCREEN, 50)

		# ADJUST CAMERA
		if survivor.rect.y > 500 :
			player.rect.y -= 2
		else:
			player.rect.y += survivor.speed - player.speed

		# REMOVE DAMAGED CAR
		if player.damaged or player.rect.y > 800:
			players.remove(player)

	# TRAFFIC
	for obstacle in traffic:
		obstacle.display(SCREEN)

	# USER - INFO
	if state == 'PAUSED':
		user_info.display( SCREEN, 'SIMULATION PAUSED')
	if info_time_window:
		user_info.display( SCREEN, 'MODEL SAVED')
		info_time_window -= 1

pygame.quit()