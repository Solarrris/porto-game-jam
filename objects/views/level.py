import pygame
import re

import constants
from pytmx.util_pygame import load_pygame
from objects.tile import Tile
from objects.player.levelPlayer import LevelPlayer
from objects.sign import Sign
from objects.movingPlatform import MovingPlatform
from objects.deathBlock import DeathBlock
from objects.underGravityBlock import UnderGravityBlock

class Level:
    def __init__(self, game, pathToTilemap, pathToBackground, number, camera_y, screen, nbcond):
        self.game = game
        self.pathToTileMap = pathToTilemap
        self.pathToBackground = pathToBackground
        self.screen = screen
        self.condVic = []

        camera_x = 0
        camera_y = camera_y
        # Ensure the camera doesn't go beyond the game world boundaries
        self.camera = pygame.Rect(camera_x, camera_y, 1024, 768)
        
        for i in range(nbcond):
            self.condVic.append(False)

        self.background = pygame.image.load(self.pathToBackground)
        self.background_rect = self.background.get_rect()

        self.all = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.signs = pygame.sprite.Group()
        # [[tile,obj,is_activated], ...]
        self.object_tiles = []

        self.player = LevelPlayer(self.game, (100, 600), None)

        self.load_tilemap()

        self.player.tiles = self.tiles

        self.number = number

        self.all.add(self.player)

        self.is_finish = False

        # Définition des niveaux dans lesquels le joueur possède directement ses compétences
        if number == 2:
            self.player.catch_invert_object = True
        if number == 3:
            self.player.catch_invert_object = True
            self.player.catch_attract_object = True

    def load_tilemap(self):
        tmx_data = load_pygame(self.pathToTileMap)

        layers = tmx_data.layers
        tile_layers = tmx_data.visible_tile_layers
        obj_groups = tmx_data.objectgroups

        self.max_width = 0
        self.max_height = 0

        for layer in tile_layers:
            layer = layers[layer]
            if (self.max_width < layer.width):
                self.max_width = layer.width
            if self.max_height < layer.height:
                self.max_height = layer.height
            for x, y, surface in layer.tiles():
                surface = pygame.transform.scale(surface, (surface.get_width() * 2.5, surface.get_height() * 2.5))
                if layer.name == "Mort":
                    deathBlock = DeathBlock((x * 40 - 40, y * 40), surface, self.player)
                    self.all.add(deathBlock)
                else:
                    tile = Tile((x * 40 - 40, y * 40), surface)
                    if layer.name == "Tuiles":
                        self.tiles.add(tile)
                    self.all.add(tile)

        for group in obj_groups:
            if re.match("Plateforme[0-9]?", group.name) is not None:
                anchor1 = group[2]
                anchor2 = group[1]
                plat = group[0]

                surface = plat.image
                surface = pygame.transform.scale(surface, (surface.get_width() * 2.5, surface.get_height() * 2.5))
                surface_anchor = anchor1.image
                surface_anchor = pygame.transform.scale(surface_anchor, (
                surface_anchor.get_width() * 2.5, surface_anchor.get_height() * 2.5))

                anchor1 = Tile((anchor1.x * 2.5 - 40, anchor1.y * 2.5), surface_anchor)
                anchor2 = Tile((anchor2.x * 2.5 - 40, anchor2.y * 2.5), surface_anchor)

                self.all.add(anchor1, anchor2)

                plateforme = MovingPlatform((plat.x * 2.5 - 40, plat.y * 2.5), surface, anchor1, anchor2)
                self.tiles.add(plateforme)
                self.all.add(plateforme)
            else:
                for obj in group:
                    surface = obj.image
                    surface = pygame.transform.scale(surface, (surface.get_width() * 2.5, surface.get_height() * 2.5))
                    if group.name == "Panneaux":
                        if obj.name == "panneau1":
                            num_mes = 0
                        elif obj.name == "panneau2":
                            num_mes = 1
                        elif obj.name == "panneau3":
                            num_mes = 2
                        elif obj.name == "panneau4":
                            num_mes = 3
                        elif obj.name == "panneau5":
                            num_mes = 4
                        elif obj.name == "panneau6":
                            num_mes = 5
                        elif obj.name == "panneau7":
                            num_mes = 6
                        message = self.game.sign_msg[num_mes]
                        sign = Sign((obj.x * 2.5 - 40, obj.y * 2.5), surface, message, self.player, self.camera)
                        self.all.add(sign)
                        self.signs.add(sign)
                    if group.name == "Sous_grav":
                        under_gravity_block = UnderGravityBlock((obj.x * 2.5 - 40, obj.y * 2.5), surface, self.player, self.tiles)
                        self.tiles.add(under_gravity_block)
                        self.all.add(under_gravity_block)
                    elif re.match("bloc[0-9]", obj.name) is not None:
                        tile = Tile((obj.x * 2.5 - 40, obj.y * 2.5), surface)
                        self.tiles.add(tile)
                        self.all.add(tile)
                    else:
                        tile = Tile((obj.x * 2.5 - 40, obj.y * 2.5), surface)
                        self.object_tiles.append([tile, obj, True])
                        self.all.add(tile)

    def update(self, screen, game):
        screen.blit(self.background, self.background_rect)

        # Update screen
        self.all.update(game, screen)

        for sprite in self.all:
            screen.blit(sprite.image, (sprite.rect.x - self.camera.x, sprite.rect.y - self.camera.y))

        if self.camera.x < 0:
            self.camera.x = 0
        if self.camera.x > (self.max_width - 1024):
            self.camera.x = self.max_width - 1024

        self.camera.x = self.player.rect.x - 300

        self.camera.y = self.player.rect.bottom - 500

        self.get_hits_obj(self.object_tiles, screen)

        if self.player.rect.y < -1000:
            self.player.die()

    def get_hits_obj(self, object_tiles, screen):
        keys = pygame.key.get_pressed()

        # obj[0] = Tile
        # obj[1] = objet(avec ses propriétés)
        for obj in object_tiles:
            if not re.match("panneau[0-9]?", obj[1].name):
                if self.player.rect.colliderect(obj[0].rect):
                    if obj[2]:
                        f_key_image = pygame.image.load("./assets/sprites/images/F-Key.png")
                        f_key_image = pygame.transform.scale(f_key_image, (f_key_image.get_width() * 1.5, f_key_image.get_height() * 1.5))
                        f_key_rect = f_key_image.get_rect()
                        f_key_rect.centerx = obj[0].rect.centerx - self.camera.x
                        f_key_rect.centery = obj[0].rect.top - 20 - f_key_rect.height - self.camera.y
                        screen.blit(f_key_image, f_key_rect)

                    if keys[pygame.K_f] and obj[2]:
                        if re.match("levier[0-9]?", obj[1].name) is not None:
                            tmp_img = pygame.image.load("assets/sprites/icons/Levier_droite.png")
                            obj[0].image = pygame.transform.scale(tmp_img, (
                                obj[1].image.get_width() * 2.5, obj[1].image.get_height() * 2.5))
                            obj[2] = False
                            self.to_victory()
                        elif obj[1].name == "vaisseau" or obj[1].name == "portal" or obj[1].name == "end":
                            if len(self.condVic) != 0:
                                indice = 1
                                find = self.condVic[0]
                                while find and indice < len(self.condVic):
                                    find = self.condVic[indice]
                                    indice += 1
                                if find and obj[1].name == "vaisseau":
                                    self.finish()
                                    self.game.is_lobby = True
                                elif find and obj[1].name == "portal":
                                    self.game.start_next_part(self.number,self.screen)
                                elif find and obj[1].name == "end":
                                    self.finish()
                                    self.game.is_lobby = True
                            else:
                                if obj[1].name == "vaisseau":
                                    self.finish()
                                    self.game.is_lobby = True
                                elif obj[1].name == "portal":
                                    self.game.start_next_part(self.number,self.screen)
                                elif obj[1].name == "end":
                                    self.finish()
                                    self.game.is_lobby = True
                        elif obj[1].name == "portal_disabled":
                            pass
                        elif obj[1].name == "inversum":
                            self.player.catch_invert_object = True
                            obj[0].image = pygame.Surface((0, 0))
                            self.to_victory()
                        elif obj[1].name == "gravitum":
                            self.player.catch_attract_object = True
                            obj[0].image = pygame.Surface((0, 0))
                            self.to_victory()
                        else:
                            obj[2] = False
                            self.to_victory()
                            obj[0].image = pygame.Surface((0, 0))

    def to_victory(self):
        if len(self.condVic) != 0:
            find = False
            indice = 0
            while not find and indice < len(self.condVic):
                if not self.condVic[indice]:
                    self.condVic[indice] = True
                    find = True
                indice += 1

    def finish(self):
        self.is_finish = True
        if self.number >= self.game.currentLevel:
            self.game.next_level()
