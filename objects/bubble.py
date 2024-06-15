import pygame


class Bubble(pygame.sprite.Sprite):
    def __init__(self, planet):
        super().__init__()

        self.planet = planet

        # Import fonts
        title_font = pygame.font.Font("./assets/fonts/main-font.ttf", 24)
        description_font = pygame.font.Font("./assets/fonts/main-font.ttf", 16)

        self.name = planet.name
        self.description = planet.description

        # Render the text onto the bubble's image
        title_surface = title_font.render(self.name, True, (230, 230, 230))
        description_surface = description_font.render(self.description, True, (230, 230, 230))

        title_rect = title_surface.get_rect()
        description_rect = description_surface.get_rect()

        key_image = pygame.image.load("./assets/sprites/images/Space-Key.png")
        key_rect = key_image.get_rect()

        rect_width = max(title_rect.width, description_rect.width, key_rect.width)
        rect_height = title_rect.height + description_rect.height + key_rect.height

        # Set the size of the bubble surface
        bubble_width = rect_width + 24  # Add padding
        bubble_height = rect_height + 32  # Add paddingtotal_text_height

        # Create a surface for the bubble with a white background
        self.image = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)

        # TODO:
        if self.planet.locked:
            rect_color = (11, 9, 18, 200)
        else:
            rect_color = (11, 9, 18)

        pygame.draw.rect(self.image, rect_color, (0, 0, bubble_width, bubble_height), border_radius=10)

        border_color = (66, 160, 180)
        pygame.draw.rect(self.image, border_color, (0, 0, bubble_width, bubble_height), 2, border_radius=10)

        self.rect = self.image.get_rect()
        self.rect.center = (planet.x, planet.rect.top -  (0.8 * planet.rect.height))

        # Position the title and description text surfaces within the bubble
        title_rect = title_surface.get_rect()
        description_rect = description_surface.get_rect()

        title_rect.centerx = self.rect.width // 2
        title_rect.top = 12  # Adjust vertical position as needed

        description_rect.centerx = self.rect.width // 2
        description_rect.top = title_rect.bottom + 8  # Adjust vertical position as needed

        key_rect.centerx = self.rect.width // 2
        key_rect.top = description_rect.bottom + 4

        # Blit the title and description onto the bubble image
        self.image.blit(title_surface, title_rect)
        self.image.blit(description_surface, description_rect)
        self.image.blit(key_image, key_rect)
