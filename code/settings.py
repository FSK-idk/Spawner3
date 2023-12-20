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

    CURRENT_LEVEL = "mountain"
    PLAYER_POS = (400, 250)

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
    WOODCUTTER_UPGRADE = [(20, 0), (50, 100), (400, 800)]
    MINER_UPGRADE = [(20, 0), (50, 100), (400, 800)]
    CATS_UPGRADE = [(20, 0), (50, 100), (400, 800)]


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
