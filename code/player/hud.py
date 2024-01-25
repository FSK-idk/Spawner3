import pygame

from core.utils import import_surface
from data.game_data import GameData
from data.save_data import save_data


class HUD(pygame.sprite.Sprite):
    def __init__(self, groups: list,
                 display: pygame.Surface) -> None:
        super().__init__(groups)

        self.display = display
        display_width, display_height = self.display.get_size()

        self.wood = save_data.wood_amount
        self.stone = save_data.stone_amount

        # wood image
        self.wood_surf = import_surface(
            GameData.project_folder + "/graphics/gui/icons/wood.png")
        self.wood_surf = pygame.transform.scale(
            self.wood_surf, (
                (self.wood_surf.get_size()[0] * 8),
                (self.wood_surf.get_size()[1] * 8)))
        self.wood_rect = self.wood_surf.get_rect(
            center=(
                display_width // 2 - self.wood_surf.get_size()[0],
                display_height * 11 // 12))

        # stone image
        self.stone_surf = import_surface(
            GameData.project_folder + "/graphics/gui/icons/stone.png")
        self.stone_surf = pygame.transform.scale(
            self.stone_surf, (
                (self.stone_surf.get_size()[0] * 8),
                (self.stone_surf.get_size()[1] * 8)))
        self.stone_rect = self.stone_surf.get_rect(
            center=(
                display_width // 2 + self.stone_surf.get_size()[0],
                display_height * 11 // 12))

        self.update_sprite()

    def update_sprite(self) -> None:
        # wood info
        self.wood_info_surf = GameData.font_lana50.render(
            f"{self.wood} ", False, "White").convert_alpha()
        self.wood_info_rect = self.wood_info_surf.get_rect(
            midright=self.wood_rect.midleft)

        # stone info
        self.stone_info_surf = GameData.font_lana50.render(
            f" {self.stone}", False, "White").convert_alpha()
        self.stone_info_rect = self.stone_info_surf.get_rect(
            midleft=self.stone_rect.midright)

        self.image = pygame.Surface(
            self.display.get_size(), pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.image.blit(self.wood_surf, self.wood_rect)
        self.image.blit(self.wood_info_surf, self.wood_info_rect)
        self.image.blit(self.stone_surf, self.stone_rect)
        self.image.blit(self.stone_info_surf, self.stone_info_rect)

    def update_info(self) -> None:
        self.wood = save_data.wood_amount
        self.stone = save_data.stone_amount

    def update(self) -> None:
        if (self.wood != save_data.wood_amount
                or self.stone != save_data.stone_amount):
            self.update_info()
            self.update_sprite()
