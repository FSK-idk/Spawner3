import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        # general setup
        super().__init__(groups)
        self.image = pygame.image.load(
            "./graphics/test_tileset/tile_040.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, -50)

        # movement
        self.diraction = pygame.math.Vector2()
        self.speed = 5

        # for collision (for the future)
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

        self.hitbox.x += self.diraction.x * self.speed
        self.hitbox.y += self.diraction.y * self.speed
        self.rect.center = self.hitbox.center

    def update(self):
        self.input()
        self.move()
