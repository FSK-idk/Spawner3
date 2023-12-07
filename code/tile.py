# basic tiles of the game

import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, path) -> None:
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.tile_path = path

        # graphics
        self.surfaces = import_surfaces(path + "animation/")
        self.image = self.surfaces[0]
        self.rect = self.image.get_rect(midbottom=pos)

        # YSortGroup info
        self.ysort = import_ysort(path)
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(path, "mask")


class TeleportTile(Tile):
    def __init__(self, pos, groups, sprite_type, path) -> None:
        super().__init__(pos, groups, sprite_type, path)

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
    def __init__(self, pos, groups, sprite_type, path) -> None:
        super().__init__(pos, groups, sprite_type, path)

        self.interact_mask = import_mask(self.tile_path, "interact_mask")

    def interact(self) -> None:
        pass


class MagicTree(InteractiveTile):
    def __init__(self, pos, groups, sprite_type, path) -> None:
        super().__init__(pos, groups, sprite_type, path)
        self.gain = 1

        # cooldown
        self.cooldown = 1000
        self.pickup_time = 0
        self.picking_up = False

    def interact(self) -> None:
        # check cooldown
        current_time = pygame.time.get_ticks()

        if not self.picking_up:
            self.picking_up = True
            self.pickup_time = pygame.time.get_ticks()
            config.WOOD_AMOUNT += self.gain

        if self.picking_up and current_time - self.pickup_time >= self.cooldown:
            self.picking_up = False
