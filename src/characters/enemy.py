import pygame
import random
from settings import ENEMIES


class Crab(pygame.sprite.Sprite):
    def __init__(self, x, ground):
        super().__init__()
        self.image = pygame.image.load(ENEMIES["crab"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(bottomleft=(x, ground))

    # Propiedades del NPC (Non-Player Character)
    npc_tamanio = 30
    npc_velocidad = 2

    direcciones = [(npc_velocidad, 0), (-npc_velocidad, 0)]
    direccion_a_moverse = random.choice(direcciones)