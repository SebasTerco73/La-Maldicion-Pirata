import pygame
import random
from settings import IMAGES_LVL2 as ENEMIES

from settings import SCREEN_WIDTH, SOUNDS_LVL2
from .character import Character


class Cannon(Character):
    def __init__(self, x, ground):
        # Sitúa al cangrejo sobre el suelo (bottom = ground)
        y = ground - 50
        super().__init__(ENEMIES["enemy_cannon"], x, y, width=50, height=50, speed=500)
        self.original_image = self.image.copy()
        # Física básica
        self.vel_y = 0.0
        self.world_widht = SCREEN_WIDTH * 3
        self.gravity = 300.0
        self.on_ground = True
        self.ground_y = ground
        # Movimiento
        self.direction = random.choice([-1, 1])
        self.movement_timer = 0.0
        self.direction_change_time = random.uniform(2.0, 4.0)
        # Propiedades de daño
        self.damage = 10
        self.attack_cooldown = 1.0  # Segundos entre ataques
        self.attack_timer = 0.0
        self.died = pygame.mixer.Sound(SOUNDS_LVL2["ghost_died"])

    def apply_gravity(self, dt):
        self.vel_y += self.gravity * dt
        self.rect.y += self.vel_y * dt
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0.0
            self.on_ground = True

    def clamp_to_world(self):
        """Evita que el jugador salga de los límites del mundo (no solo de la pantalla)."""
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction *= -1  # Invertir dirección
             
        if self.rect.right > self.world_widht:
            self.rect.right = self.world_widht


    def move_pattern(self, dt):

        # Guardar la dirección anterior
        previous_direction = self.direction

        # Actualizar temporizador de movimiento
        self.movement_timer += dt

        # Cambiar dirección cuando sea necesario
        if self.movement_timer >= self.direction_change_time:
            self.direction *= -1  # Invertir dirección
            self.movement_timer = 0.0
            self.direction_change_time = random.uniform(2.0, 4.0)

        # Mover el cangrejo usando speed heredado
        self.rect.x += int(self.speed * self.direction * dt)

        # Mantener al cangrejo dentro de la pantalla
        self.clamp_to_world()

        # -----------------------------
        # Ajustar la imagen según dirección
        # -----------------------------
        if self.direction > 0:  # moviéndose a la derecha
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:  # moviéndose a la izquierda
            self.image = self.original_image

    def check_collision_with_player(self, player) -> bool:
        """
        Verifica si hay colisión con el jugador y maneja el daño o la eliminación
        """
        if player is None:
            return False

        if self.rect.colliderect(player.rect):
            # Calcular la posición relativa del jugador respecto al cangrejo
            collision_threshold = 10  # Píxeles de margen para considerar que viene desde arriba
            player_bottom = player.rect.bottom
            enemy_top = self.rect.top

            # Determinar si el jugador está cayendo
            is_falling = getattr(player, 'is_falling', None)
            if is_falling is None:
                is_falling = (hasattr(player, 'vel_y') and player.vel_y > 0 and not getattr(player, 'on_ground', False))

            if is_falling and player_bottom < enemy_top + collision_threshold:
                # El jugador elimina al cangrejo
                self.died.play()
                self.kill()  # Elimina el sprite de todos los grupos
                # Dar un pequeño rebote al jugador
                if hasattr(player, 'jump_strength'):
                    player.vel_y = player.jump_strength * 0.5  # La mitad de la fuerza de salto normal
                player.on_ground = False
                return True
            else:
                # Si no es un golpe desde arriba y no está en tiempo de invulnerabilidad
                if self.attack_timer <= 0.0:
                    # Intentar llamar a take_damage si existe
                    if hasattr(player, 'take_damage'):
                        player.take_damage(self.damage)
                    else:
                        if hasattr(player, 'health'):
                            player.health -= self.damage
                    self.attack_timer = self.attack_cooldown
                return True

        return False

    def update(self, dt, player=None):
        # update acepta dt y opcionalmente el jugador (para chequear colisiones)
        self.apply_gravity(dt)

        # Mover el cangrejo
        self.move_pattern(dt)

        # Actualizar temporizador de ataque
        if self.attack_timer > 0.0:
            self.attack_timer -= dt

        # Mantener en el suelo
        self.rect.bottom = self.ground_y

        # Si se pasó player, chequear colisión
        if player is not None:
            self.check_collision_with_player(player)

