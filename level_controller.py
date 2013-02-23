import os, pygame
import config as cfg
from random import random
from wall import Wall
from obstacle import Obstacle
from helicopter import Helicopter
from pygame.locals import *
from loaders import load_image, load_sound

class Level_controller:
    """ Controls the game logic, keeping track of scores and updating the level sprites."""
    def __init__(self):
        self.moving = True
        self.distance_travelled = 0 
        self.separation = cfg.INITIAL_SEPARATION
        self.bottom_wall_sprites = pygame.sprite.RenderPlain()
        self.top_wall_sprites = pygame.sprite.RenderPlain()
        self.obstacle_sprites = pygame.sprite.RenderPlain()
        self.number_of_blocks_added = 0

        for i in range(cfg.width/25):
            wall = Wall(25*i, cfg.height-75)
            self.bottom_wall_sprites.add(wall)
            self.last_added_bottom = wall
            ceiling = Wall(25*i)
            ceiling.rect.bottom = 75
            self.top_wall_sprites.add(ceiling)
            self.last_added_top = ceiling

    def move_level(self):
        if not self.moving: 
            return
        else:
            pass
        self.distance_travelled += cfg.scrollspeed
        self.bottom_wall_sprites.update()
        self.top_wall_sprites.update()
        self.obstacle_sprites.update()
        if self.last_added_bottom.rect.right <= cfg.width :
            height_diff = (random()-0.5) * 40
            new_height = min(cfg.height-5, self.last_added_bottom.rect.top + height_diff)
            new_height = max(5 + self.separation, new_height)
            wall = Wall(self.last_added_bottom.rect.right -1, new_height)
            self.bottom_wall_sprites.add(wall)
            self.last_added_bottom = wall
            ceiling = Wall(self.last_added_top.rect.right -1)
            ceiling.rect.bottom = new_height - self.separation
            self.last_added_top = ceiling
            self.top_wall_sprites.add(ceiling)


            #Put in obstacles at the appropriate juncture
            if(self.number_of_blocks_added % 7 == 0):
                obstacle_top_height = ceiling.rect.bottom + random() * (self.separation - 50)
                obstacle = Obstacle(ceiling.rect.left, obstacle_top_height)
                self.top_wall_sprites.add(obstacle)


            self.number_of_blocks_added += 1


            if(self.number_of_blocks_added % 50 == 0 ):
                self.separation = max(150, self.separation - 25 )

    def get_score(self):
        return self.distance_travelled/8