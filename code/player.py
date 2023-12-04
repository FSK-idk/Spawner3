import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        # general setup
        super().__init__(groups)
        self.image = pygame.image.load(
            "../graphics/test_tileset/tile_040.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -TILESIZE // 2)

        # movement
        self.diraction = pygame.math.Vector2()
        self.speed = 5

        # for collision
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.diraction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.diraction.x = 1
        else:
            self.diraction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.diraction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.diraction.y = 1
        else:
            self.diraction.y = 0

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
