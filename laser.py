import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, screen_height, pos, speed=8):
        super().__init__()
        self.screen_height = screen_height
        self.image = pygame.Surface((4, 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.move_speed = speed

    def update(self):
        self.rect.y -= self.move_speed
        self.destroy()

    def destroy(self):
        if self.rect.y <= -20 or self.rect.y >= self.screen_height + 20:
            self.kill()

