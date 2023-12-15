# level class where everything happens

import pygame
from settings import *
from utils import *
from tile import *
from player import *
from npc import *
from debug import debug


class Level:
    def __init__(self) -> None:
        # general setup
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # level info
        self.name = "mountain"

        # map setup
        self.create_map()

    def create_map(self) -> None:
        # import level graphics
        match self.name:
            case "mountain":
                layouts = import_layouts(
                    "mountain", ["constraints", "teleports", "magic_trees", "npcs"]
                )
            case "cave":
                layouts = import_layouts(
                    "cave", ["constraints", "teleports", "magic_rocks", "npcs"]
                )

            case "cats":
                layouts = import_layouts("cats", ["constraints", "teleports"])

        # set floor
        floor = pygame.image.load(
            config.PROJECT_FOLDER + f"/graphics/background_images/{self.name}.png"
        ).convert_alpha()
        self.visible_sprites.set_floor(floor)

        # in each layout add new tiles in our groups
        for layer, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    # set position
                    x = col_index * config.TILE_SIZE
                    y = row_index * config.TILE_SIZE // 4
                    if row_index % 2 == 1:
                        x += config.TILE_SIZE // 2

                    match layer:
                        case "constraints":
                            if val != "-1":
                                if (
                                    val == "-1"
                                    or (val == "4" and self.name == "mountain")
                                    or (val == "3" and self.name == "cave")
                                    or (val == "1" and self.name == "cats")
                                ):
                                    path = (
                                        config.PROJECT_FOLDER
                                        + "/graphics/sprites/background/trees/0_tree/"
                                    )
                                    Tile((x, y), [self.obstacle_sprites], path)

                                else:
                                    if self.name == "mountain":
                                        path = (
                                            config.PROJECT_FOLDER
                                            + f"/graphics/sprites/background/trees/{int(val)}_tree/"
                                        )
                                    elif self.name == "cave":
                                        path = (
                                            config.PROJECT_FOLDER
                                            + f"/graphics/sprites/background/rocks/{int(val)}_rock/"
                                        )
                                    else:
                                        path = (
                                            config.PROJECT_FOLDER
                                            + "/graphics/sprites/background/walls/0_wall/"
                                        )

                                    Tile(
                                        (x, y),
                                        [self.visible_sprites, self.obstacle_sprites],
                                        path,
                                    )

                        case "teleports":
                            sprite_type = ["mountain", "cave", "cats"]
                            if val != "-1":
                                # visible for debugging
                                path = (
                                    config.PROJECT_FOLDER
                                    + f"/graphics/sprites/teleports/{int(val)}_{sprite_type[int(val)]}/"
                                )
                                TeleportTile(
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites],
                                    path,
                                    "teleport_" + sprite_type[int(val)],
                                )

                        case "magic_trees":
                            if val == "0":
                                path = (
                                    config.PROJECT_FOLDER
                                    + "/graphics/sprites/objects/magic_trees/0_magic_tree/"
                                )
                                MagicTree(
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites],
                                    path,
                                )
                        case "magic_rocks":
                            if val == "0":
                                path = (
                                    config.PROJECT_FOLDER
                                    + "/graphics/sprites/objects/magic_rocks/0_magic_rock/"
                                )
                                MagicRock(
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites],
                                    path,
                                )

                        case "npcs":
                            sprite_type = ["mesenev", "woodcutter", "miner"]
                            if val != "-1":
                                path = (
                                    config.PROJECT_FOLDER
                                    + f"/graphics/sprites/npcs/{int(val)}_{sprite_type[int(val)]}/"
                                )
                                NPC(
                                    [self.visible_sprites, self.obstacle_sprites],
                                    [self.visible_sprites],
                                    path,
                                    (x, y),
                                    sprite_type[int(val)],
                                )

        self.player = Player(
            config.PLAYER_POS, [self.visible_sprites], self.obstacle_sprites
        )

    def change_level(self):
        if config.CURRENT_LEVEL != self.name:
            self.name = config.CURRENT_LEVEL
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.create_map()

    def run(self) -> None:
        self.change_level()
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

        # floor
        self.floor_surf = pygame.image.load(
            config.PROJECT_FOLDER + "/graphics/background_images/mountain.png"
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

    def set_floor(self, floor) -> None:
        # creating floor
        self.floor_surf = floor
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

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
        floor_offset_pos = (
            self.floor_rect.topleft
            - self.offset
            - pygame.Vector2(config.TILE_SIZE // 2, 0.5 * config.TILE_SIZE)
        )
        self.temp_surface.blit(self.floor_surf, floor_offset_pos)

        # draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.ysort.bottom):
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

        # debug
        self.clock.tick()
        debug(self.clock.get_fps())
        debug(f"Wood: {config.WOOD_AMOUNT}", 30)
        debug(f"Stone: {config.STONE_AMOUNT}", 50)
        debug(f"Interact: {HotKeys.is_pressed(HotKeys.interact)}", 70)
