# game start

import pygame
import sys

from game_state_manager import *
from save_manager import *
from sound_manager import *


class Game:
    def __init__(self) -> None:
        # general setup
        pygame.init()

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Spawner3")
        pygame.display.update()

        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager(self.screen)
        self.save_manager = SaveManager()
        self.sound_manager = SoundManager()

    def run(self) -> None:
        # game loop
        while True:
            self.handle_events()
            self.game_state_manager.update()
            self.sound_manager.update()
            pygame.display.update()
            self.clock.tick(config.FPS)

    def handle_events(self):
        HotKeys.events = list(pygame.event.get().copy())

        if HotKeys.get_event(pygame.QUIT):
            #  save
            self.save_manager.save()

            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
