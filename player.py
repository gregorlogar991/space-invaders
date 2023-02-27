import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, init_pos, screen_width, screen_height, speed):
        super().__init__()
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=init_pos)
        self.can_shoot = True
        self.shoot_time = 0
        self.laser_wait = 600

        self.lasers = pygame.sprite.Group()

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and self.rect.bottomright[0] <= self.screen_width:
            self.rect.x += self.speed
        elif pressed[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if pressed[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def reload(self):
        if not self.can_shoot:
            if pygame.time.get_ticks() - self.shoot_time >= self.laser_wait:
                self.can_shoot = True

    def update(self):
        self.input()
        self.reload()
        self.lasers.update()

    def shoot(self):
        self.lasers.add(Laser(self.screen_height, self.rect.center, 8))
