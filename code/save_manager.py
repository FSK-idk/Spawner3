import pickle
from settings import *


class SaveManager:
    def __init__(self):
        self.load()

    def load(self):
        try:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "rb") as f:
                conf: Config = pickle.load(f)

                for attr in vars(conf).keys():
                    setattr(config, attr, getattr(conf, attr))

                    config.CURRENT_LEVEL = "cats"
                    config.PLAYER_POS = (500, 450)

                    config.WOOD_AMOUNT = 0
                    config.STONE_AMOUNT = 0

                    config.TREE_LEVEL = 0
                    config.ROCK_LEVEL = 0
                    config.CATS_LEVEL = 0

                    config.IS_BEGIN = True

        except:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
                pickle.dump(config, f)

    def save(self):
        with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
            pickle.dump(config, f)
