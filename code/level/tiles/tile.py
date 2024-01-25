import pygame

from core.utils import import_surfaces, import_ysort, import_mask
from data.game_data import *
from data.save_data import save_data


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 path: str, pos: (int, int)) -> None:
        super().__init__(groups)
        """
        Args:
            path: path to the tile folder
        """
        self.folder = path
        self.position = pos

        self.update_graphics()

    def update_graphics(self) -> None:
        # image
        self.surfaces = import_surfaces(self.folder + "animation/")
        self.root_image = self.surfaces[0]
        self.image = self.root_image
        self.rect = self.image.get_rect(midbottom=self.position)

        # sort
        self.ysort = import_ysort(self.folder + "ysort.png")
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(self.folder + "mask.png")


class TeleportSprite(StaticSprite):
    def __init__(self, groups: list, path: str,
                 pos: (int, int), type: str,
                 level_name: str) -> None:
        super().__init__(groups, path, pos)
        """
        Args:
            path: path to the tile folder
        """
        self.type = type
        self.level_name = level_name

    def teleport(self) -> None:
        match self.type:
            case "mountain":
                if self.level_name == "cave":
                    save_data.player_position = (400, 140)
                if self.level_name == "cats":
                    save_data.player_position = (520, 300)
            case "cave":
                save_data.player_position = (330, 530)
            case "cats":
                save_data.player_position = (500, 450)

        pygame.event.post(pygame.event.Event(
            UPDATE_GAMEPLAY_STATE,
            state=self.type,
            prev_state=self.level_name))


class InteractiveSprite(StaticSprite):
    def __init__(self, groups: list,
                 path: str, pos: (int, int)) -> None:
        super().__init__(groups, path, pos)
        """
        Args:
            path: path to the tile folder
        """
        # collision
        self.interact_mask = import_mask(self.folder + "interact_mask.png")

        # cooldown
        self.cooldown = 1000
        self.start_time = 0
        self.is_action = False

    def action(self) -> None:
        pass

    def interact(self) -> None:
        current_time = pygame.time.get_ticks()

        if not self.is_action:
            self.is_action = True
            self.start_time = pygame.time.get_ticks()

            self.action()

        if self.is_action and current_time - self.start_time >= self.cooldown:
            self.is_action = False


class MagicTree(InteractiveSprite):
    def __init__(self, groups: list,
                 path: str, pos: (int, int)) -> None:
        super().__init__(groups, path, pos)
        """
        Args:
            path: path to the tile folder
        """
        # info
        self.level = save_data.tree_level
        self.gain = GameData.wood_gain[self.level]

        self.level_up()

    def action(self) -> None:
        save_data.wood_amount += self.gain

    def level_up(self) -> None:
        self.level = save_data.tree_level
        self.gain = GameData.wood_gain[self.level]

        self.folder = (
            GameData.project_folder
            + f"/graphics/sprites/objects/magic_trees/{self.level}_magic_tree/")

        self.update_graphics()

    def update(self) -> None:
        if self.level != save_data.tree_level:
            self.level_up()


class MagicRock(InteractiveSprite):
    def __init__(self, groups: list,
                 path: str, pos: (int, int)) -> None:
        super().__init__(groups, path, pos)
        """
        Args:
            path: path to the tile folder
        """
        # info
        self.level = save_data.rock_level
        self.gain = GameData.stone_gain[self.level]

        self.level_up()

    def level_up(self) -> None:
        self.level = save_data.rock_level
        self.gain = GameData.stone_gain[self.level]

        self.folder = (
            GameData.project_folder
            + f"/graphics/sprites/objects/magic_rocks/{self.level}_magic_rock/")

        self.update_graphics()

    def action(self) -> None:
        save_data.stone_amount += self.gain

    def update(self) -> None:
        if self.level != save_data.rock_level:
            self.level_up()
