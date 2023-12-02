# basic tiles of the game

import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE)),
    ) -> None:
        # general setup
        super().__init__(groups)
        # type of sprite (for the future)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(midbottom=pos)
        self.hitbox = pygame.Rect(
            pos[0] - self.image.get_size()[0] / 2,
            pos[1] - Config.TILE_SIZE / 2,
            self.image.get_size()[0],
            Config.TILE_SIZE / 2,
        )
        # self.hitbox = self.rect.inflate(0, -self.image.get_size()[1] // 4)


class MagicTree(Tile):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE)),
    ) -> None:
        super().__init__(pos, groups, sprite_type, surface)

    def interact(self):
        Config.TEST_DATA += 1
