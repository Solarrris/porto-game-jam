import pygame


class Loading:
    def __init__(self, screen):
        self.screen = screen
        self.width = 0

    def loadingScreen(self, time):
        while self.width < 1024:
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, 768))
            self.width += 1
