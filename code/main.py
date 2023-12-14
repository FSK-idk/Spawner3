# game start

import pygame
import sys
import pickle
from settings import *
from level import *


class Game:
    def __init__(self) -> None:
        # general setup
        pygame.init()

        # load save
        try:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "rb") as f:
                conf: Config = pickle.load(f)
                config.CURRENT_LEVEL = conf.CURRENT_LEVEL
                config.PLAYER_POS = conf.PLAYER_POS
                config.WOOD_AMOUNT = 500  # conf.WOOD_AMOUNT
                config.STONE_AMOUNT = 500  # conf.STONE_AMOUNT
                config.TREE_LEVEL = 0  # conf.TREE_LEVEL
                config.ROCK_LEVEL = 0  # conf.ROCK_LEVEL
        except:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
                pickle.dump(config, f)

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        # pygame.mouse.set_visible(False)

        pygame.display.set_caption("Spawner3")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self) -> None:
        # game loop
        while True:
            if pygame.event.get(pygame.QUIT):
                # dump save
                with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
                    pickle.dump(config, f)

                pygame.quit()
                sys.exit()

            self.screen.fill("Light Blue")

            self.level.run()

            pygame.display.update()
            self.clock.tick(config.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
