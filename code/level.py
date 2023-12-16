# level class where everything happens

import pygame
from background import *
from npc import *
from player import *
from settings import *
from tile import *
from utils import *
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
                    "mountain",
                    [
                        "constraints",
                        "teleports",
                        "magic_trees",
                        "npcs",
                        "trees",
                    ],
                )
            case "cave":
                layouts = import_layouts(
                    "cave", ["constraints", "teleports", "magic_rocks", "npcs", "rocks"]
                )

            case "cats":
                layouts = import_layouts("cats", ["constraints", "teleports", "npcs"])

        # set floor
        self.background = Background(
            [self.all_sprites],
            config.PROJECT_FOLDER + f"/graphics/background_images/{self.name}.png",
        )

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
                                    Tile(
                                        [self.all_sprites, self.obstacle_sprites],
                                        path,
                                        (x, y),
                                    )

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
                                        [
                                            self.all_sprites,
                                            self.visible_sprites,
                                            self.obstacle_sprites,
                                        ],
                                        path,
                                        (x, y),
                                    )

                        case "trees":
                            if val != "-1":
                                path = (
                                    config.PROJECT_FOLDER
                                    + f"/graphics/sprites/background/trees/{int(val)}_tree/"
                                )
                                Tile(
                                    [
                                        self.all_sprites,
                                        self.visible_sprites,
                                    ],
                                    path,
                                    (x, y),
                                )

                        case "rocks":
                            if val != "-1":
                                path = (
                                    config.PROJECT_FOLDER
                                    + f"/graphics/sprites/background/rocks/{int(val)}_rock/"
                                )
                                Tile(
                                    [
                                        self.all_sprites,
                                        self.visible_sprites,
                                    ],
                                    path,
                                    (x, y),
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
                                    [
                                        self.all_sprites,
                                        # self.visible_sprites,
                                        self.obstacle_sprites,
                                    ],
                                    path,
                                    (x, y),
                                    "teleport_" + sprite_type[int(val)],
                                )

                        case "magic_trees":
                            if val == "0":
                                path = (
                                    config.PROJECT_FOLDER
                                    + "/graphics/sprites/objects/magic_trees/0_magic_tree/"
                                )
                                MagicTree(
                                    [
                                        self.all_sprites,
                                        self.visible_sprites,
                                        self.obstacle_sprites,
                                    ],
                                    path,
                                    (x, y),
                                )
                        case "magic_rocks":
                            if val == "0":
                                path = (
                                    config.PROJECT_FOLDER
                                    + "/graphics/sprites/objects/magic_rocks/0_magic_rock/"
                                )
                                MagicRock(
                                    [
                                        self.all_sprites,
                                        self.visible_sprites,
                                        self.obstacle_sprites,
                                    ],
                                    path,
                                    (x, y),
                                )

                        case "npcs":
                            sprite_type = ["mesenev", "woodcutter", "miner"]
                            if val != "-1":
                                path = (
                                    config.PROJECT_FOLDER
                                    + f"/graphics/sprites/npcs/{int(val)}_{sprite_type[int(val)]}/"
                                )
                                NPC(
                                    [
                                        self.all_sprites,
                                        self.visible_sprites,
                                        self.obstacle_sprites,
                                    ],
                                    [self.all_sprites, self.visible_sprites],
                                    path,
                                    (x, y),
                                    sprite_type[int(val)],
                                )

        self.player = Player(
            config.PLAYER_POS,
            [self.all_sprites, self.visible_sprites],
            self.obstacle_sprites,
        )

        self.all_sprites.update_sprites()

    def change_level(self):
        if config.CURRENT_LEVEL != self.name:
            self.name = config.CURRENT_LEVEL
            self.all_sprites.empty()
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.create_map()

    def run(self) -> None:
        self.change_level()
        self.all_sprites.run()
        self.visible_sprites.custom_draw(self.player, self.background)
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

    def custom_draw(self, player, background) -> None:
        # get offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw floor
        offset_pos = (
            background.rect.topleft
            - self.offset
            - pygame.Vector2(config.TILE_SIZE // 2, 0.5 * config.TILE_SIZE)
        ) * AllSprites.resize_coeff

        offset_pos.x -= self.half_width * AllSprites.resize_coeff - self.half_width
        offset_pos.y -= self.half_height * AllSprites.resize_coeff - self.half_height

        self.display_surf.blit(background.image, offset_pos)

        # draw sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.ysort.bottom):
            offset_pos = (sprite.rect.topleft - self.offset) * AllSprites.resize_coeff

            offset_pos.x -= self.half_width * AllSprites.resize_coeff - self.half_width
            offset_pos.y -= (
                self.half_height * AllSprites.resize_coeff - self.half_height
            )

            self.display_surf.blit(sprite.image, offset_pos)

        # debug
        self.clock.tick()
        debug(self.clock.get_fps())
        debug(f"Wood: {config.WOOD_AMOUNT}", 30)
        debug(f"Stone: {config.STONE_AMOUNT}", 50)
        debug(f"Interact: {HotKeys.is_pressed(HotKeys.interact)}", 70)


class AllSprites(pygame.sprite.Group):
    resize_step = 0.2
    max_resize_coeff = 5
    min_resize_coeff = 3.2
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
            self.update_sprites()

    def update_sprites(self):
        for sprite in self.sprites():
            if isinstance(sprite, Player):
                for act in ["run", "idle"]:
                    for x_dir in ["right", "left"]:
                        for y_dir in ["forward", "back"]:
                            image_list = sprite.root_animation_images[act][x_dir][y_dir]
                            for i in range(
                                len(sprite.animation_images[act][x_dir][y_dir])
                            ):
                                root_image = image_list[i]
                                sprite.animation_images[act][x_dir][y_dir][
                                    i
                                ] = pygame.transform.scale(
                                    root_image,
                                    (
                                        root_image.get_size()[0]
                                        * AllSprites.resize_coeff,
                                        root_image.get_size()[1]
                                        * AllSprites.resize_coeff,
                                    ),
                                )
            else:
                sprite.image = pygame.transform.scale(
                    sprite.root_image,
                    (
                        (sprite.root_image.get_size()[0] * AllSprites.resize_coeff),
                        (sprite.root_image.get_size()[1] * AllSprites.resize_coeff),
                    ),
                )

                sprite.rect.width = (
                    sprite.root_image.get_size()[0] * AllSprites.resize_coeff
                )
                sprite.rect.height = (
                    sprite.root_image.get_size()[1] * AllSprites.resize_coeff
                )

    def run(self) -> None:
        self.mouse_event_check()
