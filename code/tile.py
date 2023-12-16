# basic tiles of the game

import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups)
        self.tile_folder = path
        self.position = pos

        self.init()

    def init(self):
        # graphics
        self.surfaces = import_surfaces(self.tile_folder + "animation/")

        self.root_image = self.surfaces[0]
        self.image = self.root_image

        self.rect = self.image.get_rect(midbottom=self.position)

        # YSortGroup info
        self.ysort = import_ysort(self.tile_folder)
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(self.tile_folder, "mask")


class TeleportTile(Tile):
    def __init__(self, groups, path, pos, sprite_type) -> None:
        super().__init__(groups, path, pos)
        self.sprite_type = sprite_type

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
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups, path, pos)

        self.interact_mask = import_mask(self.tile_folder, "interact_mask")

    def interact(self) -> None:
        pass


class MagicTree(InteractiveTile):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups, path, pos)
        self.gain = 1
        self.level = config.TREE_LEVEL

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

    def level_up(self):
        self.level = config.TREE_LEVEL

        self.tile_folder = (
            config.PROJECT_FOLDER
            + f"/graphics/sprites/objects/magic_trees/{self.level}_magic_tree/"
        )

        self.init()

    def update(self):
        if self.level != config.TREE_LEVEL:
            self.level_up()


class MagicRock(InteractiveTile):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups, path, pos)
        self.gain = 1
        self.level = config.ROCK_LEVEL

        # cooldown
        self.cooldown = 1000
        self.pickup_time = 0
        self.picking_up = False

    def level_up(self):
        self.level = config.ROCK_LEVEL

        self.tile_folder = (
            config.PROJECT_FOLDER
            + f"/graphics/sprites/objects/magic_rocks/{self.level}_magic_rock/"
        )

        self.init()

    def interact(self) -> None:
        # check cooldown
        current_time = pygame.time.get_ticks()

        if not self.picking_up:
            self.picking_up = True
            self.pickup_time = pygame.time.get_ticks()
            config.STONE_AMOUNT += self.gain

        if self.picking_up and current_time - self.pickup_time >= self.cooldown:
            self.picking_up = False

    def update(self):
        if self.level != config.ROCK_LEVEL:
            self.level_up()
