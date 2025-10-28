# characters/boss_bullet.py
import pygame
from settings import SCREEN_WIDTH, IMAGES_LVL3


class CannonBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=1, speed=200):
        super().__init__()
        self.image = pygame.image.load(IMAGES_LVL3["cannon_boss"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # 1 = derecha, -1 = izquierda
        self.speed = speed

    def update(self, dt):
        # Movimiento horizontal
        self.rect.x += self.direction * self.speed * dt

        # Si sale de la pantalla, eliminarlo
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH * 3:
            self.kill()
