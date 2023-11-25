import pygame
from settings import *
from support import *

from collections import defaultdict

anim_path = get_parent_dir() + '/graphics/sprites/player/'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        # general setup
        super().__init__(groups)
        self.image = pygame.image.load(
            get_parent_dir() + "/graphics/sprites/player/forward/right/idle/idle 1.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -Config.TILE_SIZE // 2)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5

        # for collision
        self.obstacle_sprites = obstacle_sprites

        # for animation
        self.animations_per_second = 2
        self.frame = 0

        self.anim_state = {
            'forward_back': 'forward',
            'run_idle': 'idle',
            'right_left': 'right'
        }

        self.animation_images = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for f in ['forward', 'back']:
            for r in ['right', 'left']:
                for i in ['run', 'idle']:
                    self.animation_images[f][r][i] = import_surfaces(
                        get_parent_dir() + f"/graphics/sprites/player/{f}/{r}/{i}")

    def input(self):
        self.frame = (self.frame + 1) % (Config.FPS // self.animations_per_second)

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

        self.change_animation_state()
        self.image = self.get_animation_image()

    def get_animation_image(self) -> pygame.Surface:
        return self.animation_images[self.anim_state['forward_back']][self.anim_state['right_left']][
            self.anim_state['run_idle']][
            self.frame < Config.FPS // self.animations_per_second // 2]

    def change_animation_state(self) -> None:
        if self.direction.x > 0:
            self.anim_state['right_left'] = 'right'
        elif self.direction.x < 0:
            self.anim_state['right_left'] = 'left'

        if self.direction.y > 0:
            self.anim_state['forward_back'] = 'forward'
        elif self.direction.y < 0:
            self.anim_state['forward_back'] = 'back'

        if self.direction.x or self.direction.y:
            self.anim_state['run_idle'] = 'run'
        else:
            self.anim_state['run_idle'] = 'idle'

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction.y /= 2

        self.hitbox.x += self.direction.x * self.speed
        self.check_collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        self.check_collision("vertical")
        self.rect.center = self.hitbox.center

    def check_collision(self, diraction):
        # moves the player back
        if diraction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x < 0:  # move left
                        self.hitbox.left = sprite.hitbox.right
                    if self.direction.x > 0:  # move right
                        self.hitbox.right = sprite.rect.left

        if diraction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:  # move up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:  # move down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        self.input()
        self.move()
