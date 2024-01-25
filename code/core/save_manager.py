import pickle

from data.game_data import GameData
from data.save_data import save_data


class SaveManager:
    def __init__(self):
        self.load()

    def load(self) -> None:
        try:
            with open(GameData.project_folder + "/save/data.save", "rb") as f:
                load_data = pickle.load(f)

                for attr in vars(load_data).keys():
                    setattr(save_data, attr, getattr(load_data, attr))

        except:
            with open(GameData.project_folder + "/save/data.save", "wb") as f:
                pickle.dump(save_data, f)

    def save(self) -> None:
        with open(GameData.project_folder + "/save/data.save", "wb") as f:
            pickle.dump(save_data, f)

    def reset(self) -> None:
        save_data.__init__()
