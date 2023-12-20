import pygame
from settings import *
from menu import *


class SoundManager:
    def __init__(self) -> None:
        self.start_menu_active = True
        self.level_name = "mountain"
        self.volume = Menu.volume

        self.change_music()
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.volume / 100.0)

    def change_music(self):
        if Menu.start_menu_active:
            pygame.mixer.music.load(config.PROJECT_FOLDER + "/audio/menu.mp3")
        else:
            match config.CURRENT_LEVEL:
                case "mountain":
                    pygame.mixer.music.load(
                        config.PROJECT_FOLDER + "/audio/mountain.mp3"
                    )
                case "cave":
                    pygame.mixer.music.load(config.PROJECT_FOLDER + "/audio/cave.mp3")
                case "cats":
                    pygame.mixer.music.load(config.PROJECT_FOLDER + "/audio/cats.mp3")

        pygame.mixer.music.set_volume(self.volume / 100.0)
        pygame.mixer.music.play(loops=-1)

    def update(self):
        if self.volume != Menu.volume:
            self.volume = Menu.volume
            pygame.mixer.music.set_volume(self.volume / 100.0)

        if not self.start_menu_active and Menu.start_menu_active:
            self.start_menu_active = True
            self.change_music()

        if self.start_menu_active and not Menu.start_menu_active:
            self.start_menu_active = False
            self.change_music()

        if not self.start_menu_active and not Menu.start_menu_active:
            if self.level_name != config.CURRENT_LEVEL:
                self.level_name = config.CURRENT_LEVEL
                self.change_music()