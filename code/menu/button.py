import pygame

from core.utils import import_surface, import_mask


class Button(pygame.sprite.Sprite):
    def __init__(self, groups: list, path: str,
                 pos: (int, int), name: str) -> None:
        super().__init__(groups)
        self.path = path
        self.position = pos
        self.name = name

        self.image = import_surface(self.path)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = import_mask(self.path)
