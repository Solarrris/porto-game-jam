import pygame

import constants
from objects.player.player import Player


class MenuPlayer(Player):
    def __init__(self, game, coordinates, ship=True):
        self.ship = ship
        self.speed = 200

        if ship:
            original_image = pygame.image.load("assets/sprites/player/ship.png")
            original_image = pygame.transform.rotate(original_image, 270)
        else:
            original_image = pygame.image.load("assets/sprites/player/player-front.png")

        super().__init__(game, coordinates, original_image)

        self.scale = None
        self.update_image(original_image)

        self.rect = self.image.get_rect()
        self.rect.center = (self.coordinates[0], self.coordinates[1])

    def update_image(self, image):
        if self.ship:
            self.scale = 2.5
        else:
            self.scale = 3

        width = image.get_rect()[2]
        height = image.get_rect()[3]

        self.player_dimensions = (width * self.scale, height * self.scale)
        self.image = pygame.transform.scale(image, self.player_dimensions)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        image = None

        if keys[pygame.K_LEFT]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed * dt
                self.last_key_pressed = "left"

            if not self.ship:
                image = super().get_walk_image()
            else:
                image = pygame.image.load("assets/sprites/player/ship.png")
                image = pygame.transform.rotate(image, 90)
        if keys[pygame.K_RIGHT]:
            if (self.rect.x + self.rect.width) < 1024:
                self.rect.x += self.speed * dt
                self.last_key_pressed = "right"

            if not self.ship:
                image = super().get_walk_image()
            else:
                image = pygame.image.load("assets/sprites/player/ship.png")
                image = pygame.transform.rotate(image, 270)

        if keys[pygame.K_UP]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed * dt
                self.last_key_pressed = "back"

            if not self.ship:
                image = pygame.image.load("assets/sprites/player/player-back.png")
            else:
                image = pygame.image.load("assets/sprites/player/ship.png")

        if keys[pygame.K_DOWN]:
            if (self.rect.y + self.rect.width) < 768:
                self.rect.y += self.speed * dt
                self.last_key_pressed = "front"

            if not self.ship:
                image = pygame.image.load("assets/sprites/player/player-front.png")
            else:
                image = pygame.image.load("assets/sprites/player/ship.png")
                image = pygame.transform.rotate(image, 180)

        if not image and self.last_key_pressed is not None and not self.ship:
            image = pygame.image.load(f"{constants.PLAYER_PATH}/player-{self.last_key_pressed}.png")

        if image:
            self.update_image(image)
