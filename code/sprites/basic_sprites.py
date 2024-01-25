import pygame

from core.utils import import_surfaces, import_ysort, import_mask
from data.game_data import *


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
        self.root_image = import_surfaces(self.folder + "animation/")[0]
        self.image = self.root_image
        self.rect = self.image.get_rect(midbottom=self.position)

        # sort
        self.ysort = import_ysort(self.folder + "ysort.png")
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(self.folder + "mask.png")


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
