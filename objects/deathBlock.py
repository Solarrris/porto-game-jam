import pygame
from objects.tile import Tile

class DeathBlock(Tile):
    def __init__(self, coordinates, surface, player):
        super().__init__(coordinates, surface)

        self.player = player

    def update(self, game, screen):
        if self.rect.colliderect(self.player.rect):
            self.player.die()
