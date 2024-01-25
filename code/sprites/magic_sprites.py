from components.animation_component import AnimationComponent
from sprites.basic_sprites import InteractiveSprite
from data.save_data import save_data
from data.game_data import GameData


class MagicTree(InteractiveSprite, AnimationComponent):
    def __init__(self, groups: list,
                 path: str, pos: (int, int)) -> None:
        InteractiveSprite.__init__(self, groups, path, pos)
        AnimationComponent.__init__(self, self.folder)
        """
        Args:
            path: path to the tile folder
        """
        # info
        self.level = save_data.tree_level
        self.gain = GameData.wood_gain[self.level]

        self.level_up()

    def update_graphics(self) -> None:
        super().update_graphics()
        AnimationComponent.__init__(self, self.folder)

    def action(self) -> None:
        save_data.wood_amount += self.gain

    def level_up(self) -> None:
        self.level = save_data.tree_level
        self.gain = GameData.wood_gain[self.level]

        self.folder = (
            GameData.project_folder
            + f"/graphics/sprites/objects/magic_trees/{self.level}_magic_tree/")

        self.update_graphics()

    def update(self) -> None:
        if self.level != save_data.tree_level:
            self.level_up()
        self.animate()


class MagicRock(InteractiveSprite, AnimationComponent):
    def __init__(self, groups: list,
                 path: str, pos: (int, int)) -> None:
        InteractiveSprite.__init__(self, groups, path, pos)
        AnimationComponent.__init__(self, self.folder)
        """
        Args:
            path: path to the tile folder
        """
        # info
        self.level = save_data.rock_level
        self.gain = GameData.stone_gain[self.level]

        self.level_up()

    def update_graphics(self) -> None:
        super().update_graphics()
        AnimationComponent.__init__(self, self.folder)

    def level_up(self) -> None:
        self.level = save_data.rock_level
        self.gain = GameData.stone_gain[self.level]

        self.folder = (
            GameData.project_folder
            + f"/graphics/sprites/objects/magic_rocks/{self.level}_magic_rock/")

        self.update_graphics()

    def action(self) -> None:
        save_data.stone_amount += self.gain

    def update(self) -> None:
        if self.level != save_data.rock_level:
            self.level_up()
        self.animate()
