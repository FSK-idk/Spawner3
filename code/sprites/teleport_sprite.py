import pygame

from sprites.basic_sprites import StaticSprite
from data.save_data import save_data
from data.game_data import UPDATE_GAMEPLAY_STATE


class TeleportSprite(StaticSprite):
    def __init__(self, groups: list, path: str,
                 pos: (int, int), type: str,
                 level_name: str) -> None:
        super().__init__(groups, path, pos)
        """
        Args:
            path: path to the tile folder
        """
        self.type = type
        self.level_name = level_name

    def teleport(self) -> None:
        match self.type:
            case "mountain":
                if self.level_name == "cave":
                    save_data.player_position = (400, 140)
                if self.level_name == "cats":
                    save_data.player_position = (520, 300)
            case "cave":
                save_data.player_position = (330, 530)
            case "cats":
                save_data.player_position = (500, 450)

        pygame.event.post(pygame.event.Event(
            UPDATE_GAMEPLAY_STATE,
            state=self.type,
            prev_state=self.level_name))
