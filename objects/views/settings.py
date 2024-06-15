import pygame

from pygame import SurfaceType, Surface

import constants
from objects.views.credits import Credits


class Settings:
    def __init__(self, screen: Surface | SurfaceType):
        # Booleans
        self.is_credit = False

        # Credits
        self.credits = Credits()

        # Import fonts
        texts_font = pygame.font.Font(f"{constants.FONTS_PATH}/main-font-bold.ttf", 50)

        # Texts
        self.music_title = texts_font.render("Musique", True, (230, 230, 230))
        self.music_title_rect = self.music_title.get_rect()
        self.music_title_rect.centerx = screen.get_width() // 3
        self.music_title_rect.centery = screen.get_width() // 2 - 190
        self.sounds_title = texts_font.render("Sons", True, (230, 230, 230))
        self.sounds_title_rect = self.music_title.get_rect()
        self.sounds_title_rect.centerx = screen.get_width() // 3 * 2 + self.sounds_title.get_width() / 3
        self.sounds_title_rect.centery = screen.get_width() // 2 - 190

        # Music switch button
        self.switch_music_button = pygame.image.load(f'{constants.ICON_PATH}/on-button.png')
        self.switch_music_button = pygame.transform.scale(self.switch_music_button, (72, 40))
        self.switch_music_button_rect = self.switch_music_button.get_rect()
        self.switch_music_button_rect.centerx = screen.get_width() // 3
        self.switch_music_button_rect.centery = screen.get_height() // 2

        # Sounds switch button
        self.switch_sounds_button = pygame.image.load(f'{constants.ICON_PATH}/on-button.png')
        self.switch_sounds_button = pygame.transform.scale(self.switch_sounds_button, (72, 40))
        self.switch_sounds_button_rect = self.switch_sounds_button.get_rect()
        self.switch_sounds_button_rect.centerx = screen.get_width() // 3 * 2
        self.switch_sounds_button_rect.centery = screen.get_height() // 2

        # Credits button
        self.credits_button = texts_font.render("Crédits", True, (230, 230, 230))
        self.credits_button_rect = self.credits_button.get_rect()
        self.credits_button_rect.centerx = screen.get_width() // 2
        self.credits_button_rect.top = screen.get_height() - 75

        # Return button
        self.return_button = pygame.image.load(f'{constants.ICON_PATH}/return-button.png')
        self.return_button = pygame.transform.scale(self.return_button, (50, 50))
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.top = 25
        self.return_button_rect.left = 25

    def update(self, screen: Surface | SurfaceType, game, menu):
        if self.is_credit:
            self.credits.update(screen, self)
        else:
            # Display static elements
            screen.blit(self.music_title, self.music_title_rect)
            screen.blit(self.sounds_title, self.sounds_title_rect)
            screen.blit(self.return_button, self.return_button_rect)
            screen.blit(self.credits_button, self.credits_button_rect)

            # Display buttons
            self.switch_music_button = pygame.transform.scale(self.switch_music_button, (72, 40))
            self.switch_sounds_button = pygame.transform.scale(self.switch_sounds_button, (72, 40))
            screen.blit(self.switch_music_button, self.switch_music_button_rect)
            screen.blit(self.switch_sounds_button, self.switch_sounds_button_rect)

            # Clic handler
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.switch_music_button_rect.collidepoint(event.pos):
                        if pygame.mixer.music.get_volume() == 0:
                            pygame.mixer.music.set_volume(constants.MUSIC_VOLUME)
                            self.switch_music_button = pygame.image.load(f'{constants.ICON_PATH}/on-button.png')
                        else:
                            pygame.mixer.music.set_volume(0)
                            self.switch_music_button = pygame.image.load(f'{constants.ICON_PATH}/off-button.png')

                    elif self.switch_sounds_button_rect.collidepoint(event.pos):
                        if game.interface_sound.get_volume() == 0:
                            game.set_sounds_volume(constants.SOUNDS_VOLUME)
                            self.switch_sounds_button = pygame.image.load(f'{constants.ICON_PATH}/on-button.png')
                        else:
                            game.set_sounds_volume(0)
                            self.switch_sounds_button = pygame.image.load(f'{constants.ICON_PATH}/off-button.png')

                    elif self.credits_button_rect.collidepoint(event.pos):
                        self.is_credit = True

                    elif self.return_button_rect.collidepoint(event.pos):
                        menu.in_settings = False
