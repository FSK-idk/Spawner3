# level class where everything happens

import pygame
from settings import *
from utils import *
from tile import *
from player import *
from debug import debug


class Level:
    def __init__(self) -> None:
        # general setup
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        # visible sprites
        self.visible_sprites = YSortGroup()
        # collision sprites
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self) -> None:
        # import layout and sprites
        layouts = {
            "test": import_csv_layout(Config.PROJECT_FOLDER + "/levels/test/test.csv"),
            "mountain_constraints": import_csv_layout(
                Config.PROJECT_FOLDER + "/levels/mountain/mountain_constraints.csv"
            ),
        }
        graphics = {
            "test": import_surfaces(
                Config.PROJECT_FOLDER + "/graphics/sprites/ground/"
            ),
        }

        # in each layout add new tiles in our groups
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * Config.TILE_SIZE
                    y = row_index * Config.TILE_SIZE // 4
                    if row_index % 2 == 1:
                        x += Config.TILE_SIZE // 2

                    if style == "mountain_constraints":
                        if val != "-1":
                            # visible for debugging
                            surf = graphics["test"][0]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "test",
                                surf,
                            )

        self.player = Player((400, 400), [self.visible_sprites], self.obstacle_sprites)

    def run(self) -> None:
        self.visible_sprites.key_log()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        # debug fps
        self.clock = pygame.time.Clock()

        # general setup
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2

        # creating the floor
        self.floor_surf = pygame.image.load(
            Config.PROJECT_FOLDER + "/graphics/background/mountain.png"
        ).convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        # coeff to resize temp surface
        self.resize_coeff = 2
        self.resize_step = 0.1
        self.max_resize_coeff = 2
        self.min_resize_coeff = 1

        # creating temp surface with alpha channel to resize level
        self.temp_surface = pygame.surface.Surface(
            self.display_surf.get_size(), pygame.SRCALPHA
        )

    def key_log(self) -> None:
        # check mouse events
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

    def custom_draw(self, player) -> None:
        display_size = self.display_surf.get_size()

        # do transparent background for temp surface
        self.temp_surface.fill((0, 0, 0, 0))

        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.temp_surface.blit(self.floor_surf, floor_offset_pos)

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

        # debug fps
        self.clock.tick()
        debug(self.clock.get_fps())
