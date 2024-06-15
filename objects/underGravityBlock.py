import pygame
import math
from objects.tile import Tile

class UnderGravityBlock(Tile):
    def __init__(self, coordinates, surface, player, tiles):
        super().__init__(coordinates, surface)

        self.player = player
        self.tiles = tiles
        self.is_dist_x_higher = False
    
    def update(self, game, screen):
        if self.player.is_attracting:
            d_x = abs(self.rect.centerx - self.player.rect.centerx)
            d_y = abs(self.rect.centery - self.player.rect.centery)

            if (d_y == 0):
                d_y = 1

            hypotenuse = math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2))

            if d_x > d_y:
                self.is_dist_x_higher = True
            else:
                self.is_dist_x_higher = False

            # Plus hipotenuse est grand, moins la vitesse est grande
            speed = 1

            # If the block is to the left of the player
            if self.rect.centerx < self.player.rect.centerx:
                if self.is_dist_x_higher:
                    self.rect.centerx += speed

                    if self.rect.centery < self.player.rect.centery:
                        self.rect.centery += speed * (d_y / d_x)
                    else:
                        self.rect.centery -= speed * (d_y / d_x)
                else:
                    self.rect.centerx += speed * (d_x / d_y)

                    if self.rect.centery < self.player.rect.centery:
                        self.rect.centery += speed
                    else:
                        self.rect.centery -= speed
            
            else:
                if self.is_dist_x_higher:
                    self.rect.centerx -= speed
                    if self.rect.centery < self.player.rect.centery:
                        self.rect.centery += speed * (d_y / d_x)
                    else:
                        self.rect.centery -= speed * (d_y / d_x)
                else:
                    self.rect.centerx -= speed * (d_x / d_y)

                    if self.rect.centery < self.player.rect.centery:
                        self.rect.centery += speed
                    else:
                        self.rect.centery -= speed