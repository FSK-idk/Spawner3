import pygame
from settings import *
from menu import *
from game_state_manager import GameStateManager


class SoundManager:
    def __init__(self) -> None:
        self.start_menu_active = True
        self.name = "menu"
        self.volume = Menu.volume

        self.change_music()

    def change_music(self):
        pygame.mixer.music.load(config.PROJECT_FOLDER + f"/audio/{self.name}.mp3")
        pygame.mixer.music.set_volume(self.volume / 100.0)
        pygame.mixer.music.play(loops=-1)

    def update(self):
        if self.volume != SettingsMenu.volume:
            self.volume = SettingsMenu.volume
            pygame.mixer.music.set_volume(self.volume / 100.0)

        if self.name == "menu" and GameStateManager.current_state == "gameplay":
            self.name = GameStateManager.current_level
            self.change_music()
        elif self.name != "menu" and GameStateManager.current_state != "gameplay":
            self.name = "menu"
            self.change_music()
        elif self.name != "menu" and GameStateManager.current_state == "gameplay":
            if self.name != GameStateManager.current_level:
                self.name = GameStateManager.current_level
                self.change_music()
