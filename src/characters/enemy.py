"""
Clase para los enemigos tipo cangrejo.
"""
import pygame
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import IMAGES
from .character import Character
from states.event_system import EventSystem, GameEvents

class Crab(Character):
    def __init__(self, x, y, ground_y):
        super().__init__(IMAGES["cangrejo"], x, y, width=60, height=60, speed=3)
        # Propiedades de movimiento
        self.vel_x = 50.0
        self.ground_y = ground_y
        self.direction = 1  # 1 derecha, -1 izquierda
        self.movement_timer = 0
        self.direction_change_time = random.uniform(2.0, 4.0)  # Cambia dirección cada 2-4 segundos
        
        # Propiedades de daño
        self.damage = 10
        self.attack_cooldown = 1.0  # Segundos entre ataques
        self.attack_timer = 0
        
    def move_pattern(self, dt):
        """
        Implementa el patrón de movimiento del cangrejo
        """
        # Actualizar temporizador de movimiento
        self.movement_timer += dt
        
        # Cambiar dirección cuando sea necesario
        if self.movement_timer >= self.direction_change_time:
            self.direction *= -1  # Invertir dirección
            self.movement_timer = 0
            self.direction_change_time = random.uniform(2.0, 4.0)
        
        # Mover el cangrejo
        self.rect.x += self.vel_x * self.direction * dt
        
        # Mantener al cangrejo dentro de la pantalla
        self.clamp_to_screen()
        
    def check_collision_with_player(self, player) -> bool:
        """
        Verifica si hay colisión con el jugador y maneja el daño o la eliminación
        """
        if self.rect.colliderect(player.rect):
            # Calcular la posición relativa del jugador respecto al cangrejo
            collision_threshold = 10  # Píxeles de margen para considerar que viene desde arriba
            player_bottom = player.rect.bottom
            enemy_top = self.rect.top
            
            # Si el jugador está cayendo y golpea desde arriba
            if player.is_falling and player_bottom < enemy_top + collision_threshold:
                # El jugador elimina al cangrejo
                self.kill()  # Elimina el sprite de todos los grupos
                # Dar un pequeño rebote al jugador
                player.vel_y = player.jump_strength * 0.5  # La mitad de la fuerza de salto normal
                player.on_ground = False
                return True
            else:
                # Si no es un golpe desde arriba y no está en tiempo de invulnerabilidad
                if self.attack_timer <= 0:
                    player.take_damage(self.damage)
                    self.attack_timer = self.attack_cooldown
                return True
        return False
    
    def update(self, dt, player=None):
        """
        Actualiza el estado del cangrejo
        """
        if player is None:
            return
            
        self.move_pattern(dt)
        
        # Actualizar temporizador de ataque
        if self.attack_timer > 0:
            self.attack_timer -= dt
        
        # Mantener en el suelo
        self.rect.bottom = self.ground_y
        
        # Comprobar colisión con el jugador
        self.check_collision_with_player(player)
