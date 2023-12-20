import pickle
from settings import *


class SaveManager:
    def __init__(self):
        pass

    def load(self):
        try:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "rb") as f:
                conf: Config = pickle.load(f)

                for attr in vars(conf).keys():
                    setattr(config, attr, getattr(conf, attr))

        except:
            with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
                pickle.dump(config, f)

    def save(self):
        with open(config.PROJECT_FOLDER + "/data/config.txt", "wb") as f:
            pickle.dump(config, f)