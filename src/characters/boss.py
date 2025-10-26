import pygame
import random
from settings import IMAGES_LVL2 as ENEMIES, SCREEN_WIDTH, SOUNDS_LVL1
from settings import IMAGES_LVL2
from .character import Character


class Boss(Character):
    def __init__(self, ground):
        # Sitúa al cangrejo sobre el suelo (bottom = ground)
        y = ground - 150
        x = SCREEN_WIDTH * 3 - 150
        super().__init__(ENEMIES["enemy_boss"], x, y, width=150, height=150)
        # Física básica

        # Propiedades de daño
        self.damage = 10
        self.attack_cooldown = 1.0  # Segundos entre ataques
        self.attack_timer = 0.0
        self.speed_x = 150  # velocidad de movimiento del jefe (px/seg)

        self.original_image = pygame.image.load(IMAGES_LVL2["enemy_boss"]).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()



        # self.clamp_to_screen()

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
                # self.sound_kill.play()
                # self.kill()  # Elimina el sprite de todos los grupos
                pass
                
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
        # Actualizar temporizador de ataque
        if self.attack_timer > 0.0:
            self.attack_timer -= dt

        # Si se pasó player, chequear colisión
        self.check_collision_with_player(player)