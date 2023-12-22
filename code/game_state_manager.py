from state import *
from input_manager import InputManager
from save_data import save_data


class GameStateManager:
    current_state = "main_menu"

    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.states = {
            "gameplay": LevelState("cats", self.display),
            "main_menu": MenuState("main_menu", self.display),
            "pause_menu": MenuState("pause_menu", self.display),
            "settings": MenuState("settings", self.display),
            "developers": MenuState("developers", self.display),
            "begin_cutscene": CutsceneState("begin", self.display),
            "end_cutscene": CutsceneState("end", self.display)
        }

        self.prev_state = None
        self.states[GameStateManager.current_state].enter_state(
            self.prev_state)

        self.is_show_pause_menu = False
        self.pause_stack = []

    def update_state(self) -> None:
        if event := InputManager.get_event(UPDATE_STATE):
            if GameStateManager.current_state != event.state:
                self.prev_state = event.prev_state

                if self.is_show_pause_menu:
                    # go out
                    if self.prev_state == "pause_menu" and event.state == "main_menu":
                        for state in self.pause_stack:
                            self.states[state].exit_state()
                        self.pause_stack = []
                        GameStateManager.current_state = event.state
                        self.states[GameStateManager.current_state].enter_state(
                            self.prev_state)
                        self.is_show_pause_menu = False

                    elif self.pause_stack[-1] == event.state:
                        if self.pause_stack[-1] == "gameplay":
                            GameStateManager.current_state = event.state
                            self.pause_stack = []
                            self.is_show_pause_menu = False
                        elif self.pause_stack[-1] != "gameplay":
                            self.states[GameStateManager.current_state].exit_state()
                            GameStateManager.current_state = self.pause_stack.pop()
                    # go in
                    else:
                        self.pause_stack.append(GameStateManager.current_state)
                        GameStateManager.current_state = event.state
                        self.states[GameStateManager.current_state].enter_state(
                            self.prev_state)

                else:
                    if event.state == "pause_menu":
                        self.is_show_pause_menu = True
                        self.pause_stack.append(event.prev_state)

                    if event.prev_state == "begin_cutscene":
                        save_data.is_show_cutscene = False

                    # check if there is cutscene
                    if event.state == "gameplay" and save_data.is_show_cutscene:
                        GameStateManager.current_state = "begin_cutscene"
                    else:
                        GameStateManager.current_state = event.state

                    self.states[GameStateManager.current_state].enter_state(
                        self.prev_state)

    def update_gameplay_state(self) -> None:
        if event := InputManager.get_event(UPDATE_GAMEPLAY_STATE):
            save_data.current_level = event.state

    def update(self) -> None:
        self.update_state()
        self.update_gameplay_state()

        if self.is_show_pause_menu:
            for state in self.pause_stack:
                self.states[state].draw()

        self.states[GameStateManager.current_state].run()
