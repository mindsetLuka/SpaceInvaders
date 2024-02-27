import random

from enemy import Enemy


class Level:
    def __init__(self, view1, level):
        self.view1 = view1
        self.level = level
        self.wave_length = 3
        self.enemies = self.make_level_enemies(level)

    def make_level_enemies(self, lvl):
        enemies = []
        self.wave_length += 4
        for i in range(self.wave_length):
            rand_color = random.choice(["yellow", "blue", "white"])
            enemy = Enemy(random.randrange(50, self.view1.width - 50),
                          random.randrange(round((-1300 * self.level) * 0.7),
                                           -100),
                          self.view1.window,
                          self.view1.COLOR_OF_ENEMY[rand_color], rand_color)
            enemies.append(enemy)
        if lvl % 5 == 0:
            enemies.append(Enemy(random.randrange(200, self.view1.width - 200),
                                 random.randrange(
                                     round((-700 * lvl) * 0.7),
                                     -100),
                                 self.view1.window,
                                 self.view1.COLOR_OF_ENEMY["mystery"],
                                 "mystery"))
        return enemies
