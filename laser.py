import pygame.mask
import os
from crossing import cross


class Laser:
    def __init__(self, x, y, img, key):
        self.x = x
        self.y = y
        if key == 's':
            self.img = img
        else:
            self.img = pygame.image.load(
                os.path.join("assets", "player_laser_x.png"))
        self.key = key
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move_one_laser(self, speed):
        if self.key == 's':
            self.y += speed
        if self.key == 'z':
            self.x += speed
        if self.key == 'x':
            self.x -= speed

    def off_screen(self, height):
        return not height >= self.y >= 0

    def collision(self, obj):
        return cross(obj, self)
