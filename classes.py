#Import Modules
import os, pygame
from pygame.locals import *
from random import random
from config import *
from loaders import load_image, load_sound


class Wall(pygame.sprite.Sprite):
    """The boundaries of the helicopter's tunnel"""
    def __init__(self, left=600, top = 200):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('wall.png', None)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = left, top
        self.moving = True
        self.move = -1 * scrollspeed
    def update(self):
        if(not self.moving):
            return
        newpos = self.rect.move((self.move, 0))
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_rect().right :
            self.kill()
        self.rect = newpos


class Obstacle(Wall):
    """ A mischievously floating piece of rock to make the game interesting."""
    def __init__(self, left, top):
        Wall.__init__(self, left, top)
        self.image, self.rect = load_image('wall.png', None)
        self.image = pygame.transform.scale(self.image, obstacle_size )
        self.rect.size = obstacle_size
        self.rect.topleft = left, top

    def update(self):
        Wall.update(self)

class Helicopter(pygame.sprite.Sprite):
    """The helicopter- i.e., the only game object to be affected by gravity"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Hellioclopater.gif', -1)
        self.image = pygame.transform.scale(self.image, (135/2, 75/2))
        self.rect.size = 133/2, 73/2
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centery = self.area.height/2
        self.rect.left = 25
        self.acceleration = GRAVITY_ACCELERATION
        self.velocity = 0.0

    def update(self):
        if scrollspeed ==  0 :
            return
        self.rect = self.rect.move(0, self.velocity)
        self.velocity += self.acceleration
        self.velocty = min(self.velocity, 15)
    def hit_gas(self):
        self.acceleration = CLIMB_ACCELERATION

    def release_gas(self):
        self.acceleration = GRAVITY_ACCELERATION

class Level_controller:
    """ Controls the game logic, keeping track of scores and updating the level sprites."""
    def __init__(self):
        self.moving = True
        self.distance_travelled = 0 
        self.separation = INITIAL_SEPARATION
        self.bottom_wall_sprites = pygame.sprite.RenderPlain()
        self.top_wall_sprites = pygame.sprite.RenderPlain()
        self.obstacle_sprites = pygame.sprite.RenderPlain()
        self.number_of_blocks_added = 0

        for i in range(width/25):
            wall = Wall(25*i, height-75)
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
        self.distance_travelled += scrollspeed
        self.bottom_wall_sprites.update()
        self.top_wall_sprites.update()
        self.obstacle_sprites.update()
        if self.last_added_bottom.rect.right <=width :
            height_diff = (random()-0.5) * 40
            new_height = min(height-5, self.last_added_bottom.rect.top + height_diff)
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