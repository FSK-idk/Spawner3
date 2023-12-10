# game start

import pygame, sys, pickle
from settings import *
from level import *
from menu import *


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
                config.WOOD_AMOUNT = conf.WOOD_AMOUNT
                config.STONE_AMOUNT = conf.STONE_AMOUNT
        except:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
                pickle.dump(config, f)

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

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

            if Menu.start_menu_active:
                Menu.start_menu_active = Menu.start_menu(self.screen)
            else:
                self.screen.fill("Light Blue")

                self.level.run()
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    Config.FLAG = True
                if Config.FLAG:
                    Config.FLAG = Menu.show(self.screen)
                pygame.display.update()
                self.clock.tick(config.FPS)



if __name__ == "__main__":
    game = Game()
    game.run()

