import pygame

import constants
from objects.views.menu import Menu
from objects.player.menuPlayer import MenuPlayer
from objects.planet import Planet
from objects.bubble import Bubble
from objects.views.level import Level
from objects.loading import Loading


class Game:
    levels = ["assets/tilemaps/maps/maps_tmx/level_0/map_lvl0.tmx",
              "assets/tilemaps/maps/maps_tmx/level_1/map_lvl1-1.tmx",
              "assets/tilemaps/maps/maps_tmx/level_2/map_lvl2-1.tmx",
              "assets/tilemaps/maps/maps_tmx/level_3/map_lvl3-1.tmx"]

    def __init__(self, screen):
        self.running = True
        self.is_playing = False
        self.is_lobby = True
        self.is_loading = False
        self.is_starting = False
        self.started = False
        self.loading = Loading(screen)
        self.all = pygame.sprite.Group()
        self.player = MenuPlayer(self, (210, 300))

        # chaque liste correspond à un niveau et chaque partie de niveau à une valeur de la liste
        # les valeurs correspondent aux nombres de conditions pour terminer une partie de niveau
        self.vic_by_lvl = ([2],[0,1],[0,1],[0,0])

        self.sign_msg = (
            "touche 'ESPACE'",
            "La plateforme bouge, saute dessus !",
            "Récupère l'objet avec 'F'",
            "Active le levier avec 'F' pour remplir l'essence",
            "Il te faut l'algorithme de pilotage et de l'essence !",
            "Inverse la gravité avec 'E'",
            "Attire les objets vers toi en appuyant sur 'A'")

        self.planets = pygame.sprite.Group()

        # Planet creation
        planet0 = Planet(self, (150, 300), 40, "TUIL-667", "Tuiiiiiiil!", 0, False)
        planet1 = Planet(self, (300, 500), 40, "Kadelior", "Avec Kadelior ça va fort, ça va très fort", 1, False)
        planet2 = Planet(self, (450, 175), 40, "Imater", "Gros caillou", 2, True)
        #planet3 = Planet(self, (600, 700), 40, "Eucletrade", "Vous allez finir en pierrade", 3, True)
        #planet4 = Planet(self, (750, 300), 40, "Naeldrance", "Allez le XV de France", 4, True)
        planet3 = Planet(self, (900, 500), 40, "Mistraal", "Destination finale", 3, True)

        # self.planets.add(planet0, planet1, planet2, planet3, planet4, planet5)
        self.planets.add(planet0, planet1, planet2, planet3)

        self.currentPlanet = planet1

        # Bubble creation
        bubble_planet0 = Bubble(planet0)
        bubble_planet1 = Bubble(planet1)
        bubble_planet2 = Bubble(planet2)
        bubble_planet3 = Bubble(planet3)
        #bubble_planet4 = Bubble(planet4)
        #bubble_planet5 = Bubble(planet5)

        planet0.add_bubble(bubble_planet0)
        planet1.add_bubble(bubble_planet1)
        planet2.add_bubble(bubble_planet2)
        planet3.add_bubble(bubble_planet3)
        #planet4.add_bubble(bubble_planet4)
        #planet5.add_bubble(bubble_planet5)

        self.bubbles = pygame.sprite.Group()
        # self.bubbles.add(bubble_planet0, bubble_planet1, bubble_planet2, bubble_planet3, bubble_planet4, bubble_planet5)
        self.bubbles.add(bubble_planet0, bubble_planet1, bubble_planet2, bubble_planet3)

        # self.all.add(planet0, planet1, planet2, planet3, planet4, planet5, self.player)
        self.all.add(planet0, planet1, planet2, planet3, self.player)

        self.background = pygame.image.load("assets/sprites/images/main-background.png")
        self.background_rect = self.background.get_rect()

        self.clock = pygame.time.Clock()
        self.dt = 0

        self.menu = Menu(screen)

        self.currentLevel = 0

        self.compteur = 0

        # Sounds
        self.interface_sound = pygame.mixer.Sound(f"{constants.SOUNDS_PATH}/interface.mp3")
        self.interface_sound.set_volume(constants.SOUNDS_VOLUME)
        self.jump_sound = pygame.mixer.Sound(f"{constants.SOUNDS_PATH}/jump.mp3")
        self.jump_sound.set_volume(constants.SOUNDS_VOLUME)

        # Music
        pygame.mixer.music.load(f"{constants.SOUNDS_PATH}/main-theme.mp3")
        pygame.mixer.music.set_volume(constants.MUSIC_VOLUME)
        pygame.mixer.music.play(-1)

    def start(self):
        self.started = True
        self.is_starting = True

    def start_level(self, planet, screen):
        self.is_lobby = False
        self.all.remove(self.planets, self.bubbles)

        level = planet.level
        path_to_level_tile_map = self.levels[level]
        path_to_background = f"assets/sprites/images/level{level}-bg.png"

        self.level = Level(self, path_to_level_tile_map, path_to_background, level, 300, screen, self.vic_by_lvl[level][0])
    
    def start_next_part(self, level, screen):
        path_to_level_tile_map = "assets/tilemaps/maps/maps_tmx/level_"+str(level)+"/map_lvl"+str(level)+"-2.tmx"
        path_to_background = f"assets/sprites/images/level{level}-bg.png"

        self.level = Level(self, path_to_level_tile_map, path_to_background, level, 300, screen, self.vic_by_lvl[level][1])


    def update(self, screen):
        if self.is_starting:
            text_y = 0
            text_x = screen.get_width() / 2
            texts = ["", "Dans un passé lointain, la Terre se trouvait au seuil de la catastrophe, incapable de soutenir la", "surpopulation humaine.", "", "Face à ce défi colossal, une mission audacieuse fut initiée : la quête d'une nouvelle planète pouvant",
                     "offrir refuge à l'humanité.", "", "D'immenses vaisseaux spatiaux furent préparés, équipés d'androïdes chargés d'explorer l'immensité", "de l'espace à la recherche d'un nouveau foyer.", "", "Chacune de ces missions était une lueur d'espoir pour l'avenir de notre espèce.",
                     "", "À bord d'un de ces vaisseaux, notre androïde, Porto, partit en quête d'une nouvelle planète,", "ignorant le destin subi par les planète habitables découvertes lors de ses missions passées :",
                     "la destruction aux mains de l'humanité.", "", "Cette fois-ci, Porto parti découvrir le système d'Exploranchon"]
            font = pygame.font.Font("./assets/fonts/main-font.ttf", 24)
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1024, 768))
            for text in texts:
                texte_surface = font.render(text, True, (255, 255, 255))
                text_rect = texte_surface.get_rect()  

                text_rect.centerx = text_x 
                text_rect.centery = text_y

                screen.blit(texte_surface, text_rect)
                text_y = text_y + text_rect.height

            keys = pygame.key.get_pressed()

            if self.compteur > 10000 or keys[pygame.K_SPACE]:
                self.is_starting = False
                self.start_level(self.currentPlanet, screen)
                self.is_playing = True

            self.compteur+=1
        
        else:
            # Clear background
            screen.fill((255, 255, 255))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.is_playing = False

            if not self.is_playing:
                self.menu.update(screen, self)
            elif self.is_lobby:
                screen.blit(self.background, self.background_rect)

                for planet in self.planets:
                    planet.draw(screen)

                    current_planet = None

                    # Check if player is on planet
                    for planet in self.planets:
                        if self.player.rect.colliderect(planet.hitbox):
                            current_planet = planet
                            break

                    # If player on planet
                    if current_planet:
                        self.player.ship = False
                        self.all.add(current_planet.bubble)

                    else:
                        self.player.ship = True
                        self.all.remove(self.bubbles)

                    if keys[pygame.K_SPACE] and current_planet and not current_planet.locked:
                        self.start_level(current_planet, screen)

                # Update screen
                self.all.update(self.dt)
                self.all.draw(screen)
                for planet in self.planets:
                    planet.draw(screen)

            else:
                self.level.update(screen, self)

            self.dt = self.clock.tick(60) / 1000

    def set_sounds_volume(self, new_volume):
        self.interface_sound.set_volume(new_volume)
        self.jump_sound.set_volume(new_volume)

    def next_level(self):
        self.currentLevel += 1
        self.is_lobby = True
        self.planets.sprites()[self.currentLevel].locked = False

