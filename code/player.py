# player class

import pygame
from settings import *
from utils import *
from collections import defaultdict


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        # general setup
        super().__init__(groups)
        self.image = pygame.image.load(
            Config.PROJECT_FOLDER
            + "/graphics/sprites/player/idle/right/forward/idle right forward 1.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(
            -Config.TILE_SIZE // 1.5, -Config.TILE_SIZE // 1.5
        )

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 4

        # collision
        self.obstacle_sprites = obstacle_sprites

        # animation
        self.frame_rate = 6
        self.frame_index = 0

        self.animation_state = {
            "action": "idle",
            "x_direction": "right",
            "y_direction": "forward",
        }

        # action -> x direction -> y direction
        self.animation_images = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )

        for act in ["run", "idle"]:
            for x_dir in ["right", "left"]:
                for y_dir in ["forward", "back"]:
                    self.animation_images[act][x_dir][y_dir] = import_surfaces(
                        Config.PROJECT_FOLDER
                        + f"/graphics/sprites/player/{act}/{x_dir}/{y_dir}"
                    )

    def input(self) -> None:
        self.change_direction()
        self.change_animation_state()

    def change_direction(self) -> None:
        if HotKeys.is_pressed(HotKeys.go_left):
            self.direction.x = -1
        elif HotKeys.is_pressed(HotKeys.go_right):
            self.direction.x = 1
        else:
            self.direction.x = 0

        if HotKeys.is_pressed(HotKeys.go_up):
            self.direction.y = -1
        elif HotKeys.is_pressed(HotKeys.go_down):
            self.direction.y = 1
        else:
            self.direction.y = 0

    def change_animation_state(self) -> None:
        if self.direction.x or self.direction.y:
            self.animation_state["action"] = "run"
        else:
            self.animation_state["action"] = "idle"

        if self.direction.x > 0:
            self.animation_state["x_direction"] = "right"
        elif self.direction.x < 0:
            self.animation_state["x_direction"] = "left"

        if self.direction.y > 0:
            self.animation_state["y_direction"] = "forward"
        elif self.direction.y < 0:
            self.animation_state["y_direction"] = "back"

    def animate(self) -> None:
        # get list of animations
        act = self.animation_state["action"]
        x_dir = self.animation_state["x_direction"]
        y_dir = self.animation_state["y_direction"]

        animations = self.animation_images[act][x_dir][y_dir]

        # change frame index
        self.frame_index += self.frame_rate / Config.FPS
        if self.frame_index >= len(animations):
            self.frame_index = 0

        # set image
        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def move(self) -> None:
        # normalize vector by ellipse
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction.y /= 2

        # change player position
        self.hitbox.x += self.direction.x * self.speed
        self.check_collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.check_collision("vertical")
        self.rect.center = self.hitbox.center

    def check_collision(self, direction) -> None:
        # move player back
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x < 0:  # move left
                        self.hitbox.left = sprite.hitbox.right
                    if self.direction.x > 0:  # move right
                        self.hitbox.right = sprite.rect.left

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # move up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # move down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self) -> None:
        self.input()
        self.animate()
        self.move()
