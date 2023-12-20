import math
import time

import pygame
from settings import config

from menu import Menu

pygame.font.init()


class TextCloud(pygame.sprite.Sprite):
    textFont = pygame.font.Font(
        config.PROJECT_FOLDER + "/graphics/font/LanaPixel.ttf", 11
    )
    x_margins = 3
    y_margins = 3
    char_time: float = 0.05
    kill_time: float = 1.5

    def __init__(self, text: str, groups, pos) -> None:
        super().__init__(groups)
        self.position = pos

        self.rendered_text = TextCloud.textFont.render(
            text, False, "black"
        ).convert_alpha()

        self.text_width = self.rendered_text.get_width()
        self.text_height = self.rendered_text.get_height()

        self.text = text

        self.start_time = time.time()

        self.image = pygame.Surface(
            (
                self.text_width + TextCloud.x_margins * 2,
                self.text_height + TextCloud.y_margins * 2,
            )
        )

        self.image.fill("white")
        # self.image = self.rendered_text

        self.root_image = self.image

        self.rect = self.image.get_rect(midbottom=(pos[0], pos[1]))

        # YSortGroup info
        self.ysort = self.rect

    def run(self) -> None:
        if (time.time() - self.start_time) > TextCloud.char_time * len(
            self.text
        ) + TextCloud.kill_time:
            self.kill()

        chars_now = (time.time() - self.start_time) // TextCloud.char_time

        chars_now = int(len(self.text) if chars_now > len(self.text) else chars_now)
        self.root_image.blit(
            TextCloud.render_text(self.text[:chars_now]),
            (TextCloud.x_margins, TextCloud.y_margins),
        )
        self.image = self.root_image

        config.QUEUE.append(self)

    @staticmethod
    def render_text(text: str) -> pygame.Surface:
        return TextCloud.textFont.render(text, False, "black")
