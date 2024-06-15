import pygame
from pygame import Surface, SurfaceType

import constants


class Planet(pygame.sprite.Sprite):
    def __init__(self, game, coordinates, radius, name, description, level, locked):
        super().__init__()

        self.game = game

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.radius = radius
        self.name = name
        self.description = description
        self.level = level
        self.locked = locked

        self.original_image = pygame.image.load(f"assets/sprites/planets/Planet{level}.png")
        self.image = pygame.transform.scale(self.original_image, (self.radius * 2, self.radius * 2))

        self.lock_image = pygame.image.load(f"{constants.ICON_PATH}/lock.png")
        self.lock_image = pygame.transform.scale(self.lock_image, (self.radius * 29 / 36, self.radius))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.width = self.rect[0]
        self.height = self.rect[1]

        offset = 0.5

        self.hitbox = pygame.Rect(self.x - (self.radius * offset), self.y - (self.radius * offset),
                                  2 * (self.radius * offset), 2 * (self.radius * offset))

    def draw(self, screen: Surface | SurfaceType):
        screen.blit(self.image, self.rect)

        if self.locked:
            screen.blit(self.lock_image,
                        (self.x - self.lock_image.get_width() // 2, self.y - self.lock_image.get_height() // 2))

    def add_bubble(self, bubble):
        self.bubble = bubble
