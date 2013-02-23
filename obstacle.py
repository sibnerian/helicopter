import os, pygame
import config as cfg
from wall import Wall
from pygame.locals import *
from loaders import load_image, load_sound

class Obstacle(Wall):
    """ A mischievously floating piece of rock to make the game interesting."""
    def __init__(self, left, top):
        Wall.__init__(self, left, top)
        self.image, self.rect = load_image('wall.png', None)
        self.image = pygame.transform.scale(self.image, cfg.obstacle_size )
        self.rect.size = cfg.obstacle_size
        self.rect.topleft = left, top

    def update(self):
        Wall.update(self)