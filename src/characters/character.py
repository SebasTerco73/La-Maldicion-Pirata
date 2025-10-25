# character.py
import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=100, height=100, speed=200):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def move(self, dx, dt=1):
        self.rect.x += dx * self.speed * dt

    def update(self):
        pass
