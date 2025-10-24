import pygame
import random
from settings import IMAGES_LVL1 as ENEMIES, SCREEN_WIDTH, DEBUG_COLLISIONS
from .character import Character


class Crab(Character):
    def __init__(self, x, ground):
        # Sitúa al cangrejo sobre el suelo (bottom = ground)
        y = ground - 50
        super().__init__(ENEMIES["enemy_crab"], x, y, width=50, height=50, speed=120)
        # Física básica
        self.world_widht = SCREEN_WIDTH * 3
        self.vel_y = 0.0
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

    def apply_gravity(self, dt):
        self.vel_y += self.gravity * dt
        self.rect.y += self.vel_y * dt
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0.0
            self.on_ground = True

    def clamp_to_world(self):
        """Evita que el jugador salga de los límites del mundo (no solo de la pantalla)."""
        if self.rect.left < 120:
            self.rect.left = 120
            self.direction *= -1  # Invertir dirección
             
        if self.rect.right > self.world_widht:
            self.rect.right = self.world_widht

    def move_pattern(self, dt):
        """
        Implementa el patrón de movimiento del cangrejo
        """
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
        # self.clamp_to_screen()

    def check_collision_with_player(self, player) -> bool:
        """
        Verifica si hay colisión con el jugador y maneja el daño o la eliminación
        """
        if player is None:
            return False
        # Usar máscaras precomputadas (más rápido) cuando estén disponibles
        player_mask = getattr(player, 'mask', None)
        crab_mask = getattr(self, 'mask', None)
        overlap = None
        if player_mask is not None and crab_mask is not None:
            try:
                offset = (self.rect.x - player.rect.x, self.rect.y - player.rect.y)
                overlap = player_mask.overlap(crab_mask, offset)
            except Exception:
                overlap = None

        if not overlap:
            # Como respaldo, revisar rects
            if not self.rect.colliderect(player.rect):
                return False

    # Si hay overlap (o colisión por rect como respaldo), decidir si es stomp
        # Determinar si el jugador está cayendo (falling) usando vel_y o is_falling
        is_falling = getattr(player, 'is_falling', None)
        if is_falling is None:
            is_falling = (hasattr(player, 'vel_y') and getattr(player, 'vel_y', 0) > 50 and not getattr(player, 'on_ground', False))

        # Umbral en píxeles para considerar un stomp preciso
        stomp_threshold = 18
        player_bottom = player.rect.bottom
        enemy_top = self.rect.top

        if is_falling and (player_bottom - enemy_top) < stomp_threshold:
            # Stomp: el jugador elimina al cangrejo
            self.kill()
            # Rebotar el jugador hacia arriba
            if hasattr(player, 'jump_strength') and hasattr(player, 'vel_y'):
                # Asignar una velocidad hacia arriba (negativa) proporcional a jump_strength
                player.vel_y = -abs(getattr(player, 'jump_strength', 8)) * 0.6
            elif hasattr(player, 'jump'):
                # Llamada antigua si existe
                try:
                    player.jump(strength=-8)
                except TypeError:
                    player.jump(-8)
            player.on_ground = False
            return True
        else:
            # Contacto lateral o desde abajo: dañar al jugador con cooldown
            if self.attack_timer <= 0.0:
                if DEBUG_COLLISIONS:
                    print(f"[COLLISION DEBUG] CONTACT (no stomp). Applying damage {self.damage} to player.")
                if hasattr(player, 'take_damage'):
                    player.take_damage(self.damage)
                else:
                    if hasattr(player, 'health'):
                        player.health -= self.damage
                self.attack_timer = self.attack_cooldown
            return True

    def update(self, dt, player=None):
        # update acepta dt y opcionalmente el jugador (para chequear colisiones)
        self.apply_gravity(dt)

        # Mover el cangrejo
        self.move_pattern(dt)
        self.clamp_to_world()

        # Actualizar temporizador de ataque
        if self.attack_timer > 0.0:
            self.attack_timer -= dt

        # Mantener en el suelo
        self.rect.bottom = self.ground_y

        # Si se pasó player, chequear colisión
        if player is not None:
            self.check_collision_with_player(player)

