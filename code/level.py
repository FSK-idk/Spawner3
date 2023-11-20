# level class where everything happens

import pygame
from pygame.surface import Surface

from settings import *
from support import *
from tile import *
from player import Player


class Level:
    def __init__(self):
        # general setup
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        # visible sprites
        self.visible_sprites = YSortGroup()
        # collision sprites
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        # import layout and tileset
        layouts = {
            "test": import_csv_layout(get_parent_dir() + "/levels/test/test.csv"),
            "mountain_constraints": import_csv_layout(
                get_parent_dir() + "/levels/mountain/mountain_constraints.csv"
            ),
        }
        graphics = {
            "test": import_surfaces(get_parent_dir() + "/graphics/test_tileset"),
        }

        # in each layout add new tiles in our groups
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE // 4
                    if row_index % 2 == 1:
                        x += TILESIZE // 2

                    if style == "mountain_constraints":
                        if val != "-1":
                            # visible for debugging
                            surf = graphics["test"][int(0)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "test",
                                surf,
                            )

        self.player = Player((200, 200), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.key_log()

        # update and draw the level
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2

        # coeff to resize temp surface
        self.resize_coeff = 1
        self.resize_step = 0.1
        self.max_resize_coeff = 2
        self.min_resize_coeff = 1

        # creating temp surface with alpha channel to resize level
        self.temp_surface = Surface(self.display_surf.get_size(), pygame.SRCALPHA)

    def key_log(self):
        mousewheel_event = pygame.event.get(pygame.MOUSEBUTTONUP)

        if not mousewheel_event:
            return

        if mousewheel_event[0].button == 4:
            self.resize_coeff += self.resize_step

        elif mousewheel_event[0].button == 5:
            self.resize_coeff -= self.resize_step

        if self.resize_coeff > self.max_resize_coeff:
            self.resize_coeff = self.max_resize_coeff

        if self.resize_coeff < self.min_resize_coeff:
            self.resize_coeff = self.min_resize_coeff

    def custom_draw(self, player):
        display_size = self.display_surf.get_size()

        # do transparent background for temp surface
        self.temp_surface.fill((0, 0, 0, 0))

        # get the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.temp_surface.blit(sprite.image, offset_pos)

        display_size = self.display_surf.get_size()
        resized_size = (
            display_size[0] * self.resize_coeff,
            display_size[1] * self.resize_coeff,
        )
        self.display_surf.blit(
            pygame.transform.scale(self.temp_surface, resized_size),
            (
                (display_size[0] - resized_size[0]) / 2,
                (display_size[1] - resized_size[1]) / 2,
            ),
        )
