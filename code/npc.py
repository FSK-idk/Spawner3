# npc class

import pygame
from settings import *


class NPC(pygame.sprite.Sprite):
    def __init__(self, npc_groups, bubble_gruops, pos, path) -> None:
        super().__init__(npc_groups)
        self.npc_folder = path

        # graphics
        self.surfaces = import_surfaces(self.npc_folder + "animation/")
        self.image = self.surfaces[0]
        self.rect = self.image.get_rect(midbottom=pos)

        # YSortGroup info
        self.ysort = import_ysort(self.npc_folder)
        self.ysort.midtop = self.rect.midtop

        # collision
        self.mask = import_mask(self.npc_folder, "mask")
        self.interact_mask = import_mask(self.npc_folder, "interact_mask")

        # bubble
        self.bubble_groups = bubble_gruops
        self.bubble_showing = False

    def interact(self, flag):
        if self.bubble_showing == False and flag == True:
            self.bubble = Bubble(self.bubble_groups, self.rect.midtop, "woodcutter")
            self.bubble_showing = True
        elif self.bubble_showing == True and flag == False:
            self.bubble.kill()
            self.bubble_showing = False


class Bubble(pygame.sprite.Sprite):
    def __init__(self, groups, pos, bubble_type):
        super().__init__(groups)
        self.bubble_type = bubble_type
        self.bubble_folder = config.PROJECT_FOLDER + "/graphics/gui/bubbles/0_bubble/"
        self.position = pos

        # graphics
        self.surfaces = import_surfaces(self.bubble_folder)
        self.image = self.surfaces[0]
        self.rect = self.image.get_rect(midbottom=self.position)
        self.ysort = self.rect

        font = pygame.font.Font(config.PROJECT_FOLDER + "/graphics/font/mago2.ttf", 16)

        wood, stone = GameData.WOODCUTTER_UPGRADE[config.TREE_LEVEL]

        wood_surf = import_surface(
            config.PROJECT_FOLDER + "/graphics/gui/icons/wood.png"
        )
        stone_surf = import_surface(
            config.PROJECT_FOLDER + "/graphics/gui/icons/stone.png"
        )

        # show only wood
        if wood != 0 and stone == 0:
            wood_info_surf = font.render(f"{wood}", False, "White").convert_alpha()
            wood_info_rect = wood_info_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        - wood_info_surf.get_size()[0]
                        - wood_surf.get_size()[0]
                        - 1
                    )
                    // 2,
                    self.image.get_size()[1] // 2 - 2,
                )
            )

            wood_rect = wood_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        + wood_info_surf.get_size()[0]
                        - wood_surf.get_size()[0]
                        - 1
                    )
                    // 2
                    + 1,
                    self.image.get_size()[1] // 2,
                )
            )

            self.image.blit(wood_info_surf, wood_info_rect)
            self.image.blit(wood_surf, wood_rect)

        # show only stone
        if wood == 0 and stone != 0:
            stone_info_surf = font.render(f"{stone}", False, "White").convert_alpha()
            stone_info_rect = stone_info_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        - stone_info_surf.get_size()[0]
                        - stone_surf.get_size()[0]
                        - 1
                    )
                    // 2,
                    self.image.get_size()[1] // 2 - 2,
                )
            )

            stone_rect = stone_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        + stone_info_surf.get_size()[0]
                        - stone_surf.get_size()[0]
                        - 1
                    )
                    // 2
                    + 1,
                    self.image.get_size()[1] // 2,
                )
            )

            self.image.blit(stone_info_surf, stone_info_rect)
            self.image.blit(stone_surf, stone_rect)

        # show wood and stone
        if wood != 0 and stone != 0:
            wood_info_surf = font.render(f"{wood}", False, "White").convert_alpha()
            stone_info_surf = font.render(f"{stone}", False, "White").convert_alpha()

            wood_info_rect = wood_info_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        - wood_info_surf.get_size()[0]
                        - wood_surf.get_size()[0]
                        - 1
                    )
                    // 2,
                    self.image.get_size()[1] // 4 - 2,
                )
            )

            stone_info_rect = stone_info_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        - stone_info_surf.get_size()[0]
                        - stone_surf.get_size()[0]
                        - 1
                    )
                    // 2,
                    self.image.get_size()[1] * 3 // 4 - 2,
                )
            )

            wood_rect = wood_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        + wood_info_surf.get_size()[0]
                        - wood_surf.get_size()[0]
                        - 1
                    )
                    // 2
                    + 1,
                    self.image.get_size()[1] // 4,
                )
            )

            stone_rect = stone_surf.get_rect(
                midleft=(
                    (
                        self.image.get_size()[0]
                        + stone_info_surf.get_size()[0]
                        - stone_surf.get_size()[0]
                        - 1
                    )
                    // 2
                    + 1,
                    self.image.get_size()[1] * 3 // 4,
                )
            )

            self.image.blit(wood_info_surf, wood_info_rect)
            self.image.blit(wood_surf, wood_rect)
            self.image.blit(stone_info_surf, stone_info_rect)
            self.image.blit(stone_surf, stone_rect)