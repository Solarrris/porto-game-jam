import pygame

import constants


class Credits:
    def __init__(self):
        # Import fonts
        self.main_font = pygame.font.Font(f"{constants.FONTS_PATH}/main-font.ttf", 30)
        self.main_font_bold = pygame.font.Font(f"{constants.FONTS_PATH}/main-font-bold.ttf", 40)

        # Texts
        self.texts = ["Développeurs", "BILLOT Samuel, MEREL Paul, COURAULT Robin, JACQUET Léo", "Game designer",
                      "COURAULT Robin", "Game artist", "MEREL Paul", "Musiques", "JACQUET Léo", "Sources",
                      "AI Pixelart, Wallpaper Flare, Justin-R (images), Pixabay (sons), Itch.io"]

        # Return button
        self.return_button = pygame.image.load(f'{constants.ICON_PATH}/return-button.png')
        self.return_button = pygame.transform.scale(self.return_button, (50, 50))
        self.return_button_rect = self.return_button.get_rect()
        self.return_button_rect.top = 25
        self.return_button_rect.left = 25

    def update(self, screen, settings):
        # Display elements
        screen.blit(self.return_button, self.return_button_rect)

        total_height = (sum([self.main_font_bold.size(text)[1] for text in self.texts]) + 12 * len(self.texts)) - 15
        y = (screen.get_height() - total_height) // 2

        for index, text in enumerate(self.texts):
            if index % 2 == 0:
                font = self.main_font_bold
                bottom_space = 5
            else:
                font = self.main_font
                bottom_space = 20
            text_object = font.render(text, True, (230, 230, 230))
            text_rect = text_object.get_rect()
            x = (screen.get_width() - text_rect.width) // 2
            screen.blit(text_object, (x, y))
            y += text_rect.height + bottom_space

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.return_button_rect.collidepoint(event.pos):
                settings.is_credit = False
