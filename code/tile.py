import pygame
from settings import *

'''
Classe Tile
Os "objetos" de facto do jogo.
'''

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups,surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = None
        self.image = surface
        
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect ## inflar aqui também ?
