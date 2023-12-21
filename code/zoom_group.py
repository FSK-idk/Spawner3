import pygame

from player import Player
from game_data import GameData
from input_manager import InputManager


class ZoomGroup(pygame.sprite.Group):
    resize_step = 0.2
    max_resize_coeff = 5
    min_resize_coeff = 3.3
    resize_coeff = min_resize_coeff

    def __init__(self) -> None:
        super().__init__()
        self.sprites_entity = self.sprites().copy()

    def mouse_event_check(self) -> None:
        mousewheel_event = InputManager.get_event(pygame.MOUSEBUTTONUP)

        if not mousewheel_event:
            return

        if mousewheel_event.button == 4:
            ZoomGroup.resize_coeff += ZoomGroup.resize_step
        elif mousewheel_event.button == 5:
            ZoomGroup.resize_coeff -= ZoomGroup.resize_step

        if ZoomGroup.resize_coeff > ZoomGroup.max_resize_coeff:
            ZoomGroup.resize_coeff = ZoomGroup.max_resize_coeff
        if ZoomGroup.resize_coeff < ZoomGroup.min_resize_coeff:
            ZoomGroup.resize_coeff = ZoomGroup.min_resize_coeff

        if mousewheel_event.button == 4 or mousewheel_event.button == 5:
            self.update_all_sprites()

    def update_all_sprites(self) -> None:
        for sprite in self.sprites():
            if isinstance(sprite, Player):
                for act in ["run", "idle"]:
                    for x_dir in ["right", "left"]:
                        for y_dir in ["forward", "back"]:
                            image_list = \
                                sprite.root_animation_images[act][x_dir][y_dir]
                            for i in range(
                                    len(sprite.animation_images[act][x_dir][y_dir])):
                                root_image = image_list[i]
                                sprite.animation_images[act][x_dir][y_dir][i] = \
                                    pygame.transform.scale(
                                    root_image, (
                                        root_image.get_size()[0]
                                        * ZoomGroup.resize_coeff,
                                        root_image.get_size()[1]
                                        * ZoomGroup.resize_coeff))
            else:
                sprite.image = pygame.transform.scale(sprite.root_image, (
                    (sprite.root_image.get_size()[0] * ZoomGroup.resize_coeff),
                    (sprite.root_image.get_size()[1] * ZoomGroup.resize_coeff)))

                sprite.rect.width = (
                    sprite.root_image.get_size()[0] * ZoomGroup.resize_coeff)
                sprite.rect.height = (
                    sprite.root_image.get_size()[1] * ZoomGroup.resize_coeff)

    def update_list(self) -> None:
        if GameData.is_update_all_sprites:
            GameData.is_update_all_sprites = False
            GameData.update_list = []
            self.update_all_sprites()

        for sprite in GameData.update_list:
            sprite.image = pygame.transform.scale(
                sprite.root_image, (
                    (sprite.root_image.get_size()[0] * ZoomGroup.resize_coeff),
                    (sprite.root_image.get_size()[1] * ZoomGroup.resize_coeff)))

            sprite.rect.width = (
                sprite.root_image.get_size()[0] * ZoomGroup.resize_coeff)
            sprite.rect.height = (
                sprite.root_image.get_size()[1] * ZoomGroup.resize_coeff)

        GameData.update_list = []

    def run(self) -> None:
        self.mouse_event_check()
