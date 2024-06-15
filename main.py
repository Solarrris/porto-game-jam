import pygame
import math

import constants
from objects.game import Game

pygame.init()

pygame.display.set_caption("Porto")

screen = pygame.display.set_mode((1024, 768))

# Start game
game = Game(screen)

# Game loop
while game.running:
    game.update(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

pygame.quit()
