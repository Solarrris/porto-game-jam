import pygame

import constants


class Player(pygame.sprite.Sprite):
    def __init__(self, game, coordinates, image=None):
        super().__init__()

        self.game = game
        self.coordinates = coordinates

        self.image = None

        if image is None:
            image = pygame.image.load("assets/sprites/player/player-right.png")

        self.update_image(image)

        self.player_dimensions = None
        self.last_key_pressed = None

        self.rect = self.image.get_rect()
        self.rect.center = (self.coordinates[0], self.coordinates[1])

        # Walk attributs
        self.walk_frame = 0
        self.animation_counter = 0
        self.walk_animation_speed = 4

        self.walk_right_images = [
            pygame.image.load(f"{constants.PLAYER_PATH}/player-walk-right-1.png"),
            pygame.image.load(f"{constants.PLAYER_PATH}/player-right.png"),
            pygame.image.load(f"{constants.PLAYER_PATH}/player-walk-right-2.png"),
            pygame.image.load(f"{constants.PLAYER_PATH}/player-right.png")
        ]

        self.walk_left_images = [
            pygame.image.load(f"{constants.PLAYER_PATH}/player-walk-left-1.png"),
            pygame.image.load(f"{constants.PLAYER_PATH}/player-left.png"),
            pygame.image.load(f"{constants.PLAYER_PATH}/player-walk-left-2.png"),
            pygame.image.load(f"{constants.PLAYER_PATH}/player-left.png")
        ]

    def update_image(self, image):
        width = image.get_rect()[2]
        height = image.get_rect()[3]

        self.player_dimensions = (width * 3, height * 3)
        self.image = pygame.transform.scale(image, self.player_dimensions)

    def get_walk_image(self):
        if self.animation_counter % self.walk_animation_speed == 0:
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_left_images)

        self.animation_counter += 1

        if self.last_key_pressed == "left":
            return self.walk_left_images[self.walk_frame]

        if self.last_key_pressed == "right":
            return self.walk_right_images[self.walk_frame]

        self.animation_counter = 1
        return self.image
