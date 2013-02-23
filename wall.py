#Import Modules
import os, pygame
import config as cfg
from pygame.locals import *
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
        self.move = -1 * cfg.scrollspeed
    def update(self):
        if(not self.moving):
            return
        newpos = self.rect.move((self.move, 0))
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_rect().right :
            self.kill()
        self.rect = newpos