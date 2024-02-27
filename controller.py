import random
import pygame

from crossing import cross
from levels import Level
from player import Player
from viewgame import ViewGame


class Game:
    def __init__(self):
        self.run = True
        self.FPS = 60
        self.level = 1
        self.lives = 5
        self.scores = 0
        self.lost_count = 0
        self.lost = False
        self.player_speed = 4
        self.laser_speed = 5
        self.view_of_game = ViewGame()
        self.need_input = False
        self.input_comp = False
        self.text_input = ''
        self.name = ''

    def main_menu(self):
        self.run = True
        self.level = 1
        self.lives = 5
        self.scores = 0
        self.lost_count = 0
        self.lost = False
        self.view_of_game.ship = Player(
            self.view_of_game.window.get_width() / 2 - 30,
            self.view_of_game.window.get_height() - 50,
            self.view_of_game.window,
            self.view_of_game.GREEN_PLAYER_SHIP,
            self.view_of_game.PLAYER_LASER)
        while self.run:
            mouse = pygame.mouse.get_pos()
            self.view_of_game.redraw_window_menu()
            for event in pygame.event.get():
                self.view_of_game.redraw_window_menu()
                if event.type == pygame.QUIT:
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view_of_game.width / 3 < \
                            mouse[0] < 2 * self.view_of_game.width / 3 \
                            and self.view_of_game.height / 4 < mouse[1] \
                            < (self.view_of_game.height / 4) \
                            + self.view_of_game.height / 6:
                        self.main(self.name)
                    if self.view_of_game.width / 3 < \
                            mouse[0] < 2 * self.view_of_game.width / 3 \
                            and (self.view_of_game.height / 4) \
                            + self.view_of_game.height / 6 < mouse[1] \
                            < (self.view_of_game.height / 4) \
                            + 2 * self.view_of_game.height / 6:
                        self.table()

                    if self.view_of_game.width / 3 < mouse[0] \
                            < 2 * self.view_of_game.width / 3 \
                            and (self.view_of_game.height / 4) \
                            + 2 * self.view_of_game.height / 6 < mouse[1] \
                            < (self.view_of_game.height / 4) \
                            + 3 * self.view_of_game.height / 6:
                        quit(0)
        pygame.quit()

    def main(self, nickname):
        self.run = True
        s1 = True
        s2 = True
        enemies = []
        shield1 = self.view_of_game.shield1
        shield2 = self.view_of_game.shield2
        main_ship = self.view_of_game.ship
        clock = pygame.time.Clock()
        all_level_enemies = Level(self.view_of_game, self.level)
        enemies += all_level_enemies.enemies
        while self.run:
            clock.tick(self.FPS)
            self.view_of_game.redraw_window(nickname,
                                            self.lives,
                                            self.level,
                                            enemies,
                                            self.lost,
                                            self.scores,
                                            s1, s2)
            if self.lost:
                if self.lost_count > self.FPS * 3:
                    self.run = False
                    with open("assets/data.txt", "a", encoding="cp1251") \
                            as file:
                        file.write(f'(\'{self.name}\', \'{self.scores}\')\n')
                else:
                    self.lost_count += 1
                    continue
            if self.lives < 0 or main_ship.health <= 0:
                self.lost = True

            if len(enemies) == 0:
                self.level += 1
                enemies += all_level_enemies.make_level_enemies(self.level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] and main_ship.y > 0 \
                    and not cross(main_ship, shield1) \
                    and not cross(main_ship, shield2):
                main_ship.y -= self.player_speed
            if keys[pygame.K_a] and main_ship.x - self.player_speed > 0 \
                    and not cross(main_ship, shield1) \
                    and not cross(main_ship, shield2):
                main_ship.x -= self.player_speed
            if keys[pygame.K_d] and \
                    main_ship.x < self.view_of_game.window.get_width() - 30 \
                    and not cross(main_ship, shield1) \
                    and not cross(main_ship, shield2):
                main_ship.x += self.player_speed
            if keys[pygame.K_s] and \
                    main_ship.y < self.view_of_game.window.get_height() - 50 \
                    and not cross(main_ship, shield1) \
                    and not cross(main_ship, shield2):
                main_ship.y += self.player_speed
            if keys[pygame.K_w] and cross(main_ship, shield1) \
                    and not (main_ship.y > shield1.y + 20
                             and shield1.x - 55 < main_ship.x
                             < shield1.x + 100):
                main_ship.y -= self.player_speed
            if keys[pygame.K_s] and cross(main_ship, shield1) \
                    and (main_ship.y > shield1.y + 20
                         and shield1.x - 55 < main_ship.x < shield1.x + 100):
                main_ship.y += self.player_speed
            if keys[pygame.K_a] and cross(main_ship, shield1) \
                    and main_ship.x - self.player_speed > 0 \
                    and shield1.x - 50 > main_ship.x:
                main_ship.x -= self.player_speed
            if keys[pygame.K_d] and cross(main_ship, shield1) \
                    and main_ship.x > shield1.x + 80:
                main_ship.x += self.player_speed
            if keys[pygame.K_w] and cross(main_ship, shield2) \
                    and not (main_ship.y > shield2.y + 20
                             and shield2.x - 55 < main_ship.x
                             < shield2.x + 100):
                main_ship.y -= self.player_speed
            if keys[pygame.K_s] and cross(main_ship, shield2) \
                    and (main_ship.y > shield2.y + 20
                         and shield2.x - 55 < main_ship.x < shield2.x + 100):
                main_ship.y += self.player_speed
            if keys[pygame.K_a] and cross(main_ship, shield2) \
                    and main_ship.x - self.player_speed > 0 \
                    and shield2.x - 50 > main_ship.x:
                main_ship.x -= self.player_speed
            if keys[pygame.K_d] and cross(main_ship, shield2) \
                    and main_ship.x > shield2.x + 80:
                main_ship.x += self.player_speed

            if keys[pygame.K_SPACE]:
                main_ship.shoot()
            if keys[pygame.K_z]:
                main_ship.shoot_z()
            if keys[pygame.K_x]:
                main_ship.shoot_x()
            if keys[pygame.K_ESCAPE]:
                self.run = False
            if main_ship.x == (self.view_of_game.width - 30) \
                    and (main_ship.y == self.view_of_game.height - 50):
                self.easter_egg()
                self.run = False

            for enemy in enemies:
                enemy.move()
                enemy.move_lasers(self.laser_speed, main_ship, 1)
                enemy.move_lasers(self.laser_speed / 5 + 1, shield1, 2)
                enemy.move_lasers(self.laser_speed / 5 + 1, shield2, 2)
                if enemy.health <= 0:
                    enemies.remove(enemy)
                    self.scores += 10 * enemy.bonus
                if random.randrange(0, 180) == 1:
                    enemy.shoot()
                if cross(enemy, main_ship):
                    if enemy.bonus == 5:
                        self.lost = True
                if cross(enemy, shield1):
                    if enemy.bonus == 5:
                        s1 = False
                if cross(enemy, shield2):
                    if enemy.bonus == 5:
                        s2 = False
                if cross(enemy, main_ship):
                    self.scores += 10
                    main_ship.health -= 20
                    if enemy in enemies:
                        enemies.remove(enemy)
                if cross(enemy, shield1):
                    shield1.health -= 10
                    if enemy in enemies:
                        enemies.remove(enemy)
                if cross(enemy, shield2):
                    shield2.health -= 10
                    if enemy in enemies:
                        enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > self.view_of_game.height:
                    self.lives -= 1
                    if enemy in enemies:
                        enemies.remove(enemy)
            if shield1.health <= 0:
                s1 = False
            if shield2.health <= 0:
                s2 = False
            main_ship.move_lasers(self.laser_speed - 2, enemies, 1)
            main_ship.lasers_in_shield(self.laser_speed - 2, shield1, 1)
            main_ship.lasers_in_shield(self.laser_speed - 2, shield2, 1)
        self.main_menu()

    def table(self):
        while self.run:
            mouse = pygame.mouse.get_pos()
            self.view_of_game.draw_table_score()
            for event in pygame.event.get():
                self.view_of_game.draw_table_score()
                if event.type == pygame.QUIT:
                    self.main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 0 < mouse[0] < self.view_of_game.width / 3 \
                            and 0 < mouse[1] < self.view_of_game.height / 4:
                        self.main(self.name)
                    if 2 * self.view_of_game.width / 3 < mouse[0] \
                            < self.view_of_game.width \
                            and 3 * self.view_of_game.height / 4 < mouse[1] <\
                            self.view_of_game.height:
                        quit(0)

    def easter_egg(self):
        while self.run:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            self.view_of_game.window.blit(self.view_of_game.BG, (0, 0))
            input_rect = pygame.Rect(self.view_of_game.width / 2 - 125,
                                     self.view_of_game.height / 2 - 200, 250,
                                     70)
            pygame.draw.rect(self.view_of_game.window, (255, 255, 255),
                             input_rect)
            self.view_of_game.window.blit(
                self.view_of_game.main_font.render("НАЧАТЬ ИГРУ",
                                                   1, (180, 0, 0)), (
                    self.view_of_game.width / 2 - 125 + 70,
                    self.view_of_game.height / 2 - 200 + 25))
            if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
                self.run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_menu()
            self.view_of_game.draw_easter_egg()
        self.main_menu()

    def start(self):
        while self.run:
            self.view_of_game.window.blit(self.view_of_game.BG, (0, 0))
            self.view_of_game.one_string_of_menu(
                self.view_of_game.width / 2 - self.view_of_game.width / 6, 0,
                self.view_of_game.main_font.render("ВВЕДИТЕ ИМЯ В ПОЛЕ НИЖЕ",
                                                   1, (255, 255, 255)))
            input_rect = pygame.Rect(self.view_of_game.width / 2 - 125,
                                     self.view_of_game.height / 2 - 200, 250,
                                     70)
            pygame.draw.rect(self.view_of_game.window, (255, 255, 255),
                             input_rect)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
                self.need_input = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                if self.need_input and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.need_input = False
                        self.name = self.text_input
                        self.text_input = ''
                        self.run = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    else:
                        if len(self.text_input) < 10:
                            self.text_input += event.unicode
            if len(self.text_input):
                f1 = pygame.font.Font(None, 36)
                text1 = f1.render(self.text_input, True, (180, 0, 0))
                self.view_of_game.window.blit(text1, (
                    self.view_of_game.width / 2 - 115,
                    self.view_of_game.height / 2 - 175))
            pygame.display.update()
        self.main(self.name)
