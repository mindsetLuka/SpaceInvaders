import ast
import os
import pygame

from player import Player
from operator import itemgetter
from shield import Shield


class ViewGame:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 650
        self.shield_img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "shield2.png")),
            (110, 80))
        self.EGG = pygame.image.load(
            os.path.join("assets", "player_laser.png"))
        self.MYSTERY_SHIP = pygame.image.load(
            os.path.join("assets", "mystery2.png"))
        self.YELLOW_ENEMY_SHIP = pygame.image.load(
            os.path.join("assets", "yellow_enemy.png"))
        self.WHITE_ENEMY_SHIP = pygame.image.load(
            os.path.join("assets", "white_enemy.png"))
        self.BLUE_ENEMY_SHIP = pygame.image.load(
            os.path.join("assets", "blue_enemy.png"))
        self.GREEN_PLAYER_SHIP = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "green_player.png")),
            (70, 70))
        self.ENEMY_LASER = pygame.image.load(
            os.path.join("assets", "enemy_laser.png"))
        self.PLAYER_LASER = pygame.image.load(
            os.path.join("assets", "player_laser.png"))
        self.BG = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "background-black.png")),
            (self.width, self.height))
        self.COLOR_OF_ENEMY = {
            "yellow": (self.YELLOW_ENEMY_SHIP, self.ENEMY_LASER),
            "blue":
                (self.BLUE_ENEMY_SHIP, self.ENEMY_LASER),
            "white":
                (self.WHITE_ENEMY_SHIP, self.ENEMY_LASER),
            "mystery":
                (self.MYSTERY_SHIP, self.ENEMY_LASER)}
        pygame.font.init()
        self.main_font = pygame.font.SysFont('arial', 20)
        self.dead = pygame.font.SysFont('comicsans', 30)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invaders")
        self.ship = Player(self.window.get_width() / 2 - 30,
                           self.window.get_height() - 50,
                           self.window,
                           self.GREEN_PLAYER_SHIP,
                           self.PLAYER_LASER)
        self.shield1 = Shield(self.window.get_width() / 4 - 50,
                              self.window.get_height() - 200,
                              self.window,
                              self.shield_img)
        self.shield2 = Shield(self.window.get_width() * 3 / 4 - 50,
                              self.window.get_height() - 200,
                              self.window,
                              self.shield_img)

    def redraw_window(self, nickname, lives, level, enemies, lost, scores, s1,
                      s2):
        self.window.blit(self.BG, (0, 0))
        nickname = self.main_font.render(f"Игрок: {nickname}", True,
                                         (255, 255, 255))
        lives_label = self.main_font.render(f"Жизни: {lives}", True,
                                            (255, 255, 255))
        scores_label = self.main_font.render(f"Очки: {scores}", True,
                                             (255, 255, 255))
        level_label = self.main_font.render(f"Уровень: {level}", True,
                                            (255, 255, 255))
        self.window.blit(nickname, (0, 0))
        self.window.blit(level_label,
                         (self.width - level_label.get_width() - 10, 25))
        self.window.blit(scores_label,
                         (self.width - scores_label.get_width() - 10,
                          25 + level_label.get_height() + 10))
        self.window.blit(lives_label,
                         (self.width - lives_label.get_width() - 10,
                          45 + scores_label.get_height()
                          + level_label.get_height()))
        if s1:
            self.shield1.draw()
            self.shield1.health_bar()
        else:
            self.shield1.mask.clear()

        if s2:
            self.shield2.draw()
            self.shield2.health_bar()
        else:
            self.shield2.mask.clear()

        self.ship.draw()
        self.ship.health_bar()
        for enemy in enemies:
            enemy.draw()
        if lost:
            dead = self.dead.render("YOU DIED", True, (255, 0, 0))
            self.window.blit(dead, (
                round(self.width / 2 - dead.get_width() / 2),
                round(self.height / 3 - dead.get_height() / 2)))
        pygame.display.update()

    def one_string_of_menu(self, x, y, text):
        pygame.draw.rect(self.window,
                         (255, 255, 255),
                         (x, y, self.width / 3, self.height / 6))
        pygame.draw.rect(self.window,
                         (0, 0, 0),
                         (x + 10, y + 5,
                          self.width / 3 - 40, self.height / 6 - 20))
        self.window.blit(text, (x + 30, y + 35))

    def redraw_window_menu(self):
        self.window.blit(self.BG, (0, 0))
        self.one_string_of_menu(self.width / 3, self.height / 4,
                                self.main_font.render("PLAY", True,
                                                      (255, 255, 255)))
        self.one_string_of_menu(self.width / 3,
                                self.height / 4 + self.height / 6,
                                self.main_font.render("TABLESCORE", True,
                                                      (255, 255, 255)))
        self.one_string_of_menu(self.width / 3,
                                self.height / 4 + (2 * self.height / 6) - 1,
                                self.main_font.render("QUIT", True,
                                                      (255, 255, 255)))
        pygame.display.update()

    def draw_table_score(self):
        self.window.blit(self.BG, (0, 0))
        self.one_string_of_menu(0, 0,
                                self.main_font.render("PLAY", True,
                                                      (255, 255, 255)))
        self.one_string_of_menu(self.width - self.width / 3,
                                self.height - self.height / 6,
                                self.main_font.render("QUIT", True,
                                                      (255, 255, 255)))
        f = pygame.font.Font(None, 36)
        top = f.render('TOP', True, (255, 255, 255))
        self.window.blit(top, (190, 115))
        player = f.render('Player:', True, (255, 255, 255))
        self.window.blit(player, (100, 150))
        score = f.render('Score:', True, (255, 255, 255))
        self.window.blit(score, (300, 150))

        with open("assets/data.txt", 'r', encoding="cp1251") as file:
            items = [parse_item(line.rstrip()) for line in file]

        t = 50
        for item in sorted(items, key=itemgetter(1), reverse=True):
            name = f.render(str(item[0]), True, (180, 0, 0))
            self.window.blit(name, (100, 150 + t))
            scores = f.render(str(item[1]), True, (180, 0, 0))
            self.window.blit(scores, (300, 150 + t))
            t += 50
        pygame.display.update()

    def draw_easter_egg(self):
        f = pygame.font.Font(None, 27)
        g = pygame.font.Font(None, 15)
        text0 = g.render("https://alexbers.com/", True, (180, 0, 0))
        text1 = f.render("Уважаемый абонент", True, (180, 0, 0))
        text2 = f.render(
            "Данный ресурс заблокирован по решению органов "
            "государственной власти Российской Федерации",
            True, (180, 0, 0))
        text3 = f.render("Dear customer", True, (180, 0, 0))
        text4 = f.render(
            "Access to the requested resource has been blocked "
            "by decision of public authorities of Russian Federation",
            True, (180, 0, 0))
        self.window.blit(text0, (
            self.window.get_width() - 150,
            self.window.get_height() - 30))
        self.window.blit(text1, (
            self.window.get_width() / 2 - 100,
            self.window.get_height() / 2))
        self.window.blit(text2, (
            self.window.get_width() / 6 - 145,
            self.window.get_height() / 2 + 30))
        self.window.blit(text3, (
            self.window.get_width() / 2 - 75,
            self.window.get_height() / 2 + 60))
        self.window.blit(text4, (
            self.window.get_width() / 6 - 145,
            self.window.get_height() / 2 + 90))
        pygame.display.update()


def parse_item(s):
    name, score = ast.literal_eval(s)
    return name, int(score)
