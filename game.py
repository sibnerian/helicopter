#Import Modules
import os, pygame
import config as cfg
from pygame.locals import *
from random import random
from loaders import load_image, load_sound
from wall import Wall
from obstacle import Obstacle 
from helicopter import Helicopter
from level_controller import Level_controller

def run_game():
	#initialize pygame
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((cfg.width, cfg.height))
	pygame.display.set_caption('Helicopter')
	pygame.mouse.set_visible(1)

	#Create background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((25, 25, 25))

    #Prepare game objects
	controller = Level_controller()
	helicopter = Helicopter()
	copter = pygame.sprite.RenderPlain()
	copter.add(helicopter)

	#Main loop
	while 1: 
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == MOUSEBUTTONDOWN or \
            event.type == KEYDOWN and event.key == K_UP:
				helicopter.hit_gas()
			elif event.type is MOUSEBUTTONUP or \
            event.type == KEYUP and event.key == K_UP:
				helicopter.release_gas()
			elif event.type is KEYDOWN and event.key == K_r:
				controller = Level_controller()
				helicopter = Helicopter()
				copter = pygame.sprite.RenderPlain()
				copter.add(helicopter)

		#Draw the current frame
		screen.blit(background, (0,0))
		controller.bottom_wall_sprites.draw(screen)
		controller.top_wall_sprites.draw(screen)
		controller.obstacle_sprites.draw(screen)
		copter.draw(screen)
		screen.blit(get_score_surface(controller.get_score()), (10, 10))


		#Check for collisions, stopping the game if any are found
		if len(pygame.sprite.groupcollide(copter, controller.top_wall_sprites, 0, 0)) != 0 or \
			len(pygame.sprite.groupcollide(copter, controller.bottom_wall_sprites, 0, 0)) != 0 or \
			len(pygame.sprite.groupcollide(copter, controller.obstacle_sprites, 0, 0)) != 0:
			controller.moving = False
			text = get_game_over_surface(controller.get_score())
			textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/2)
			screen.blit(text, textpos)
		
		pygame.display.flip()

		#Move the level, updating all sprites in the process.
		#ONLY done if level is moving -- ie, game is not over
		controller.move_level()
		if controller.moving:
			copter.update()


#Creates a score display surface for a given score
def get_score_surface(score_num):
    if pygame.font:
        font = pygame.font.Font(None, 20)
        text = font.render("Score: " + str(score_num), 1, (250, 250, 250))
        return text

#Creates a "Game over" surface for a given score.
#Compares the flight of the helicopter to a score-appropriate bird.
def get_game_over_surface(score):
    if pygame.font: 
        font = pygame.font.Font(None, 45)
        birdnum = min(score/100, 7)
        text = font.render("Like a" + cfg.birds[birdnum] +", you flew "+str(score)+" meters. Press R to fly again.", 1, (250, 250, 250))
        return text
