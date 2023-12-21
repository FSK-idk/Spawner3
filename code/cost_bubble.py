import pygame

from utils import import_surfaces, import_surface
from game_data import GameData
from save_data import save_data


class CostBubble(pygame.sprite.Sprite):
    def __init__(self, groups: list, pos: (int, int), type: str) -> None:
        super().__init__(groups)
        self.position = pos
        self.type = type
        self.folder = GameData.project_folder + "/graphics/gui/bubbles/0_bubble/"

        # image
        self.surfaces = import_surfaces(self.folder)
        self.root_image = self.surfaces[0]
        self.image = self.root_image
        self.rect = self.image.get_rect(midbottom=self.position)

        # sort
        self.ysort = self.rect

        match self.type:
            case "woodcutter":
                wood, stone = GameData.woodcutter_upgrade[save_data.tree_level]
            case "miner":
                wood, stone = GameData.miner_upgrade[save_data.rock_level]
            case "laptop":
                wood, stone = GameData.cats_upgrade[save_data.cats_level]

        wood_surf = import_surface(
            GameData.project_folder + "/graphics/gui/icons/wood.png")
        stone_surf = import_surface(
            GameData.project_folder + "/graphics/gui/icons/stone.png")

        # show only wood
        if wood != 0 and stone == 0:
            wood_info_surf = GameData.font_mago16.render(
                f"{wood}", False, "White").convert_alpha()
            wood_info_rect = wood_info_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    - wood_info_surf.get_size()[0]
                    - wood_surf.get_size()[0]
                    - 1) // 2,
                    self.image.get_size()[1] // 2 - 2))

            wood_rect = wood_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    + wood_info_surf.get_size()[0]
                    - wood_surf.get_size()[0]
                    - 1) // 2 + 1,
                    self.image.get_size()[1] // 2))

            self.image.blit(wood_info_surf, wood_info_rect)
            self.image.blit(wood_surf, wood_rect)

        # show only stone
        if wood == 0 and stone != 0:
            stone_info_surf = GameData.font_mago16.render(
                f"{stone}", False, "White").convert_alpha()
            stone_info_rect = stone_info_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    - stone_info_surf.get_size()[0]
                    - stone_surf.get_size()[0]
                    - 1) // 2,
                    self.image.get_size()[1] // 2 - 2))

            stone_rect = stone_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    + stone_info_surf.get_size()[0]
                    - stone_surf.get_size()[0]
                    - 1) // 2 + 1,
                    self.image.get_size()[1] // 2))

            self.image.blit(stone_info_surf, stone_info_rect)
            self.image.blit(stone_surf, stone_rect)

        # show wood and stone
        if wood != 0 and stone != 0:
            wood_info_surf = GameData.font_mago16.render(
                f"{wood}", False, "White").convert_alpha()
            stone_info_surf = GameData.font_mago16.render(
                f"{stone}", False, "White").convert_alpha()

            wood_info_rect = wood_info_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    - wood_info_surf.get_size()[0]
                    - wood_surf.get_size()[0]
                    - 1) // 2,
                    self.image.get_size()[1] // 4 - 2))

            wood_rect = wood_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    + wood_info_surf.get_size()[0]
                    - wood_surf.get_size()[0]
                    - 1) // 2 + 1,
                    self.image.get_size()[1] // 4))

            stone_info_rect = stone_info_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    - stone_info_surf.get_size()[0]
                    - stone_surf.get_size()[0]
                    - 1) // 2,
                    self.image.get_size()[1] * 3 // 4 - 2))

            stone_rect = stone_surf.get_rect(
                midleft=((
                    self.image.get_size()[0]
                    + stone_info_surf.get_size()[0]
                    - stone_surf.get_size()[0]
                    - 1) // 2 + 1,
                    self.image.get_size()[1] * 3 // 4))

            self.image.blit(wood_info_surf, wood_info_rect)
            self.image.blit(wood_surf, wood_rect)
            self.image.blit(stone_info_surf, stone_info_rect)
            self.image.blit(stone_surf, stone_rect)
