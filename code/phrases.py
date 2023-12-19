import math
import time

import pygame
from settings import config

from menu import Menu

pygame.font.init()


class TextCloud:
    textFont = pygame.font.Font(config.PROJECT_FOLDER + '/graphics/font/Clarity.ttf', 14)
    x_margins = 3
    y_margins = 3
    char_time: float = .15

    def __init__(self, text: str, surface: pygame.Surface) -> None:
        rendered_text = TextCloud.textFont.render(text, 1, 'black')
        self.text_width = rendered_text.get_width()
        self.text_height = rendered_text.get_height()

        self.text = text

        self.start_time = time.time()

        self.surface = surface

    def run(self, bottom_center_pos: tuple[int, int]) -> None:

        chars_now = (time.time() - self.start_time) // TextCloud.char_time

        chars_now = int(len(self.text) if chars_now > len(self.text) else chars_now)

        pygame.draw.rect(self.surface, 'white', (
            bottom_center_pos[0] - self.text_width / 2 - TextCloud.x_margins,
            bottom_center_pos[1] - self.text_height - TextCloud.y_margins,
            self.text_width + TextCloud.x_margins * 2, self.text_height + TextCloud.y_margins * 2))

        self.surface.blit(TextCloud.render_text(self.text[:chars_now]),
                          (bottom_center_pos[0] - self.text_width / 2, bottom_center_pos[1] - self.text_height))

    @staticmethod
    def render_text(text: str) -> pygame.Surface:
        return TextCloud.textFont.render(text, 1, 'black')
