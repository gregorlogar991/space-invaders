import sys

import pygame.sprite
from random import choice, randint
from player import *
import obstacle
from alien import *
from laser import Laser


class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(
            Player((screen_width / 2, screen_height), screen_width, screen_height, 5))

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        obstacle_n = 4
        self.obstacle_positions = [x * (screen_width / obstacle_n) for x in range(obstacle_n)]
        start = ((screen_width / obstacle_n) - (self.block_size * 10)) / 2
        self.position_obstacles(*self.obstacle_positions, x_start=start, y_start=480)

        self.aliens_direction = 1
        self.aliens = pygame.sprite.Group()
        self.create_aliens(lvl1)
        self.alien_lasers = pygame.sprite.Group()

        self.boss = pygame.sprite.GroupSingle()
        self.boss_spawn_time = randint(40, 80)

    def boss_timer(self):
        self.boss_spawn_time -= 1
        if self.boss_spawn_time <= 0:
            self.boss.add(Boss(choice(["left", "right"]), screen_width))
            print("BOSS CREATED")
            self.boss_spawn_time = randint(400, 800)
    def alien_shoot(self):
        if self.aliens:
            self.alien_lasers.add(Laser(screen_height, choice(self.aliens.sprites()).rect.center, -6))

    def alien_position(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_width:
                self.alien_advance_forward(2)
                self.aliens_direction = -1
            if alien.rect.left <= 0:
                self.alien_advance_forward(2)
                self.aliens_direction = 1

    def alien_advance_forward(self, dist):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += dist

    def create_aliens(self, lvl, x_dist=60, y_dist=48, x_margin=70, y_margin=50):
        for index_r, row in enumerate(lvl):
            for index_c, col in enumerate(row):
                if col == "Y":
                    color = "yellow"
                elif col == "G":
                    color = "green"
                else:
                    color = "red"
                self.aliens.add(Alien(color, index_c * x_dist + x_margin, index_r * y_dist + y_margin))

    def position_obstacles(self, *args, x_start, y_start):
        for x_margin in args:
            print(x_margin)
            self.create_obstacle(x_start, y_start, x_margin)

    def create_obstacle(self, x, y, x_margin):
        for r_index, row in enumerate(self.shape):
            for c_index, column in enumerate(row):
                if column == "X":
                    self.blocks.add(
                        obstacle.Block(self.block_size, (241, 79, 80), x + x_margin + c_index * self.block_size,
                                       y + r_index * self.block_size))

    def run(self):
        self.player.update()
        self.aliens.update(self.aliens_direction)
        self.alien_lasers.update()
        self.boss.update()

        self.alien_position()
        self.boss_timer()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.boss.draw(screen)

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game()

    ALIEN_LASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIEN_LASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIEN_LASER:
                game.alien_shoot()
        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
