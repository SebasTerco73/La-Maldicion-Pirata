import pygame
import random
from settings import IMAGES_LVL2 as ENEMIES, SCREEN_WIDTH, SOUNDS_LVL3
from .character import Character
from .ghost import Ghost
from .cannonBoss import CannonBoss


class Boss2(Character):
    def __init__(self, ground, ghost_group):
        # Sitúa al cangrejo sobre el suelo (bottom = ground)
        self.ground = ground
        y = ground - 150
        x = SCREEN_WIDTH * 3 - 150
        super().__init__(ENEMIES["enemy_boss"], x, y, width=150, height=150)
        self.ghost_group = ghost_group
        self.take_damage_sound =pygame.mixer.Sound(SOUNDS_LVL3["boss_damage"]) 
        self.death_sound = pygame.mixer.Sound(SOUNDS_LVL3["boss_kill"])

        # Propiedades de daño
        self.damage = 20
        self.attack_cooldown = 1.0  # Segundos entre ataques
        self.attack_timer = 0.0
        self.health = 100 # Aca va 100

          # 🔫 Sistema de disparo
        self.shoot_cooldown = 10
        self.shoot_timer = 7.0
        self.bullets = pygame.sprite.Group()

    def shoot(self, player):
        # Determinar dirección hacia el jugador
        direction = -1 if player.rect.centerx < self.rect.centerx else 1
        bullet_y = self.rect.centery
        bullet_x = self.rect.centerx + (direction * 60)
        bullet = CannonBoss(bullet_x, bullet_y, direction)
        self.bullets.add(bullet)

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
                self.take_damage(25)
                self.take_damage_sound.play()
                

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
        self.bullets.empty()
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
                self.death_sound.play()
                # Calcular duración del sonido
                wait_time_ms = int(self.death_sound.get_length() * 1000)
                # Esperar a que termine
                pygame.time.delay(wait_time_ms)
                # Finalmente eliminar al jefe
                self.kill()
            except Exception:
                pass
        else:
        # Cada vez que recibe daño, regenerar fantasmas
            self.regenerate_ghosts()

    def update(self, dt, player=None):
        # Actualizar temporizadores
        if self.attack_timer > 0.0:
            self.attack_timer -= dt
        if self.shoot_timer > 0.0:
            self.shoot_timer -= dt

        # Verificar disparo
        if self.shoot_timer <= 0.0 and player:
            self.shoot(player)
            self.shoot_timer = self.shoot_cooldown

        # Actualizar balas
        self.bullets.update(dt)

        # Chequear colisión con jugador
        self.check_collision_with_player(player)

