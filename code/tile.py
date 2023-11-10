# basic tiles of the game

import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))
    ):
        # general setup
        super().__init__(groups)
        # type of sprite (for the future)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
