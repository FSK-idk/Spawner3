import pygame

from player import Player
from background import Background
from zoom_group import ZoomGroup
from game_data import GameData


class YSortGroup(pygame.sprite.Group):
    def __init__(self, display: pygame.Surface) -> None:
        super().__init__()
        self.display_surf = display
        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surf.get_size()[0] // 2
        self.half_height = self.display_surf.get_size()[1] // 2

    def draw(self, player: Player, background: Background) -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw floor
        offset_pos = (background.rect.topleft - self.offset
                      - pygame.Vector2(
                          GameData.tile_size // 2,
                          0.5 * GameData.tile_size))
        offset_pos *= ZoomGroup.resize_coeff
        offset_pos.x -= (self.half_width * ZoomGroup.resize_coeff
                         - self.half_width)
        offset_pos.y -= (self.half_height * ZoomGroup.resize_coeff
                         - self.half_height)

        self.display_surf.blit(background.image, offset_pos)

        # draw sprites
        for sprite in sorted(self.sprites(),
                             key=lambda sprite: sprite.ysort.bottom):
            offset_pos = (sprite.rect.topleft - self.offset) * \
                ZoomGroup.resize_coeff

            offset_pos.x -= (self.half_width * ZoomGroup.resize_coeff
                             - self.half_width)
            offset_pos.y -= (self.half_height * ZoomGroup.resize_coeff
                             - self.half_height)

            self.display_surf.blit(sprite.image, offset_pos)
