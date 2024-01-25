import pygame

from level.level import Level
from level.cutscene import Cutscene
from menu.menu import *


class State:
    def __init__(self, name: str, display: pygame.Surface) -> None:
        self.name = name
        self.display = display


class LevelState(State):
    def __init__(self, name, display) -> None:
        super().__init__(name, display)

    def enter_state(self) -> None:
        self.level = Level(self.name, self.display)

    def exit_state(self) -> None:
        del self.level

    def draw(self) -> None:
        self.level.draw()

    def run(self) -> None:
        self.draw()


class CutsceneState(State):
    def __init__(self, name: str, display: pygame.Surface) -> None:
        super().__init__(name, display)

    def enter_state(self) -> None:
        self.cutscene = Cutscene(self.name, self.display)

    def exit_state(self) -> None:
        del self.cutscene

    def draw(self) -> None:
        self.cutscene.draw()

    def run(self) -> None:
        self.draw()


class MenuState(State):
    def __init__(self, name: str, display: pygame.Surface) -> None:
        super().__init__(name, display)

    def enter_state(self) -> None:
        match self.name:
            case "main_menu":
                self.menu = MainMenu(self.name, self.display)
            case "settings":
                self.menu = SettingsMenu(self.name, self.display)
            case "developers":
                self.menu = DevelopersMenu(self.name, self.display)
            case "pause_menu":
                self.menu = PauseMenu(self.name, self.display)

    def exit_state(self) -> None:
        del self.menu

    def draw(self) -> None:
        self.menu.draw()

    def run(self) -> None:
        self.draw()
        self.menu.update()
