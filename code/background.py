# background image

import pygame
from utils import *


class Background(pygame.sprite.Sprite):
    def __init__(self, groups, path) -> None:
        super().__init__(groups)
        self.path = path
        self.position = (0, 0)

        # graphics
        self.surface = import_surface(path)
        self.root_image = self.surface
        self.image = self.root_image

        self.rect = self.image.get_rect(topleft=self.position)
