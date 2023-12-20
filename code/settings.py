# game constants

import pygame
from utils import *


class Config:
    FLAG = False
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    TILE_SIZE = 32
    PROJECT_FOLDER = get_parent_dir()

    CURRENT_LEVEL = "cats"
    PLAYER_POS = (500, 450)

    WOOD_AMOUNT = 0
    STONE_AMOUNT = 0

    TREE_LEVEL = 0
    ROCK_LEVEL = 0
    CATS_LEVEL = 0

    IS_UPDATE = 0
    UPDATE_BG = 0

    IS_BEGIN = False

    QUEUE = []


class GameData:
    # wood - stone
    WOODCUTTER_UPGRADE = [(20, 0), (500, 600), (900, 1000)]
    MINER_UPGRADE = [(10, 10), (600, 500), (1000, 900)]
    CATS_UPGRADE = [(200, 200), (800, 800), (1500, 1500)]

    WOOD_GAIN = [1, 20, 50, 100]
    STONE_GAIN = [1, 20, 50, 100]


class HotKeys:
    interact = [pygame.K_e]

    pause = [pygame.K_ESCAPE]
    contin = [pygame.K_SPACE]

    go_right = [pygame.K_RIGHT, pygame.K_d]
    go_left = [pygame.K_LEFT, pygame.K_a]
    go_up = [pygame.K_UP, pygame.K_w]
    go_down = [pygame.K_DOWN, pygame.K_s]

    @staticmethod
    def is_pressed(codes: list[int]) -> bool:
        keys = pygame.key.get_pressed()
        return any(map(lambda key: keys[key], codes))


config = Config()
