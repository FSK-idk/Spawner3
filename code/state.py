from menu import *
from cutscene import *
from level import *


class State:
    def __init__(self, name, display) -> None:
        self.name = name
        self.display = display
        self.prev_state = None


class LevelState(State):
    def __init__(self, name, display) -> None:
        super().__init__(name, display)

    def enter_state(self, prev_state):
        self.level = Level(self.name, self.display)

    def exit_state(self):
        del self.level

    def update(self):
        pass

    def update_level(self, name):
        self.level.change_level(name)

    def run(self):
        if self.name != "gameplay":
            self.level.run()


class CutsceneState(State):
    def __init__(self, name, display) -> None:
        super().__init__(name, display)

    def enter_state(self, prev_state):
        self.cutscene = Cutscene(self.name, self.display)

    def exit_state(self):
        del self.cutscene

    def update(self):
        pass

    def run(self):
        self.cutscene.run()


class MenuState(State):
    def __init__(self, name, display) -> None:
        super().__init__(name, display)

    def enter_state(self, prev_state):
        if self.name == "main_menu":
            self.menu = MainMenu(self.name, self.display)
        elif self.name == "settings":
            self.menu = SettingsMenu(self.name, self.display, prev_state)
        elif self.name == "developers":
            self.menu = DevelopersMenu(self.name, self.display)
        elif self.name == "pause_menu":
            self.menu = PauseMenu(self.name, self.display)

    def exit_state(self):
        del self.menu

    def update(self):
        pass

    def run(self):
        self.menu.run()
