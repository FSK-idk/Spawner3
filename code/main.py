# game start

import pygame
import sys

from level import *
from menu import *
from settings import *
from cutscene import *
from phrases import *
from save_manager import *
from sound_manager import *


class Game:
    def __init__(self) -> None:
        # general setup
        pygame.init()

        self.save_manager = SaveManager()
        self.sound_manager = SoundManager()

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

        pygame.display.set_caption("Spawner3")

        self.clock = pygame.time.Clock()

        self.level = Level()
        self.cutscene = CutScene()

    def run(self) -> None:
        # game loop
        while True:
            if pygame.event.get(pygame.QUIT):
                #  save
                self.save_manager.save()

                pygame.quit()
                sys.exit()

            if (
                Menu.start_menu_active
                and not Menu.settings_active
                and not Menu.developers_menu_active
            ):
                Menu.start_menu_active = Menu.start_menu(self.screen)
            elif Menu.settings_active:
                Menu.settings(self.screen)
            elif Menu.developers_menu_active:
                Menu.developers(self.screen)
            else:
                self.screen.fill("Light Blue")

                if config.IS_BEGIN:
                    self.cutscene.run()
                else:
                    self.level.run()

                if HotKeys.is_pressed(HotKeys.pause):
                    Menu.pause_menu_active = True
                if Menu.pause_menu_active:
                    Menu.pause_menu_active = Menu.pause_menu(self.screen)

                pygame.display.update()
                self.clock.tick(config.FPS)

            self.sound_manager.update()


if __name__ == "__main__":
    game = Game()
    game.run()
