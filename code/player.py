import pygame
from settings import *
from support import *

anim_path = get_parent_dir() + '/graphics/sprites/player/'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        # general setup
        super().__init__(groups)
        self.image = pygame.image.load(
            get_parent_dir() + "/graphics/sprites/player/forward/right/idle/idle 1.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -TILESIZE // 2)

        # movement
        self.diraction = pygame.math.Vector2()
        self.speed = 5

        # for collision
        self.obstacle_sprites = obstacle_sprites

        # for animation
        self.animations_per_second = 2
        self.frame = 0
        self.forward_back = 'forward'
        self.run_idle = 'idle'
        self.right_left = 'right'

        self.animation_images = {
            "forward": {
                "left": {
                    "idle":
                        [
                            pygame.image.load(anim_path + 'forward/left/idle/idle 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'forward/left/idle/idle 2.png').convert_alpha()
                        ],
                    "run":
                        [
                            pygame.image.load(anim_path + 'forward/left/run/run 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'forward/left/run/run 2.png').convert_alpha()
                        ]
                },
                "right": {
                    "idle":
                        [
                            pygame.image.load(anim_path + 'forward/right/idle/idle 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'forward/right/idle/idle 2.png').convert_alpha()
                        ],
                    "run":
                        [
                            pygame.image.load(anim_path + 'forward/right/run/run 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'forward/right/run/run 2.png').convert_alpha()
                        ]
                }
            },
            "back": {
                "left": {
                    "idle":
                        [
                            pygame.image.load(anim_path + 'back/left/idle/idle 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'back/left/idle/idle 2.png').convert_alpha()
                        ],
                    "run":
                        [
                            pygame.image.load(anim_path + 'back/left/run/run 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'back/left/run/run 2.png').convert_alpha()
                        ]
                },
                "right": {
                    "idle":
                        [
                            pygame.image.load(anim_path + 'back/right/idle/idle 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'back/right/idle/idle 2.png').convert_alpha()
                        ],
                    "run":
                        [
                            pygame.image.load(anim_path + 'back/right/run/run 1.png').convert_alpha(),
                            pygame.image.load(anim_path + 'back/right/run/run 2.png').convert_alpha()
                        ]
                }
            }
        }

    def input(self):
        self.frame = (self.frame + 1) % (FPS // self.animations_per_second)

        keys = pygame.key.get_pressed()

        player_move = {
            'right': keys[pygame.K_RIGHT] or keys[pygame.K_d],
            'left': keys[pygame.K_LEFT] or keys[pygame.K_a],
            'up': keys[pygame.K_UP] or keys[pygame.K_w],
            'down': keys[pygame.K_DOWN] or keys[pygame.K_s]
        }

        if any(map(lambda x: player_move[x], ['left', 'right', 'up', 'down'])):
            self.run_idle = 'run'
        else:
            self.run_idle = 'idle'

        if player_move['left']:
            self.right_left = 'left'
            self.diraction.x = -1
        elif player_move['right']:
            self.right_left = 'right'
            self.diraction.x = 1
        else:
            self.diraction.x = 0

        if player_move['up']:
            self.forward_back = 'back'
            self.diraction.y = -1
        elif player_move['down']:
            self.forward_back = 'forward'
            self.diraction.y = 1
        else:
            self.diraction.y = 0

        self.image = self.animation_images[self.forward_back][self.right_left][self.run_idle][
            self.frame < FPS // self.animations_per_second // 2]

    def move(self):
        if self.diraction.magnitude() != 0:
            self.diraction = self.diraction.normalize()
            self.diraction.y /= 2

        self.hitbox.x += self.diraction.x * self.speed
        self.check_collision("horizontal")
        self.hitbox.y += self.diraction.y * self.speed
        self.check_collision("vertical")
        self.rect.center = self.hitbox.center

    def check_collision(self, diraction):
        # moves the player back
        if diraction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.diraction.x < 0:  # move left
                        self.hitbox.left = sprite.hitbox.right
                    if self.diraction.x > 0:  # move right
                        self.hitbox.right = sprite.rect.left

        if diraction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.diraction.y < 0:  # move up
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.diraction.y > 0:  # move down
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):
        self.input()
        self.move()
