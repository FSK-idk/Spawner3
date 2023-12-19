# head-up display to show amount of wood and stones

import pygame
from settings import *
from utils import *


class HUD(pygame.sprite.Sprite):
    def __init__(self, groups, surface) -> None:
        super().__init__(groups)

        # graphics
        self.display_surf = surface

        self.font = pygame.font.Font(
            config.PROJECT_FOLDER + "/graphics/font/Clarity.ttf", 48
        )

        # wood
        self.wood_surf = import_surface(
            config.PROJECT_FOLDER + "/graphics/gui/icons/wood.png"
        )
        self.wood_surf = pygame.transform.scale(
            self.wood_surf,
            (
                (self.wood_surf.get_size()[0] * 8),
                (self.wood_surf.get_size()[1] * 8),
            ),
        )
        self.wood_rect = self.wood_surf.get_rect(
            center=(
                self.display_surf.get_size()[0] // 2 - self.wood_surf.get_size()[0],
                self.display_surf.get_size()[1] * 11 // 12,
            )
        )

        # stone
        self.stone_surf = import_surface(
            config.PROJECT_FOLDER + "/graphics/gui/icons/stone.png"
        )

        self.stone_surf = pygame.transform.scale(
            self.stone_surf,
            (
                (self.stone_surf.get_size()[0] * 8),
                (self.stone_surf.get_size()[1] * 8),
            ),
        )
        self.stone_rect = self.stone_surf.get_rect(
            center=(
                self.display_surf.get_size()[0] // 2 + self.stone_surf.get_size()[0],
                self.display_surf.get_size()[1] * 11 // 12,
            )
        )

        self.update_info()

    def update_info(self):
        self.wood = config.WOOD_AMOUNT
        self.stone = config.STONE_AMOUNT

        # wood info
        self.wood_info_surf = self.font.render(
            f"{self.wood} ", False, "White"
        ).convert_alpha()
        self.wood_info_rect = self.wood_info_surf.get_rect(
            midright=self.wood_rect.midleft
        )

        # stone info
        self.stone_info_surf = self.font.render(
            f" {self.stone}", False, "White"
        ).convert_alpha()
        self.stone_info_rect = self.stone_info_surf.get_rect(
            midleft=self.stone_rect.midright
        )

        self.image = pygame.surface.Surface(
            self.display_surf.get_size(), pygame.SRCALPHA
        )

        # draw
        self.image.blit(self.wood_surf, self.wood_rect)
        self.image.blit(self.wood_info_surf, self.wood_info_rect)
        self.image.blit(self.stone_surf, self.stone_rect)
        self.image.blit(self.stone_info_surf, self.stone_info_rect)

        self.rect = self.image.get_rect()

    def update(self):
        if self.wood != config.WOOD_AMOUNT or self.stone != config.STONE_AMOUNT:
            self.update_info()
