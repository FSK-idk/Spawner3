import pygame

from data.game_data import GameData


class TextCloud(pygame.sprite.Sprite):
    x_margins = 3
    y_margins = 3
    char_time = 50
    kill_time = 1500

    def __init__(self, text: str, groups: list, pos: (int, int)) -> None:
        super().__init__(groups)
        self.text = text
        self.position = pos

        # text
        self.rendered_text = GameData.font_lana11.render(
            self.text, False, "black").convert_alpha()

        self.text_width = self.rendered_text.get_width()
        self.text_height = self.rendered_text.get_height()

        # image
        self.image = pygame.Surface((
            self.text_width + TextCloud.x_margins * 2,
            self.text_height + TextCloud.y_margins * 2))
        self.image.fill("white")
        self.root_image = self.image
        self.rect = self.image.get_rect(midbottom=self.position)

        # sort
        self.ysort = self.rect

        # time
        self.start_time = pygame.time.get_ticks()

    def run(self) -> None:
        if ((pygame.time.get_ticks() - self.start_time)
                > TextCloud.char_time * len(self.text) + TextCloud.kill_time):
            self.kill()

        chars_now = (pygame.time.get_ticks()
                     - self.start_time) // TextCloud.char_time
        chars_now = int(len(self.text) if chars_now > len(self.text)
                        else chars_now)

        self.root_image.blit(
            TextCloud.render_text(self.text[:chars_now]),
            (TextCloud.x_margins, TextCloud.y_margins))
        self.image = self.root_image

        GameData.update_list.append(self)

    @staticmethod
    def render_text(text: str) -> pygame.Surface:
        return GameData.font_lana11.render(text, False, "black")
