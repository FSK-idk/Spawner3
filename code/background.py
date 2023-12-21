import pygame

from utils import import_surface


class Background(pygame.sprite.Sprite):
    def __init__(self, groups: list, path: str) -> None:
        """
        Args:
            path: path to the image with extension
        """
        super().__init__(groups)
        self.path = path
        self.position = (0, 0)

        self.surface = import_surface(path)
        self.root_image = self.surface
        self.image = self.root_image
        self.rect = self.image.get_rect(topleft=self.position)
