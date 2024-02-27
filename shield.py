import pygame


class Shield:
    COOLDOWN = 20

    def __init__(self, x, y, window, shield_img, health=500):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.shield_img = shield_img
        self.window = window
        self.mask = pygame.mask.from_surface(self.shield_img)

    def draw(self):
        self.x = self.x % self.window.get_width()
        self.window.blit(self.shield_img, (self.x, self.y))

    def health_bar(self):
        pygame.draw.rect(self.window, (255, 0, 0), (
            self.x, self.y + self.shield_img.get_height() + 10,
            self.shield_img.get_width(), 10))
        pygame.draw.rect(self.window, (0, 255, 0), (
            self.x, self.y + self.shield_img.get_height() + 10,
            self.shield_img.get_width() * (self.health / self.max_health), 10))
