from level import *
from menu import *
from settings import *
from cutscene import *
from phrases import *
from settings import *


class GameStateManager:
    current_state = "main_menu"
    current_level = "cats"

    def __init__(self, display) -> None:
        self.display = display

        self.states = {
            "gameplay": LevelState("cats", self.display),
            "main_menu": MenuState("main_menu", self.display),
            "pause_menu": MenuState("pause_menu", self.display),
            "settings": MenuState("settings", self.display),
            "developers": MenuState("developers", self.display),
            "begin_cutscene": CutsceneState("begin", self.display),
            "end_cutscene": CutsceneState("end", self.display),
        }

        GameStateManager.current_state = "main_menu"

        self.prev_state = None
        self.states[GameStateManager.current_state].enter_state(self.prev_state)

        self.show_pause_menu = False
        self.show_gameplay = False
        self.show_cutscene = False  # save_data.show_cutscene
        self.queue = []

    def update(self):
        if event := HotKeys.get_event(UPDATE_STATE):
            if GameStateManager.current_state != event.state:
                self.prev_state = event.prev_state

                if self.show_pause_menu:
                    # go in depth
                    if self.queue[-1] == event.state:
                        if self.queue[-1] != "gameplay":
                            self.states[GameStateManager.current_state].exit_state()
                            GameStateManager.current_state = self.queue.pop()
                        elif self.queue[-1] == "gameplay":
                            GameStateManager.current_state = event.state
                            self.queue = []
                            self.show_pause_menu = False
                    # go out
                    else:
                        self.queue.append(GameStateManager.current_state)
                        GameStateManager.current_state = event.state
                        self.states[GameStateManager.current_state].enter_state(
                            self.prev_state
                        )

                else:
                    # pause menu
                    if event.state == "pause_menu":
                        self.show_pause_menu = True
                        self.queue.append(event.prev_state)

                    # check if cutscene
                    if (
                        event.prev_state == "main_menu"
                        and event.state == "gameplay"
                        and self.show_cutscene
                    ):
                        GameStateManager.current_state = "begin_cutscene"
                    else:
                        GameStateManager.current_state = event.state

                    if event.prev_state == "begin_cutscene":
                        self.show_cutscene = False

                    self.states[GameStateManager.current_state].enter_state(
                        self.prev_state
                    )

        # update level
        if event := HotKeys.get_event(UPDATE_GAMEPLAY_STATE):
            self.states[GameStateManager.current_state].update_level(event.state)
            GameStateManager.current_level = event.state

        if self.show_pause_menu:
            for state in self.queue:
                self.states[state].run()

        self.states[GameStateManager.current_state].run()


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
