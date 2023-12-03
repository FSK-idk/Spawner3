# basic tiles of the game

import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((config.TILE_SIZE, config.TILE_SIZE)),
    ) -> None:
        # general setup
        super().__init__(groups)
        self.sprite_type = sprite_type

        # graphics
        self.image = surface
        self.rect = self.image.get_rect(midbottom=pos)
        self.hitbox = pygame.Rect(
            pos[0] - self.image.get_size()[0] / 2,
            pos[1] - config.TILE_SIZE / 2,
            self.image.get_size()[0],
            config.TILE_SIZE / 2,
        )


class TeleportTile(Tile):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((config.TILE_SIZE, config.TILE_SIZE)),
    ) -> None:
        super().__init__(pos, groups, sprite_type, surface)

    def teleport(self):
        # change level name and player position
        if self.sprite_type == "teleport_mountain":
            if config.CURRENT_LEVEL == "cave":
                config.PLAYER_POS = (400, 150)
            if config.CURRENT_LEVEL == "cats":
                config.PLAYER_POS = (500, 325)
            config.CURRENT_LEVEL = "mountain"
        if self.sprite_type == "teleport_cave":
            config.CURRENT_LEVEL = "cave"
            config.PLAYER_POS = (350, 550)
        if self.sprite_type == "teleport_cats":
            config.CURRENT_LEVEL = "cats"
            config.PLAYER_POS = (500, 450)


class InteractiveTile(Tile):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((config.TILE_SIZE, config.TILE_SIZE)),
    ) -> None:
        super().__init__(pos, groups, sprite_type, surface)

        self.interact_area = self.hitbox.inflate(5, 5)

    def interact(self) -> None:
        # debug
        config.TEST_DATA += 1
        pass


class MagicTree(InteractiveTile):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((config.TILE_SIZE, config.TILE_SIZE)),
    ) -> None:
        super().__init__(pos, groups, sprite_type, surface)

        self.gain = 1

        # cooldown
        self.cooldown = 1000
        self.pickup_time = 0
        self.picking_up = False

    def interact(self) -> None:
        super().interact()

        # check cooldown
        current_time = pygame.time.get_ticks()

        if not self.picking_up:
            self.picking_up = True
            self.pickup_time = pygame.time.get_ticks()
            config.WOOD_AMOUNT += self.gain

        if self.picking_up and current_time - self.pickup_time >= self.cooldown:
            self.picking_up = False
