import pygame.mask

from ship import Ship
from laser import Laser


class Player(Ship):
    def __init__(self, x, y, window, ship_img, laser_img, health=100):
        super().__init__(x, y, window, health)
        self.ship_img = ship_img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, speed, objs, const):
        self.reload()
        for laser in self.lasers:
            laser.move_one_laser(-speed)
            if laser.off_screen(self.window.get_height()):
                if laser in self.lasers:
                    self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 100
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def lasers_in_shield(self, speed, obj, const):
        self.reload()
        for laser in self.lasers:
            laser.move_one_laser(-speed)
            if laser.off_screen(self.window.get_height()):
                if laser in self.lasers:
                    self.lasers.remove(laser)
            else:
                if laser.collision(obj):
                    obj.health -= 10 * const
                    if laser in self.lasers:
                        self.lasers.remove(laser)

    def health_bar(self):
        pygame.draw.rect(self.window, (255, 0, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width(), 10))
        pygame.draw.rect(self.window, (0, 255, 0), (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health), 10))

    def shoot_z(self):
        if self.cooldown_counter == 0:
            laser = Laser(round(self.x - 20),
                          round(self.y + 35),
                          self.laser_img, "z")
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def shoot_x(self):
        if self.cooldown_counter == 0:
            laser = Laser(round(self.x + 55),
                          round(self.y + 35),
                          self.laser_img, "x")
            self.lasers.append(laser)
            self.cooldown_counter = 1
