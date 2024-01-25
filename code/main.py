import pygame

from sys import exit
from core.utils import import_surface
from core.save_manager import SaveManager
from core.game_state_manager import GameStateManager
from core.sound_manager import SoundManager
from core.input_manager import InputManager
from data.game_data import GameData, RESET_SAVE_DATA
from data.save_data import save_data


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.display = pygame.display.set_mode(
            (save_data.screen_width, save_data.screen_height))
        pygame.display.set_caption("Spawner3")

        pygame.display.set_icon(
            import_surface(GameData.project_folder +
                           "/graphics/gui/icons/icon256.png"))

        self.clock = pygame.time.Clock()

        self.save_manager = SaveManager()
        self.game_state_manager = GameStateManager(self.display)
        self.sound_manager = SoundManager()

    def run(self) -> None:
        while True:
            self.handle_events()
            self.game_state_manager.update()
            self.sound_manager.update()

            pygame.display.update()
            self.clock.tick(save_data.fps)

    def handle_events(self) -> None:
        InputManager.events = list(pygame.event.get().copy())

        if InputManager.get_event(RESET_SAVE_DATA):
            self.save_manager.reset()

        if InputManager.get_event(pygame.QUIT):
            self.save_manager.save()

            pygame.quit()
            exit()


if __name__ == "__main__":
    game = Game()
    game.run()
