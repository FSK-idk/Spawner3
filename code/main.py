# game start

import pygame
import sys
from settings import *
from level import *
from menu import *

class Game:
    def __init__(self):
        # general setup
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Spawner3")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        flag = False
        # game loop
        while True:
            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()

            self.screen.fill("Black")

            self.level.run()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                flag = True
            if flag:
                flag = Menu.show(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()

