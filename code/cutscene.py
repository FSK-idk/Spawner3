import pygame

from utils import *
from input_manager import InputManager
from game_data import *


class Cutscene:
    def __init__(self, name: str, display: pygame.Surface) -> None:
        self.name = name
        self.display_surface = display

        self.images = import_surfaces(
            GameData.project_folder + "/graphics/cut_scenes/intro")

        for i in range(0, len(self.images)):
            self.images[i] = pygame.transform.scale(
                self.images[i], self.display_surface.get_size())

        self.rect = self.images[0].get_rect()

        self.index = 0

        # cooldown
        self.cooldown = 1000
        self.start_time = 0
        self.is_action = False

    def action(self) -> None:
        self.index += 1

    def draw(self) -> None:
        self.display_surface.blit(self.images[self.index], self.rect)

        if InputManager.is_pressed(InputManager.contin):
            current_time = pygame.time.get_ticks()

            if not self.is_action:
                self.is_action = True
                self.start_time = pygame.time.get_ticks()

                self.action()

            if self.is_action and current_time - self.start_time >= self.cooldown:
                self.is_action = False

        if self.index == len(self.images):
            pygame.event.post(pygame.event.Event(
                UPDATE_STATE,
                state="gameplay",
                prev_state="begin_cutscene"))
