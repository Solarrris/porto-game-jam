import pygame
import math
from objects.tile import Tile

class MovingPlatform(Tile):
    def __init__(self, coordinates, surface, anchor1, anchor2):
        super().__init__(coordinates, surface)
        self.anchor1 = anchor1
        self.anchor2 = anchor2
        self.is_pointing_to_first_point = False
        self.is_horizontal_platform = False

        self.d_x = self.anchor2.rect.x - self.anchor1.rect.x
        self.d_y = self.anchor2.rect.y - self.anchor1.rect.y

        if abs(self.d_x) > abs(self.d_y):
            self.is_horizontal_platform = True

        if (self.is_horizontal_platform and self.d_x < 0) or (not self.is_horizontal_platform and self.d_y < 0):
            temp = self.anchor1
            self.anchor1 = self.anchor2
            self.anchor2 = temp
        
        if self.is_horizontal_platform:
            self.rect.centery = self.anchor1.rect.centery
        else:
            self.rect.centerx = self.anchor1.rect.centerx


    def update(self, *args, **kwargs):
        if self.is_horizontal_platform:
            if self.is_pointing_to_first_point:
                self.rect.centerx -= 2

                if self.rect.centerx < self.anchor1.rect.centerx:
                    self.rect.centerx = self.anchor1.rect.centerx
                    self.is_pointing_to_first_point = False
            else:
                self.rect.centerx += 2

                if self.rect.centerx > self.anchor2.rect.centerx:
                    self.rect.centerx = self.anchor2.rect.centerx
                    self.is_pointing_to_first_point = True
        else:
            if self.is_pointing_to_first_point:
                self.rect.centery-= 2

                if self.rect.centery < self.anchor1.rect.centery:
                    self.rect.centery = self.anchor1.rect.centery
                    self.is_pointing_to_first_point = False
            else:
                self.rect.centery += 2

                if self.rect.centery > self.anchor2.rect.centery:
                    self.rect.centery = self.anchor2.rect.centery
                    self.is_pointing_to_first_point = True