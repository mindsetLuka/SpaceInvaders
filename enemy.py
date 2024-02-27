import pygame.mask

from laser import Laser
from ship import Ship


class Enemy(Ship):
    def __init__(self, x, y, window, img_with_color, color, health=100):
        super().__init__(x, y, window, health)
        self.ship_img = img_with_color[0]
        self.laser_img = img_with_color[1]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.speed = 1
        self.bonus = 1
        if color == "blue":
            self.speed = 1.5
        if color == "mystery":
            self.health = 600
            self.bonus = 5

    def move(self):
        self.y += self.speed

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(round(self.x + 37.5),
                          round(self.y + 35),
                          self.laser_img, "s")
            self.lasers.append(laser)
            self.cooldown_counter = 1
