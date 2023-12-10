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
        self.visible_sprites = YSortGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.all_sprites = AllSprites()

        # level info
        self.name = "mountain"

        # map setup
        self.create_map()

    def create_map(self) -> None:
        # import level graphics
        match self.name:
            case "mountain":
                layouts = import_layouts(
                    "mountain", ["constraints", "teleports", "magic_trees"]
                )
            case "cave":
                layouts = import_layouts("cave", ["constraints", "teleports"])

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
                            if val == "0":
                                # add self.visible_sprites group for debugging
                                path = (
                                        config.PROJECT_FOLDER
                                        + "/graphics/sprites/teleports/0_mountain/"
                                )
                                Tile(
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites, self.all_sprites],
                                    "constraints",
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
                                    [self.visible_sprites, self.obstacle_sprites, self.all_sprites],
                                    "teleport_" + sprite_type[int(val)],
                                    path,
                                )

                        case "magic_trees":
                            if val == "0":
                                path = (
                                        config.PROJECT_FOLDER
                                        + "/graphics/sprites/objects/magic_trees/0_magic_tree/"
                                )
                                MagicTree(
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites, self.all_sprites],
                                    "magic_tree",
                                    path,
                                )

        self.player = Player(
            config.PLAYER_POS, [self.visible_sprites, self.all_sprites], self.obstacle_sprites
        )

    def change_level(self):
        if config.CURRENT_LEVEL != self.name:
            self.name = config.CURRENT_LEVEL
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.create_map()

    def run(self) -> None:
        self.change_level()
        self.all_sprites.run()
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

        # creating temp surface with alpha channel to resize level
        self.temp_surface = pygame.surface.Surface(
            self.display_surf.get_size(), pygame.SRCALPHA
        )

    def set_floor(self, floor) -> None:
        # creating floor
        self.floor_surf = floor
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

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
            offset_pos = (sprite.rect.topleft - self.offset) * AllSprites.resize_coeff
            offset_pos.x -= self.half_width * AllSprites.resize_coeff - self.half_width
            offset_pos.y -= self.half_height * AllSprites.resize_coeff - self.half_height
            self.temp_surface.blit(sprite.image, offset_pos)

        display_size = self.display_surf.get_size()

        self.display_surf.blit(self.temp_surface, (0, 0))

        # debug
        self.clock.tick()
        debug(self.clock.get_fps())
        debug(f"Wood: {config.WOOD_AMOUNT}", 30)
        debug(f"Stone: {config.STONE_AMOUNT}", 50)
        debug(f"Interact: {HotKeys.is_pressed(HotKeys.interact)}", 70)


class AllSprites(pygame.sprite.Group):
    resize_step = 0.03
    max_resize_coeff = 2
    min_resize_coeff = 1
    resize_coeff = min_resize_coeff

    def __init__(self) -> None:
        super().__init__()
        self.sprites_entity = self.sprites().copy()

    def mouse_event_check(self) -> None:
        # check mouse events
        mousewheel_event = pygame.event.get(pygame.MOUSEBUTTONUP)

        if not mousewheel_event:
            return

        if mousewheel_event[0].button == 4:
            AllSprites.resize_coeff += AllSprites.resize_step

        elif mousewheel_event[0].button == 5:
            AllSprites.resize_coeff -= AllSprites.resize_step

        if AllSprites.resize_coeff > AllSprites.max_resize_coeff:
            AllSprites.resize_coeff = AllSprites.max_resize_coeff

        if AllSprites.resize_coeff < AllSprites.min_resize_coeff:
            AllSprites.resize_coeff = AllSprites.min_resize_coeff

        if mousewheel_event[0].button == 4 or mousewheel_event[0].button == 5:
            for sprite in self.sprites():

                if isinstance(sprite, Player):
                    for act in ["run", "idle"]:
                        for x_dir in ["right", "left"]:
                            for y_dir in ["forward", "back"]:
                                image_list = sprite.root_animation_images[act][x_dir][y_dir]
                                for i in range(len(sprite.animation_images[act][x_dir][y_dir])):
                                    root_image = image_list[i]
                                    sprite.animation_images[act][x_dir][y_dir][i] = pygame.transform.scale(root_image, (
                                        root_image.get_size()[0] * AllSprites.resize_coeff,
                                        root_image.get_size()[1] * AllSprites.resize_coeff))
                else:
                    sprite.image = pygame.transform.scale(sprite.root_image,
                                                          ((sprite.root_image.get_size()[0] * AllSprites.resize_coeff),
                                                           (sprite.root_image.get_size()[1] * AllSprites.resize_coeff)))

                    sprite.rect.width = sprite.root_image.get_size()[0] * AllSprites.resize_coeff
                    sprite.rect.height = sprite.root_image.get_size()[1] * AllSprites.resize_coeff

    def run(self) -> None:
        self.mouse_event_check()
