# basic tiles of the game

import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups)
        self.folder = path
        self.position = pos

        self.update_graphics()

    def update_graphics(self):
        # picture
        self.surfaces = import_surfaces(self.folder + "animation/")

        self.root_image = self.surfaces[0]
        self.image = self.root_image

        self.rect = self.image.get_rect(midbottom=self.position)

        # sorting by Y info
        self.ysort = import_ysort(self.folder)
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(self.folder, "mask")


class TeleportTile(Tile):
    def __init__(self, groups, path, pos, sprite_type, level_name) -> None:
        super().__init__(groups, path, pos)
        self.sprite_type = sprite_type
        self.level_name = level_name

    def teleport(self):
        # change level name and player position
        if self.sprite_type == "teleport_mountain":
            if self.level_name == "cave":
                config.PLAYER_POS = (200, 200)

            if self.level_name == "cats":
                config.PLAYER_POS = (500, 325)

            pygame.event.post(
                pygame.event.Event(
                    UPDATE_GAMEPLAY_STATE,
                    state="mountain",
                    prev_state=self.level_name,
                )
            )

            # config.CURRENT_LEVEL = "mountain"
        if self.sprite_type == "teleport_cave":
            config.PLAYER_POS = (350, 550)

            pygame.event.post(
                pygame.event.Event(
                    UPDATE_GAMEPLAY_STATE, state="cave", prev_state=self.level_name
                )
            )

        if self.sprite_type == "teleport_cats":
            config.PLAYER_POS = (500, 450)

            pygame.event.post(
                pygame.event.Event(
                    UPDATE_GAMEPLAY_STATE, state="cats", prev_state=self.level_name
                )
            )


class InteractiveTile(Tile):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups, path, pos)

        # interctive data
        self.interact_mask = import_mask(self.folder, "interact_mask")


class MagicTree(InteractiveTile):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups, path, pos)
        self.gain = GameData.WOOD_GAIN[config.TREE_LEVEL]
        self.level = config.TREE_LEVEL
        self.level_up()

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
        self.gain = GameData.WOOD_GAIN[config.TREE_LEVEL]

        self.folder = (
            config.PROJECT_FOLDER
            + f"/graphics/sprites/objects/magic_trees/{self.level}_magic_tree/"
        )

        self.update_graphics()

    def update(self):
        if self.level != config.TREE_LEVEL:
            self.level_up()


class MagicRock(InteractiveTile):
    def __init__(self, groups, path, pos) -> None:
        super().__init__(groups, path, pos)
        self.gain = GameData.STONE_GAIN[config.ROCK_LEVEL]
        self.level = config.ROCK_LEVEL
        self.level_up()

        # cooldown
        self.cooldown = 1000
        self.pickup_time = 0
        self.picking_up = False

    def level_up(self):
        self.level = config.ROCK_LEVEL
        self.gain = GameData.STONE_GAIN[config.ROCK_LEVEL]

        self.folder = (
            config.PROJECT_FOLDER
            + f"/graphics/sprites/objects/magic_rocks/{self.level}_magic_rock/"
        )

        self.update_graphics()

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
