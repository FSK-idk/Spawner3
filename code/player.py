# player class

import pygame
from menu import *
from npc import *
from settings import *
from tile import *
from utils import *
from collections import defaultdict


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.player_folder = config.PROJECT_FOLDER + "/graphics/sprites/player/"

        # graphics
        self.image = import_surface(
            self.player_folder + "animation/idle/right/forward/idle right forward 1.png"
        )
        self.root_image = self.image

        self.rect = self.image.get_rect(midbottom=pos)

        # YSortGroup info
        self.ysort = import_ysort(self.player_folder)
        self.ysort.midtop = self.rect.midtop

        # collision
        self.obstacle_sprites = obstacle_sprites
        self.mask = import_mask(self.player_folder, "mask")

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 3.425  # ! do not change. rounding

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
                        self.player_folder + "animation/" + f"{act}/{x_dir}/{y_dir}"
                    )
        self.root_animation_images = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )

        for act in ["run", "idle"]:
            for x_dir in ["right", "left"]:
                for y_dir in ["forward", "back"]:
                    self.root_animation_images[act][x_dir][y_dir] = import_surfaces(
                        self.player_folder + "animation/" + f"{act}/{x_dir}/{y_dir}"
                    )

    def input(self) -> None:
        self.change_direction()
        self.change_animation_state()

    def change_direction(self) -> None:
        if not Menu.pause_menu_active:
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
        self.frame_index += self.frame_rate / config.FPS
        if self.frame_index >= len(animations):
            self.frame_index = 0

        # set image
        self.image = animations[int(self.frame_index)]

    def move(self) -> None:
        # normalize vector by ellipse
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction.y /= 2  # isometry

        # change player position
        self.rect.x += self.direction.x * self.speed
        self.check_collision("general")
        self.check_collision("horizontal")
        self.rect.y += self.direction.y * self.speed
        self.check_collision("general")
        self.check_collision("vertical")
        self.ysort.midtop = self.rect.midtop

    def check_collision(self, type) -> None:
        if type == "general":
            for sprite in self.obstacle_sprites:
                if isinstance(sprite, TeleportTile) and pygame.sprite.collide_mask(
                    sprite, self
                ):
                    sprite.teleport()

                if isinstance(sprite, InteractiveTile) and HotKeys.is_pressed(
                    HotKeys.interact
                ):
                    # check collision with mask functions
                    xoffset = self.rect[0] - sprite.rect[0]
                    yoffset = self.rect[1] - sprite.rect[1]
                    if sprite.interact_mask.overlap(self.mask, (xoffset, yoffset)):
                        sprite.interact()

                if isinstance(sprite, NPC):
                    # check collision with mask functions
                    xoffset = self.rect[0] - sprite.rect[0]
                    yoffset = self.rect[1] - sprite.rect[1]
                    if sprite.interact_mask.overlap(self.mask, (xoffset, yoffset)):
                        sprite.show_bubble(True)
                        if HotKeys.is_pressed(HotKeys.interact):
                            sprite.interact()
                    else:
                        sprite.show_bubble(False)

        if type == "horizontal":
            for sprite in self.obstacle_sprites:
                if pygame.sprite.collide_mask(sprite, self):
                    if self.direction.x < 0:  # move left
                        self.rect.left -= self.direction.x * self.speed
                    if self.direction.x > 0:  # move right
                        self.rect.right -= self.direction.x * self.speed

        if type == "vertical":
            for sprite in self.obstacle_sprites:
                if pygame.sprite.collide_mask(sprite, self):
                    if self.direction.y < 0:  # move up
                        self.rect.top -= self.direction.y * self.speed
                    if self.direction.y > 0:  # move down
                        self.rect.bottom -= self.direction.y * self.speed

    def update(self) -> None:
        self.input()
        self.animate()
        self.move()
