import pygame

from menu.menu import *
from core.game_state_manager import GameStateManager
from data.game_data import GameData
from data.save_data import save_data


class SoundManager:
    def __init__(self) -> None:
        self.start_menu_active = True
        self.name = "menu"
        self.volume = SettingsMenu.volume

        self.change_music()

    def change_music(self) -> None:
        pygame.mixer.music.load(
            GameData.project_folder + f"/audio/{self.name}.mp3")
        pygame.mixer.music.set_volume(self.volume / 100.0)
        pygame.mixer.music.play(loops=-1)

    def update(self) -> None:
        if self.volume != SettingsMenu.volume:
            self.volume = SettingsMenu.volume
            pygame.mixer.music.set_volume(self.volume / 100.0)

        if (self.name == "menu"
                and GameStateManager.current_state == "gameplay"
                and GameStateManager.current_substate == ""):
            self.name = save_data.current_level
            self.change_music()
        elif (self.name != "menu"
              and (GameStateManager.current_state == "main_menu"
                   or GameStateManager.current_substate != "")):
            self.name = "menu"
            self.change_music()
        elif (self.name != "menu"
              and GameStateManager.current_state == "gameplay"
              and GameStateManager.current_substate == ""
              and self.name != save_data.current_level):
            self.name = save_data.current_level
            self.change_music()
