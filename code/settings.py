# game constants

import pygame
from utils import *


class Config:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    TILE_SIZE = 32
    PROJECT_FOLDER = get_parent_dir()

    CURRENT_LEVEL = "mountain"
    PLAYER_POS = (400, 250)

    WOOD_AMOUNT = 0
    STONE_AMOUNT = 0

    TEST_DATA = 12


class HotKeys:
    interact = [pygame.K_e]

    pause = [pygame.K_ESCAPE]

    go_right = [pygame.K_RIGHT, pygame.K_d]
    go_left = [pygame.K_LEFT, pygame.K_a]
    go_up = [pygame.K_UP, pygame.K_w]
    go_down = [pygame.K_DOWN, pygame.K_s]

    @staticmethod
    def is_pressed(codes: list[int]) -> bool:
        keys = pygame.key.get_pressed()
        return any(map(lambda key: keys[key], codes))


config = Config()
