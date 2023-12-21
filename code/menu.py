import pygame
import pygame_widgets
import webbrowser
from settings import *
from pygame_widgets.slider import Slider
from utils import *


class Button(pygame.sprite.Sprite):
    def __init__(self, groups, path, pos, name) -> None:
        super().__init__(groups)
        self.path = path
        self.position = pos
        self.name = name

        self.image = import_surface(self.path)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = import_mask_path(self.path)


class MainMenu:
    def __init__(self, name, display) -> None:
        self.name = name
        self.display = display

        self.sprite_group = pygame.sprite.Group()

        width, height = self.display.get_size()

        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/play.png",
            (width / 2, height / 2),
            "play",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/settings.png",
            (width / 2, height / 6 * 3.67),
            "settings",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/developers.png",
            (width / 2, height / 4 * 2.87),
            "developers",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3.3),
            "quit",
        )

    def run(self):
        self.display.fill("Yellow")

        text = GameData.font_lana100.render("Spawner3", False, "Black")
        text_rect = text.get_rect(
            center=(self.display.get_size()[0] / 2, self.display.get_size()[1] / 3)
        )
        self.display.blit(text, text_rect)

        self.sprite_group.draw(self.display)
        self.check_collision()

    def check_collision(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.sprite_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (
                sprite.rect.collidepoint(*pos)
                and sprite.mask.get_at(pos_in_mask)
                and HotKeys.get_event(pygame.MOUSEBUTTONDOWN)
            ):
                match sprite.name:
                    case "play":
                        pygame.event.post(
                            pygame.event.Event(
                                UPDATE_STATE, state="gameplay", prev_state="main_menu"
                            )
                        )
                    case "settings":
                        pygame.event.post(
                            pygame.event.Event(
                                UPDATE_STATE, state="settings", prev_state="main_menu"
                            )
                        )
                    case "developers":
                        pygame.event.post(
                            pygame.event.Event(
                                UPDATE_STATE, state="developers", prev_state="main_menu"
                            )
                        )
                    case "quit":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))


