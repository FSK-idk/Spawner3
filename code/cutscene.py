import pygame
from settings import *
from utils import *


class CutScene:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.images = import_surfaces(
            config.PROJECT_FOLDER + "/graphics/cut_scenes/intro"
        )

        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.scale(
                self.images[i], self.display_surface.get_size()
            )

        self.rect = self.images[0].get_rect()

        self.index = 0

        # cooldown
        self.cooldown = 1000
        self.contin_time = 0
        self.contining = False

    def run(self):
        self.display_surface.blit(self.images[self.index], self.rect)

        if HotKeys.is_pressed(HotKeys.contin):
            # check cooldown
            current_time = pygame.time.get_ticks()

            if not self.contining:
                self.contining = True
                self.contin_time = pygame.time.get_ticks()
                self.index += 1

            if self.contining and current_time - self.contin_time >= self.cooldown:
                self.contining = False

        if self.index == len(self.images):
            config.IS_BEGIN = False

        pass
