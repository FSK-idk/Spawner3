import pygame

from utils import import_layouts
from ysort_group import YSortGroup
from zoom_group import ZoomGroup
from hud import HUD
from background import Background
from player import Player
from tile import *
from npc import NPC
from game_data import GameData
from save_data import save_data


class Level:
    def __init__(self, name: str, display: pygame.Surface) -> None:
        self.name = name
        self.display = display

        # groups
        self.visible_sprites = YSortGroup(self.display)
        self.obstacle_sprites = pygame.sprite.Group()
        self.zoom_group = ZoomGroup()
        self.hud_group = pygame.sprite.Group()

        HUD([self.hud_group], self.display)

        self.background = None

        self.create_map()

    def create_map(self) -> None:
        # import layout
        match self.name:
            case "mountain":
                layouts = import_layouts(
                    "mountain", ["constraints", "teleports",
                                 "magic_trees", "npcs", "trees",])
            case "cave":
                layouts = import_layouts(
                    "cave", ["constraints", "teleports",
                             "magic_rocks", "npcs", "rocks"])
            case "cats":
                layouts = import_layouts(
                    "cats", ["constraints", "teleports", "npcs"])

        GameData.is_update_background = True
        self.update_background()

        self.player = Player(
            [self.zoom_group,
             self.visible_sprites],
            save_data.player_position,
            self.obstacle_sprites)

        # create sprites
        for layer, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * GameData.tile_size
                    y = row_index * GameData.tile_size // 4
                    if row_index % 2 == 1:
                        x += GameData.tile_size // 2

                    match layer:
                        case "constraints":
                            if val != "-1":
                                if ((val == "4" and self.name == "mountain")
                                    or (val == "3" and self.name == "cave")
                                        or (val == "1" and self.name == "cats")):
                                    path = (
                                        GameData.project_folder
                                        + "/graphics/sprites/background/trees/0_tree/")
                                    StaticSprite(
                                        [self.zoom_group,
                                            self.obstacle_sprites],
                                        path,
                                        (x, y))

                                else:
                                    path = (
                                        GameData.project_folder
                                        + f"/graphics/sprites/background/")
                                    if self.name == "mountain":
                                        path += f"trees/{int(val)}_tree/"
                                    elif self.name == "cave":
                                        path += f"rocks/{int(val)}_rock/"
                                    else:
                                        path += "walls/0_wall/"

                                    StaticSprite(
                                        [self.zoom_group,
                                         self.visible_sprites,
                                         self.obstacle_sprites],
                                        path,
                                        (x, y))

                        case "trees":
                            if val != "-1":
                                path = (
                                    GameData.project_folder
                                    + f"/graphics/sprites/background/trees/{int(val)}_tree/")
                                StaticSprite(
                                    [self.zoom_group,
                                     self.visible_sprites],
                                    path,
                                    (x, y))

                        case "rocks":
                            if val != "-1":
                                path = (
                                    GameData.project_folder
                                    + f"/graphics/sprites/background/rocks/{int(val)}_rock/")
                                StaticSprite(
                                    [self.zoom_group,
                                     self.visible_sprites],
                                    path,
                                    (x, y))

                        case "teleports":
                            sprite_type = ["mountain", "cave", "cats"]
                            if val != "-1":
                                path = (
                                    GameData.project_folder
                                    + f"/graphics/sprites/teleports/{int(val)}_{sprite_type[int(val)]}/")
                                TeleportSprite(
                                    [self.zoom_group,
                                     self.obstacle_sprites],
                                    path,
                                    (x, y),
                                    sprite_type[int(val)],
                                    self.name)

                        case "magic_trees":
                            if val == "0":
                                path = (
                                    GameData.project_folder
                                    + "/graphics/sprites/objects/magic_trees/0_magic_tree/")
                                MagicTree(
                                    [self.zoom_group,
                                     self.visible_sprites,
                                     self.obstacle_sprites],
                                    path,
                                    (x, y))

                        case "magic_rocks":
                            if val == "0":
                                path = (
                                    GameData.project_folder
                                    + "/graphics/sprites/objects/magic_rocks/0_magic_rock/")
                                MagicRock(
                                    [self.zoom_group,
                                     self.visible_sprites,
                                     self.obstacle_sprites],
                                    path,
                                    (x, y))

                        case "npcs":
                            sprite_type = ["mesenev",
                                           "woodcutter",
                                           "miner",
                                           "laptop"]
                            if val != "-1":
                                path = (
                                    GameData.project_folder
                                    + f"/graphics/sprites/npcs/{int(val)}_{sprite_type[int(val)]}/")
                                NPC(
                                    [self.zoom_group,
                                     self.visible_sprites,
                                     self.obstacle_sprites],
                                    [self.zoom_group,
                                     self.visible_sprites],
                                    path,
                                    (x, y),
                                    sprite_type[int(val)])

        self.zoom_group.update_all_sprites()

    def update_background(self) -> None:
        if GameData.is_update_background:
            GameData.is_update_background = False
            if self.background:
                self.background.kill()
            if self.name != "cats":
                self.background = Background(
                    [self.zoom_group],
                    GameData.project_folder
                    + f"/graphics/background_images/{self.name}.png")
            else:
                self.background = Background(
                    [self.zoom_group],
                    GameData.project_folder
                    + f"/graphics/background_images/{save_data.cats_level}_{self.name}.png")

    def update_level(self) -> None:
        if self.name != save_data.current_level:
            self.name = save_data.current_level
            self.zoom_group.empty()
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.background.kill()
            self.create_map()

    def draw(self) -> None:
        self.update_level()

        self.zoom_group.run()
        self.zoom_group.update_list()

        self.update_background()

        self.visible_sprites.draw(self.player, self.background)
        self.visible_sprites.update()

        self.hud_group.draw(self.display)
        self.hud_group.update()
