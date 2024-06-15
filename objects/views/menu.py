import pygame
import math

from pygame import Surface, SurfaceType

import constants
from objects.views.settings import Settings


class Menu:
    def __init__(self, screen: Surface | SurfaceType):
        # Booleans
        self.in_settings = False

        # Settings
        self.settings = Settings(screen)

        # Background
        self.background = pygame.image.load(f'{constants.IMAGES_PATH}/main-title-background.png')

        # Game title
        self.title = pygame.image.load(f'{constants.IMAGES_PATH}/porto.png')
        self.title = pygame.transform.scale(self.title,
                                            (self.title.get_width() * 4, self.title.get_height() * 4))
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = math.ceil(screen.get_width() / 2)
        self.title_rect.centery = 200

        # Play button
        self.play_button = pygame.image.load(f'{constants.ICON_PATH}/play-button.png')
        self.play_button = pygame.transform.scale(self.play_button, (150, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.centerx = math.ceil(screen.get_width() / 2)
        self.play_button_rect.centery = math.ceil(screen.get_height() / 2)

        # Exit button
        self.exit_button = pygame.image.load(f'{constants.ICON_PATH}/exit-button.png')
        self.exit_button = pygame.transform.scale(self.exit_button, (50, 50))
        self.exit_button_rect = self.exit_button.get_rect()
        self.exit_button_rect.top = 25
        self.exit_button_rect.left = 25

        # Settings button
        self.settings_button = pygame.image.load(f'{constants.ICON_PATH}/settings_button.png')
        self.settings_button = pygame.transform.scale(self.settings_button, (65, 65))
        self.settings_button_rect = self.settings_button.get_rect()
        self.settings_button_rect.centerx = math.ceil(screen.get_width() / 2 + 125)
        self.settings_button_rect.centery = math.ceil(screen.get_height() / 2)

    def update(self, screen: Surface | SurfaceType, game):
        # Print content
        screen.blit(self.background, (0, 0))
        if self.in_settings:
            self.settings.update(screen, game, self)
        else:
            screen.blit(self.title, self.title_rect)
            screen.blit(self.play_button, self.play_button_rect)
            screen.blit(self.exit_button, self.exit_button_rect)
            screen.blit(self.settings_button, self.settings_button_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if click on play button
                    if self.play_button_rect.collidepoint(event.pos):
                        game.interface_sound.play()
                        if not game.started:
                            game.start()
                        else:
                            game.is_playing = True
                    elif self.exit_button_rect.collidepoint(event.pos):
                        game.interface_sound.play()
                        game.running = False
                    elif self.settings_button_rect.collidepoint(event.pos):
                        game.interface_sound.play()
                        self.in_settings = True
                elif event.type == pygame.KEYUP:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_RETURN]:
                        game.interface_sound.play()
                        game.start()
