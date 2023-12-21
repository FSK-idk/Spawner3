from state import *
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
