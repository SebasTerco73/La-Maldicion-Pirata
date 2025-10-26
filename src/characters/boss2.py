import pygame
import random
from settings import IMAGES_LVL2 as ENEMIES, SCREEN_WIDTH
from .character import Character
from .ghost import Ghost


class Boss2(Character):
    def __init__(self, ground, ghost_group):
        # Sitúa al cangrejo sobre el suelo (bottom = ground)
        self.ground = ground
        y = ground - 150
        x = SCREEN_WIDTH * 3 - 150
        super().__init__(ENEMIES["enemy_boss"], x, y, width=150, height=150)
        self.ghost_group = ghost_group

        # Propiedades de daño
        self.damage = 20
        self.attack_cooldown = 1.0  # Segundos entre ataques
        self.attack_timer = 0.0
        self.health = 100 # Aca va 100

    def regenerate_ghosts(self):
        for _ in range(20):
            randomPos = random.randint(600, SCREEN_WIDTH * 3)
            ghost = Ghost(randomPos, self.ground)
            self.ghost_group.add(ghost)

    def check_collision_with_player(self, player) -> bool:
        """
        Verifica si hay colisión con el jugador y maneja el daño o la eliminación
        """
        if player is None:
            return False

        if self.rect.colliderect(player.rect):
            collision_threshold = 10
            player_bottom = player.rect.bottom
            enemy_top = self.rect.top

            # Detectar si el jugador está cayendo
            is_falling = getattr(player, 'is_falling', None)
            if is_falling is None:
                is_falling = (hasattr(player, 'vel_y') and player.vel_y > 0 and not getattr(player, 'on_ground', False))

            if is_falling and player_bottom < enemy_top + collision_threshold:
                # Golpe al boss desde arriba
                self.take_damage(20)

                # Rebote vertical fuerte
                push_distance = player.rect.x  # Distancia hasta la izquierda
                player.rect.x = max(0, player.rect.x - push_distance)  # Se mueve hasta el borde izquierdo

                player.on_ground = False

                # Rebote horizontal (knockback grande hacia la izquierda)
                player.apply_knockback(source_x=self.rect.centerx, strength=80)

                return True

            else:
                # Daño al jugador si colisiona de lado o de frente
                if self.attack_timer <= 0.0:
                    if hasattr(player, 'take_damage'):
                        player.apply_knockback(source_x=self.rect.centerx, strength=80)

                        # El daño se aplica solo si no está invulnerable
                        if not (player.invulnerable_from_damage or player.invulnerable_from_jump):
                            player.take_damage(self.damage)

                    elif hasattr(player, 'health'):
                        player.health -= self.damage
                    self.attack_timer = self.attack_cooldown
                return True

        return False
    
    def take_damage(self, amount):
        """Reduce la vida del boss y lo elimina si llega a 0."""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            # Contar la muerte del boss como puntaje y eliminar
            if not getattr(self, '_score_counted', False):
                self._score_counted = True
                try:
                    if hasattr(self, 'ghost_group') and hasattr(self.ghost_group, 'scene'):
                        # no usual, pero intentar proteger
                        pass
                except Exception:
                    pass
            try:
                self.kill()  # elimina al boss del juego
            except Exception:
                pass
        else:
        # Cada vez que recibe daño, regenerar fantasmas
            self.regenerate_ghosts()

    def update(self, dt, player=None):
        # Actualizar temporizador de ataque
        if self.attack_timer > 0.0:
            self.attack_timer -= dt

        # Si se pasó player, chequear colisión
        self.check_collision_with_player(player)

