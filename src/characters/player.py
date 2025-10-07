import pygame
from settings import IMAGES, LVL1_GROUND_Y, FPS
from .character import Character
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from states.event_system import EventSystem, GameEvents

class Player(Character):
    def __init__(self, x, y, ground, dt):
        super().__init__(IMAGES["player"], x, y, width=100, height=100, speed=5)
        # Propiedades de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 1000.0  # Aceleración en píxeles/segundo²
        self.max_speed = 400.0     # Velocidad máxima en píxeles/segundo
        self.friction = 0.85       # Factor de fricción (1 = sin fricción, 0 = fricción máxima)
        
        # Propiedades de salto
        self.gravity = 1200        # Gravedad en píxeles/segundo²
        self.jump_strength = -600  # Fuerza de salto (negativo porque sube)
        self.on_ground = False
        self.ground_y = ground
        self.is_falling = False    # Indica si el jugador está cayendo
        
        # Estado del jugador
        self.health = 100
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1.5  # Segundos de invulnerabilidad después de daño
        
        # Sistema de eventos
        self.event_system = EventSystem.get_instance()
        
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        
        # Movimiento horizontal con aceleración
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x -= self.acceleration * dt
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x += self.acceleration * dt
        else:
            # Aplicar fricción cuando no hay input
            self.vel_x *= self.friction
        
        # Limitar velocidad máxima
        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))
        
        # Salto
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
        
        # Aplicar movimiento
        self.rect.x += self.vel_x * dt
        self.clamp_to_screen()
    
    def apply_gravity(self, dt):
        """Aplica gravedad y limita el suelo"""
        if not self.on_ground:
            self.vel_y += self.gravity * dt
            # Actualizar estado de caída
            self.is_falling = self.vel_y > 0
        
        self.rect.y += self.vel_y * dt

        # Colisión con el suelo
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True
            self.is_falling = False

    def take_damage(self, amount):
        """
        Aplica daño al jugador si no está invulnerable
        """
        if not self.invulnerable:
            self.health -= amount
            self.invulnerable = True
            self.invulnerable_timer = self.invulnerable_duration
            self.event_system.emit(GameEvents.PLAYER_DAMAGE, damage=amount)
            
            if self.health <= 0:
                self.health = 0
                self.event_system.emit(GameEvents.PLAYER_DEATH)

    def update_invulnerability(self, dt):
        """
        Actualiza el temporizador de invulnerabilidad
        """
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def update(self, dt):
        self.handle_input(dt)
        self.apply_gravity(dt)
        self.update_invulnerability(dt)
        self.clamp_to_screen()

