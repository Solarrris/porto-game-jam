import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, coordinates, surface):
        super().__init__()

        self.image = surface
        self.rect = self.image.get_rect(topleft = coordinates)