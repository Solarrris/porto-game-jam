import pygame

import constants
from objects.player.player import Player
from objects.movingPlatform import MovingPlatform
from objects.underGravityBlock import UnderGravityBlock


class LevelPlayer(Player):
    def __init__(self, game, coordinates, tiles):
        self.gravity = 1
        self.is_inverted = False
        self.is_attracting = False

        self.last_attract = 0

        super().__init__(game, coordinates)

        self.tiles = tiles

        self.is_jumping = False
        self.on_ground = False

        self.velocity = pygame.math.Vector2(0, 0)

        # pour posséder ou non l'inversion
        self.catch_invert_object = False
        # pour posséder ou non l'attraction
        self.catch_attract_object = False

    def update(self, game, screen):
        keys = pygame.key.get_pressed()

        image = None

        # Check keys pressed
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            image = self.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            image = self.move_right()
        elif self.catch_invert_object and keys[pygame.K_e]:
            self.invert_gravity()
        elif self.catch_attract_object and keys[pygame.K_a] and self.last_attract > 10:
            self.last_attract = 0
            self.is_attracting = not self.is_attracting
        else:
            self.velocity.x = 0

        # Jump
        if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_z]:
            self.jump(game)

        self.horizontal_movement()
        self.collision_x()

        self.vertical_movement()
        self.collision_y()

        if image is None and self.last_key_pressed is not None and self.last_key_pressed != "up":
            image = pygame.image.load(f"{constants.PLAYER_PATH}/player-{self.last_key_pressed}.png")

        if image is not None:
            self.update_image(image)

        self.last_attract += 1

    def update_image(self, image):
        if self.is_inverted:
            image = pygame.transform.flip(image, False, True)

        super().update_image(image)

    def move_left(self):
        self.velocity.x = -5
        self.last_key_pressed = "left"

        return super().get_walk_image()

    def move_right(self):
        self.velocity.x = 5
        self.last_key_pressed = "right"

        return super().get_walk_image()

    def jump(self, game):
        self.last_key_pressed = "up"
        if self.on_ground:
            self.is_jumping = True
            game.jump_sound.play()
            
            if self.is_inverted:
                self.velocity.y += 18
            else:
                self.velocity.y -= 18

            self.on_ground = False

    def horizontal_movement(self):
        self.rect.x += self.velocity.x

    def vertical_movement(self):
        if self.is_inverted:
            self.velocity.y -= self.gravity
            self.rect.top += self.velocity.y
        else:
            self.velocity.y += self.gravity
            self.rect.bottom += self.velocity.y

    def die(self):
        self.is_inverted = False
        self.velocity.y = 0
        self.rect.x = 50
        self.rect.y = 300

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if isinstance(tile, UnderGravityBlock):
                    if self.is_attracting:
                        if self.rect.centerx < tile.rect.centerx:
                            tile.rect.centerx += 1
                        else:
                            tile.rect.centerx -= 1

                        if self.rect.centery < tile.rect.centery:
                            tile.rect.centery += 1
                        else:
                            tile.rect.centery -= 1

                    self.is_attracting = False

                hits.append(tile)

        return hits

    def collision_x(self):
        hits = self.get_hits(self.tiles)

        for tile in hits:
            isMovingPlatform = isinstance(tile, MovingPlatform)
            isVerticalPlatform = False

            if isMovingPlatform:
                if not tile.is_horizontal_platform:
                    isVerticalPlatform = True
            if not isVerticalPlatform:
                if self.velocity.x > 0:
                    self.rect.x = tile.rect.left - self.rect.width
                elif self.velocity.x < 0:
                    self.rect.x = tile.rect.right

    def collision_y(self):
        self.on_ground = False
        if self.is_inverted:
            self.rect.bottom -= 1
        else:
            self.rect.bottom += 1

        hits = self.get_hits(self.tiles)
        for tile in hits:
            if self.is_inverted:
                if self.velocity.y < 0:
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity.y = 0
                    self.rect.top = tile.rect.bottom
                elif self.velocity.y > 0:
                    self.velocity.y = 0
                    self.rect.bottom = tile.rect.top
            else:
                if self.velocity.y > 0:
                    self.on_ground = True
                    self.is_jumping = False
                    self.velocity.y = 0
                    self.rect.bottom = tile.rect.top
                elif self.velocity.y < 0:
                    self.velocity.y = 0
                    self.rect.top = tile.rect.bottom

    def invert_gravity(self):
        if (self.on_ground):
            self.is_inverted = not self.is_inverted
