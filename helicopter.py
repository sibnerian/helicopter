import os, pygame
import config as cfg
from wall import Wall
from pygame.locals import *
from loaders import load_image, load_sound

class Helicopter(pygame.sprite.Sprite):
    """The helicopter- i.e., the only game object to be affected by gravity"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('Hellioclopater.gif', -1)
        self.image = pygame.transform.scale(self.image, cfg.helicopter_size)
        self.rect.size = subtract_one_from_tuple(cfg.helicopter_size)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centery = self.area.height/2
        self.rect.left = cfg.helicopter_initial_left
        self.acceleration = cfg.GRAVITY_ACCELERATION
        self.velocity = 0.0

    def update(self):
        self.rect = self.rect.move(0, self.velocity)
        self.velocity += self.acceleration
        self.velocty = min(self.velocity, 15)
    def hit_gas(self):
        self.acceleration = cfg.CLIMB_ACCELERATION

    def release_gas(self):
        self.acceleration = cfg.GRAVITY_ACCELERATION

def subtract_one_from_tuple(tup):
    a, b = tup
    return (a-1, b-1)