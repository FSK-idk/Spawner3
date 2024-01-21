import pygame

from collections import defaultdict
from utils import *
from npc import NPC
from tile import TeleportSprite, InteractiveSprite
import game_state_manager as gsm
from input_manager import InputManager
from game_data import *
from save_data import save_data


class Player(pygame.sprite.Sprite):
    def __init__(self, groups: list, pos: (int, int),
                 obstacle_sprites: pygame.sprite.Group) -> None:
        super().__init__(groups)
        self.folder = GameData.project_folder + "/graphics/sprites/player/"

        # image
        self.root_image = import_surface(
            self.folder + "animation/idle/right/forward/idle right forward 1.png")
        self.image = self.root_image
        self.rect = self.image.get_rect(midbottom=pos)

        # sort
        self.ysort = import_ysort(self.folder + "ysort.png")
        self.ysort.midtop = self.rect.midtop

        # collision
        self.obstacle_sprites = obstacle_sprites
        self.mask = import_mask(self.folder + "mask.png")

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 3.425

        # animation
        self.frame_rate = 6
        self.frame_index = 0

        self.animation_state = {
            "action": "idle",
            "x_direction": "right",
            "y_direction": "forward",
        }

        self.root_animation_images = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))
        self.animation_images = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list)))

        for act in ["run", "idle"]:
            for x_dir in ["right", "left"]:
                for y_dir in ["forward", "back"]:
                    self.root_animation_images[act][x_dir][y_dir] = import_surfaces(
                        self.folder + "animation/" +
                        f"{act}/{x_dir}/{y_dir}")

                    self.animation_images[act][x_dir][y_dir] = \
                        self.root_animation_images[act][x_dir][y_dir].copy()

    def change_direction(self) -> None:
        if gsm.GameStateManager.current_substate == "":
            if InputManager.is_pressed(InputManager.go_left):
                self.direction.x = -1
            elif InputManager.is_pressed(InputManager.go_right):
                self.direction.x = 1
            else:
                self.direction.x = 0

            if InputManager.is_pressed(InputManager.go_up):
                self.direction.y = -1
            elif InputManager.is_pressed(InputManager.go_down):
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

    def input(self) -> None:
        if InputManager.is_pressed(InputManager.pause):
            pygame.event.post(pygame.event.Event(
                UPDATE_SUBSTATE, substate="pause_menu"))

        self.change_direction()
        self.change_animation_state()

    def animate(self) -> None:
        act = self.animation_state["action"]
        x_dir = self.animation_state["x_direction"]
        y_dir = self.animation_state["y_direction"]
        animations = self.animation_images[act][x_dir][y_dir]

        # change frame index
        self.frame_index += self.frame_rate / save_data.fps
        if self.frame_index >= len(animations):
            self.frame_index = 0

        self.image = animations[int(self.frame_index)]

    def check_collision(self, type: str) -> None:
        if type == "general":
            for sprite in self.obstacle_sprites:
                if (isinstance(sprite, TeleportSprite)
                        and pygame.sprite.collide_mask(sprite, self)):
                    sprite.teleport()

                if (isinstance(sprite, InteractiveSprite)
                        and InputManager.is_pressed(InputManager.interact)):
                    xoffset = self.rect[0] - sprite.rect[0]
                    yoffset = self.rect[1] - sprite.rect[1]
                    if sprite.interact_mask.overlap(
                            self.mask, (xoffset, yoffset)):
                        sprite.interact()

                if isinstance(sprite, NPC):
                    xoffset = self.rect[0] - sprite.rect[0]
                    yoffset = self.rect[1] - sprite.rect[1]
                    if sprite.interact_mask.overlap(
                            self.mask, (xoffset, yoffset)):
                        sprite.collide(True)
                        if InputManager.is_pressed(InputManager.interact):
                            sprite.interact()
                    else:
                        sprite.collide(False)

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

    def move(self) -> None:
        # normalize vector by ellipse
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction.y /= 2  # isometry

        self.rect.x += self.direction.x * self.speed
        self.check_collision("general")
        self.check_collision("horizontal")

        self.rect.y += self.direction.y * self.speed
        self.check_collision("general")
        self.check_collision("vertical")

        self.ysort.midtop = self.rect.midtop

    def update(self) -> None:
        self.input()
        self.animate()
        self.move()
