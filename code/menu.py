import pygame
import pygame_widgets
import webbrowser

from utils import import_surface
from button import Button
from pygame_widgets.slider import Slider
from input_manager import InputManager
from game_data import *


class Menu:
    def __init__(self, name: str, display: pygame.Surface) -> None:
        self.name = name
        self.display = display
        self.background_serf = import_surface(
            GameData.project_folder + "/graphics/background_images/menu.png")
        self.background_serf = pygame.transform.scale(
            self.background_serf, self.display.get_size())
        self.background_rect = self.background_serf.get_rect()


class MainMenu(Menu):
    def __init__(self, name: str, display: pygame.Surface) -> None:
        super().__init__(name, display)
        width, height = self.display.get_size()

        self.buttons_group = pygame.sprite.Group()

        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/play.png",
            (width / 2, height / 2),
            "play")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/settings.png",
            (width / 2, height / 6 * 3.67),
            "settings")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/developers.png",
            (width / 2, height / 4 * 2.87),
            "developers")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3.3),
            "quit")

    def draw_background(self) -> None:
        self.display.blit(self.background_serf, self.background_rect)

        text = GameData.font_lana150.render("Spawner3", False, "Black")
        text_rect = text.get_rect(
            center=(self.display.get_size()[0] / 2,
                    self.display.get_size()[1] / 3))

        self.display.blit(text, text_rect)

    def draw(self) -> None:
        self.draw_background()
        self.buttons_group.draw(self.display)

    def input(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.buttons_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y

            if (sprite.rect.collidepoint(*pos)
                and sprite.mask.get_at(pos_in_mask)
                    and InputManager.get_event(pygame.MOUSEBUTTONDOWN)):
                match sprite.name:
                    case "play":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_STATE, state="gameplay"))
                    case "settings":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_SUBSTATE, substate="settings"))
                    case "developers":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_SUBSTATE, substate="developers"))
                    case "quit":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self) -> None:
        self.input()


class SettingsMenu(Menu):
    volume = 100

    def __init__(self, name: str, display: pygame.Surface) -> None:
        super().__init__(name, display)
        width, height = self.display.get_size()

        self.buttons_group = pygame.sprite.Group()

        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3.3),
            "quit")

        self.slider = Slider(
            self.display,
            width // 2 - 200, height // 2,
            400, 20,
            min=0, max=100, step=1)
        self.slider.value = SettingsMenu.volume

    def draw_background(self) -> None:
        self.display.blit(self.background_serf, self.background_rect)

        text = GameData.font_lana50.render("Звук", False, "Black")
        text_rect = text.get_rect(
            center=(self.display.get_size()[0] / 2,
                    self.display.get_size()[1] / 3))

        self.display.blit(text, text_rect)

        volume_level = GameData.font_lana50.render(
            f"{SettingsMenu.volume}%", False, "Black")

        self.display.blit(volume_level,
                          (self.display.get_size()[0] / 2.13,
                           self.display.get_size()[1] / 2.5))

    def draw(self) -> None:
        self.draw_background()
        self.buttons_group.draw(self.display)

    def input(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.buttons_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (sprite.rect.collidepoint(pos)
                and sprite.mask.get_at(pos_in_mask)
                    and InputManager.get_event(pygame.MOUSEBUTTONDOWN)):
                match sprite.name:
                    case "quit":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_SUBSTATE, substate="exit_substate"))

    def update(self) -> None:
        SettingsMenu.volume = self.slider.getValue()
        pygame_widgets.update(InputManager.events)
        self.input()


