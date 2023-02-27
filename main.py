import sys

import pygame.sprite

from player import *
import obstacle
from alien import *


class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(
            Player((screen_width / 2, screen_height), screen_width, screen_height, 5))

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        obstacle_n = 4
        self.obstacle_positions = [x * (screen_width / obstacle_n) for x in range(obstacle_n)]
        print(self.obstacle_positions)
        start = ((screen_width / obstacle_n) - (self.block_size * 10)) / 2
        print(start)
        self.position_obstacles(*self.obstacle_positions, x_start=start, y_start=480)

        self.aliens_direction = 1
        self.aliens = pygame.sprite.Group()
        self.create_aliens(lvl1)

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
                color = ""
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
        self.alien_position()
        self.aliens.update(self.aliens_direction)

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
