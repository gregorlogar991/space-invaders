import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load(f"images/{color}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction


lvl1 = [
    "YYYYYYYY",
    "GGGGGGGG",
    "GGGGGGGG",
    "RRRRRRRR",
    "RRRRRRRR",
    "RRRRRRRR",
]
