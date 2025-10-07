# player.py
import pygame
from settings import IMAGES
from .character import Character
from .events import GameEvents, EventSystem  # Use relative import if events.py is in the same directory

class Player(Character):
    def __init__(self, x, y, ground):
        super().__init__(IMAGES["player"], x, y, width=120, height=120, speed=350)
        self.vel_y = 0
        self.gravity = 1000
        self.jump_strength = -500
        self.on_ground = False
        self.ground_y = ground
        # Estado de salud
        self.max_health = 100
        self.health = self.max_health
        # Invulnerabilidad temporal tras recibir daño (segundos)
        self.invulnerable_timer = 0.0
        # Indicador de invulnerabilidad y duración por defecto
        self.invulnerable = False
        self.invulnerable_duration = 1.0
        # Sistema de eventos (opcional). Si no se pasa uno externo, creamos uno local
        self.event_system = EventSystem()
       
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1
        self.move(dx, dt)
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
    
    def apply_gravity(self, dt):
        self.vel_y += self.gravity * dt
        self.rect.y += self.vel_y * dt
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True

    def update(self, dt):
        self.handle_input(dt)
        self.clamp_to_screen()
        self.apply_gravity(dt)
        # Actualizar timers
        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0.0:
                self.invulnerable_timer = 0.0
                self.invulnerable = False

    @property
    def is_falling(self):
        return self.vel_y > 0 and not self.on_ground

    def take_damage(self, amount):
        """
        Aplica daño al jugador si no está invulnerable
        """
        if amount is None:
            return
        try:
            dmg = float(amount)
        except Exception:
            return
        if dmg <= 0:
            return
        if not getattr(self, 'invulnerable', False):
            self.health = max(0, self.health - dmg)
            self.invulnerable = True
            self.invulnerable_timer = max(0.0, float(getattr(self, 'invulnerable_duration', 1.0)))
            # Emitir eventos sólo si existe event_system y tiene emit
            if hasattr(self, 'event_system') and hasattr(self.event_system, 'emit'):
                try:
                    self.event_system.emit(GameEvents.PLAYER_DAMAGE, damage=dmg)
                except Exception:
                    pass

            if self.health <= 0:
                self.health = 0
                if hasattr(self, 'event_system') and hasattr(self.event_system, 'emit'):
                    try:
                        self.event_system.emit(GameEvents.PLAYER_DEATH)
                    except Exception:
                        pass
