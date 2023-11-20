# game start

import pygame, sys
from settings import *
from level import *


class Game:
    def __init__(self):
        # general setup
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Spawner3")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        # game loop
        while True:
            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

            self.screen.fill("Black")

            self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