class SettingsMenu:
    volume = 100

    def __init__(self, name, display, prev_state) -> None:
        self.name = name
        self.display = display
        self.prev_state = prev_state

        self.sprite_group = pygame.sprite.Group()

        width, height = self.display.get_size()

        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3.3),
            "quit",
        )

        self.slider = Slider(
            self.display,
            width // 2 - 200,
            height // 2,
            400,
            20,
            min=0,
            max=100,
            step=1,
        )
        self.slider.value = SettingsMenu.volume

    def run(self):
        SettingsMenu.volume = self.slider.getValue()

        self.display.fill("Yellow")

        text = GameData.font_lana50.render("Звук", False, "Black")
        text_rect = text.get_rect(
            center=(self.display.get_size()[0] / 2, self.display.get_size()[1] / 3)
        )
        self.display.blit(text, text_rect)

        volume_level = GameData.font_lana50.render(
            f"{SettingsMenu.volume}%", False, "Black"
        )
        self.display.blit(
            volume_level,
            (self.display.get_size()[0] / 2.13, self.display.get_size()[1] / 2.5),
        )

        pygame_widgets.update(HotKeys.events)

        self.sprite_group.draw(self.display)
        self.check_collision()

    def check_collision(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.sprite_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (
                sprite.rect.collidepoint(pos)
                and sprite.mask.get_at(pos_in_mask)
                and HotKeys.get_event(pygame.MOUSEBUTTONDOWN)
            ):
                match sprite.name:
                    case "quit":
                        if self.prev_state == "main_menu":
                            pygame.event.post(
                                pygame.event.Event(
                                    UPDATE_STATE,
                                    state="main_menu",
                                    prev_state="settings",
                                )
                            )
                        elif self.prev_state == "pause_menu":
                            pygame.event.post(
                                pygame.event.Event(
                                    UPDATE_STATE,
                                    state="pause_menu",
                                    prev_state="settings",
                                )
                            )


class DevelopersMenu:
    def __init__(self, name, display) -> None:
        self.name = name
        self.display = display

        self.sprite_group = pygame.sprite.Group()

        width, height = self.display.get_size()

        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/profile/profile1.png",
            (width * 2 / 10, height * 7 / 17),
            "profile1",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/profile/profile2.png",
            (width * 4 / 10, height * 7 / 17),
            "profile2",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/profile/profile3.png",
            (width * 6 / 10, height * 7 / 17),
            "profile3",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/profile/profile4.png",
            (width * 8 / 10, height * 7 / 17),
            "profile4",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3.3),
            "quit",
        )

    def run(self):
        self.display.fill("Yellow")

        text = GameData.font_lana50.render("Разработчики", False, "Black")
        text_rect = text.get_rect(
            center=(self.display.get_size()[0] / 2, self.display.get_size()[1] / 8)
        )
        self.display.blit(text, text_rect)

        name_text1 = GameData.font_lana30.render("Симанков Александр", False, "Black")
        name_text1_rect = name_text1.get_rect(
            center=(
                self.display.get_size()[0] * 2 / 10,
                self.display.get_size()[1] * 11 / 17,
            )
        )
        name_text2 = GameData.font_lana30.render("Рыбкин Владимир", False, "Black")
        name_text2_rect = name_text2.get_rect(
            center=(
                self.display.get_size()[0] * 4 / 10,
                self.display.get_size()[1] * 11 / 17,
            )
        )
        name_text3 = GameData.font_lana30.render("Верхов Владимир", False, "Black")
        name_text3_rect = name_text3.get_rect(
            center=(
                self.display.get_size()[0] * 6 / 10,
                self.display.get_size()[1] * 11 / 17,
            )
        )
        name_text4 = GameData.font_lana30.render("Можаров Дмитрий", False, "Black")
        name_text4_rect = name_text4.get_rect(
            center=(
                self.display.get_size()[0] * 8 / 10,
                self.display.get_size()[1] * 11 / 17,
            )
        )

        self.display.blit(name_text1, name_text1_rect)
        self.display.blit(name_text2, name_text2_rect)
        self.display.blit(name_text3, name_text3_rect)
        self.display.blit(name_text4, name_text4_rect)

        self.sprite_group.draw(self.display)
        self.check_collision()

    def check_collision(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.sprite_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (
                sprite.rect.collidepoint(*pos)
                and sprite.mask.get_at(pos_in_mask)
                and HotKeys.get_event(pygame.MOUSEBUTTONDOWN)
            ):
                match sprite.name:
                    case "profile1":
                        webbrowser.open_new("https://github.com/Fotlex")
                    case "profile2":
                        webbrowser.open_new("https://github.com/FSK-idk")
                    case "profile3":
                        webbrowser.open_new("https://github.com/verhovv")
                    case "profile4":
                        webbrowser.open_new("https://github.com/dmitry416")
                    case "quit":
                        pygame.event.post(
                            pygame.event.Event(UPDATE_STATE, state="main_menu")
                        )


class PauseMenu:
    def __init__(self, name, display) -> None:
        self.name = name
        self.display = display

        self.sprite_group = pygame.sprite.Group()

        width, height = self.display.get_size()

        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/play.png",
            (width / 2, height / 2),
            "continue",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/settings.png",
            (width / 2, height / 6 * 3.75),
            "settings",
        )
        Button(
            [self.sprite_group],
            config.PROJECT_FOLDER + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3),
            "quit",
        )

    def run(self):
        shadow = pygame.surface.Surface(self.display.get_size())
        shadow.fill("Black")
        shadow.set_alpha(200)

        self.display.blit(shadow, shadow.get_rect())

        self.sprite_group.draw(self.display)
        self.check_collision()

    def check_collision(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.sprite_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (
                sprite.rect.collidepoint(*pos)
                and sprite.mask.get_at(pos_in_mask)
                and HotKeys.get_event(pygame.MOUSEBUTTONDOWN)
            ):
                match sprite.name:
                    case "continue":
                        pygame.event.post(
                            pygame.event.Event(
                                UPDATE_STATE, state="gameplay", prev_state="pause_menu"
                            )
                        )
                    case "settings":
                        pygame.event.post(
                            pygame.event.Event(
                                UPDATE_STATE, state="settings", prev_state="pause_menu"
                            )
                        )
                    case "quit":
                        pygame.event.post(
                            pygame.event.Event(
                                UPDATE_STATE, state="main_menu", prev_state="pause_menu"
                            )
                        )
