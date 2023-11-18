# level class where everything happens

import pygame
from settings import *
from support import *
from tile import *
from player import Player


class Level:
    def __init__(self):
        # general setup
        self.display_surf = pygame.display.get_surface()

        # sprite groups
        # visible sprites
        self.visible_sprites = YSortGroup()
        # collision sprites
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        # import layout and tileset
        layouts = {"test": import_csv_layout("./levels/test/test.csv")}
        graphics = {
            "test": import_surfaces("./graphics/test_tileset"),
        }

        # in each layout add new tiles in our groups
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE // 4
                    if row_index % 2 == 1:
                        x += TILESIZE // 2

                    if style == "test":
                        if val != "-1":
                            surf = graphics["test"][int(0)]  # later depends on val
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "test",
                                surf,
                            )

        self.player = Player((0, 0), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the level
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # get the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surf.blit(sprite.image, offset_pos)