class DevelopersMenu(Menu):
    def __init__(self, name: str, display: pygame.Surface) -> None:
        super().__init__(name, display)
        width, height = self.display.get_size()

        self.buttons_group = pygame.sprite.Group()

        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/profile/profile1.png",
            (width * 2 / 10, height * 7 / 17),
            "profile1")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/profile/profile2.png",
            (width * 4 / 10, height * 7 / 17),
            "profile2")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/profile/profile3.png",
            (width * 6 / 10, height * 7 / 17),
            "profile3")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/profile/profile4.png",
            (width * 8 / 10, height * 7 / 17),
            "profile4")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3.3),
            "quit")

    def draw_background(self) -> None:
        self.display.blit(self.background_serf, self.background_rect)

        text = GameData.font_lana50.render("Разработчики", False, "Black")
        text_rect = text.get_rect(
            center=(self.display.get_size()[0] / 2,
                    self.display.get_size()[1] / 8))

        self.display.blit(text, text_rect)

        name_text1 = GameData.font_lana30.render(
            "Симанков Александр", False, "Black")
        name_text1_rect = name_text1.get_rect(
            center=(
                self.display.get_size()[0] * 2 / 10,
                self.display.get_size()[1] * 11 / 17))
        name_text2 = GameData.font_lana30.render(
            "Рыбкин Владимир", False, "Black")
        name_text2_rect = name_text2.get_rect(
            center=(
                self.display.get_size()[0] * 4 / 10,
                self.display.get_size()[1] * 11 / 17))
        name_text3 = GameData.font_lana30.render(
            "Верхов Владимир", False, "Black")
        name_text3_rect = name_text3.get_rect(
            center=(
                self.display.get_size()[0] * 6 / 10,
                self.display.get_size()[1] * 11 / 17))
        name_text4 = GameData.font_lana30.render(
            "Можаров Дмитрий", False, "Black")
        name_text4_rect = name_text4.get_rect(
            center=(
                self.display.get_size()[0] * 8 / 10,
                self.display.get_size()[1] * 11 / 17))

        self.display.blit(name_text1, name_text1_rect)
        self.display.blit(name_text2, name_text2_rect)
        self.display.blit(name_text3, name_text3_rect)
        self.display.blit(name_text4, name_text4_rect)

    def draw(self) -> None:
        self.draw_background()
        self.buttons_group.draw(self.display)

    def input(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.buttons_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (sprite.rect.collidepoint(*pos)
                and sprite.mask.get_at(pos_in_mask)
                    and InputManager.get_event(pygame.MOUSEBUTTONDOWN)):
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
                        pygame.event.post(pygame.event.Event(
                            UPDATE_SUBSTATE, substate="exit_substate"))

    def update(self) -> None:
        self.input()


class PauseMenu(Menu):
    def __init__(self, name: str, display: pygame.Surface) -> None:
        super().__init__(name, display)

        self.buttons_group = pygame.sprite.Group()

        width, height = self.display.get_size()

        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/continue.png",
            (width / 2, height / 2),
            "continue")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/settings.png",
            (width / 2, height / 6 * 3.75),
            "settings")
        Button(
            [self.buttons_group],
            GameData.project_folder + "/graphics/gui/buttons/quit.png",
            (width / 2, height / 4 * 3),
            "quit")

        self.shadow_surf = pygame.Surface(self.display.get_size())
        self.shadow_surf.fill("Black")
        self.shadow_surf.set_alpha(200)
        self.shadow_rect = self.shadow_surf.get_rect()

    def draw_background(self) -> None:
        self.display.blit(self.shadow_surf, self.shadow_rect)

    def draw(self) -> None:
        self.draw_background()
        self.buttons_group.draw(self.display)

    def input(self) -> None:
        pos = pygame.mouse.get_pos()

        for sprite in self.buttons_group:
            pos_in_mask = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if (sprite.rect.collidepoint(*pos)
                and sprite.mask.get_at(pos_in_mask)
                    and InputManager.get_event(pygame.MOUSEBUTTONDOWN)):
                match sprite.name:
                    case "continue":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_SUBSTATE, substate="exit_substate"))
                    case "settings":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_SUBSTATE, substate="settings"))
                    case "quit":
                        pygame.event.post(pygame.event.Event(
                            UPDATE_STATE, state="main_menu"))

    def update(self) -> None:
        self.input()
