import pygame

from objects.tile import Tile


class Sign(Tile):
    def __init__(self, coordinates, surface, text, player, camera):
        super().__init__(coordinates, surface)

        self.text = text
        self.display_text = False
        self.player = player
        self.camera = camera

        text_font = pygame.font.Font("./assets/fonts/main-font.ttf", 24)

        self.title_surface = text_font.render(self.text, True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.centerx = self.rect.centerx
        self.title_rect.centery = self.rect.top - 30 - self.title_rect.height

    def update(self, game, screen):
        if self.display_text:
            screen.blit(self.title_surface, (self.title_rect.x - self.camera.x, self.title_rect.y - self.camera.y))
        
        if self.player.rect.colliderect(self.rect):
            self.display_text = True
        else:
            self.display_text = False
