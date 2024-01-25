from core.state import *
from core.input_manager import InputManager
from data.save_data import save_data
from data.game_data import *


class GameStateManager:
    current_state = "main_menu"
    current_substate = ""

    def __init__(self, display: pygame.Surface) -> None:
        self.display = display

        self.substates = {
            "pause_menu": MenuState("pause_menu", self.display),
            "settings": MenuState("settings", self.display),
            "developers": MenuState("developers", self.display),
            "begin_cutscene": CutsceneState("begin", self.display),
            "end_cutscene": CutsceneState("end", self.display)
        }

        self.states = {
            "gameplay": LevelState("cats", self.display),
            "main_menu": MenuState("main_menu", self.display),
        }

        self.states[GameStateManager.current_state].enter_state()
        self.substate_stack = []

    def update_state(self) -> None:
        if event := InputManager.get_event(UPDATE_STATE):
            while GameStateManager.current_substate != "":
                self.substates[GameStateManager.current_substate].exit_state()
                GameStateManager.current_substate = self.substate_stack.pop()

            self.states[GameStateManager.current_state].exit_state()
            GameStateManager.current_state = event.state
            self.states[GameStateManager.current_state].enter_state()

            if GameStateManager.current_state == "gameplay" and save_data.is_show_begin_cutscene:
                self.substate_stack.append(GameStateManager.current_substate)
                GameStateManager.current_substate = "begin_cutscene"
                self.substates[GameStateManager.current_substate].enter_state()

    def update_substate(self) -> None:
        if event := InputManager.get_event(UPDATE_SUBSTATE):
            if event.substate == "exit_substate":
                self.substates[GameStateManager.current_substate].exit_state()
                GameStateManager.current_substate = self.substate_stack.pop()
                return

            if GameStateManager.current_substate == event.substate:
                return

            self.substate_stack.append(GameStateManager.current_substate)
            GameStateManager.current_substate = event.substate
            self.substates[GameStateManager.current_substate].enter_state()

    def update_gameplay_state(self) -> None:
        if event := InputManager.get_event(UPDATE_GAMEPLAY_STATE):
            save_data.current_level = event.state

    def update(self) -> None:
        self.update_substate()
        self.update_state()
        self.update_gameplay_state()

        if self.substate_stack:
            self.states[GameStateManager.current_state].draw()
            self.substates[GameStateManager.current_substate].run()
        else:
            self.states[GameStateManager.current_state].run()
