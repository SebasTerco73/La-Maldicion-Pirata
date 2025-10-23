# player.py
import pygame
from settings import IMAGES, SCREEN_WIDTH
from .character import Character
from .events import GameEvents, EventSystem  # Use relative import if events.py is in the same directory

class Player(Character):
    """def __init__(self, x, y, ground_y, world_width=None):
    super().__init__()
    # ... tu código actual ...
    self.ground_y = ground_y
    self.world_width = world_width if world_width is not None else SCREEN_WIDTH
    """
    def __init__(self, x, y, ground_y, world_width=None):
        super().__init__(IMAGES["player-right"], x, y, width=90, height=90, speed=250)
        self.image_left = pygame.image.load(IMAGES["player-left"]).convert_alpha()
        self.image_left = pygame.transform.scale(self.image_left, (90, 90))
        self.image_right = pygame.image.load(IMAGES["player-right"]).convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (90, 90))
        self.facing_right = True  # 🔹 inicializamos la dirección al principio

        spritesheet = pygame.image.load(IMAGES["player-walk"]).convert_alpha()
        self.frames = self.extraer_frames(spritesheet, cols=7, rows=1, scale=(100,100))
        self.frame_actual = 0
    
        self.vel_y = 0
        self.gravity = 1500
        self.jump_strength = -550
        self.on_ground = False
        self.ground_y = ground_y
        self.world_width = world_width if world_width is not None else SCREEN_WIDTH
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
        
    def extraer_frames(self, sheet, cols, rows, scale=None):
        frames = []
        w, h = sheet.get_size()
        frame_w, frame_h = w // cols, h // rows
        for y in range(rows):
            for x in range(cols):
                rect = pygame.Rect(x * frame_w, y * frame_h, frame_w, frame_h)
                frame = sheet.subsurface(rect).copy()
                if scale:
                    frame = pygame.transform.smoothscale(frame, scale)
                frames.append(frame)
        return frames
    
    def draw(self, pantalla):
        pantalla.blit(self.frames[int(self.frame_actual)], (self.rect.x, self.rect.y))

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        self.dx = 0  # Guardamos movimiento horizontal

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx = -1
            self.facing_right = False
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx = 1
            self.facing_right = True

        # Mover solo si hay dx
        self.move(self.dx, dt)

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
        self.clamp_to_world()
        self.apply_gravity(dt)

         # Solo animar si hay movimiento horizontal
        anim_fps = 12  # 12 frames por segundo, ajustable
        if getattr(self, 'dx', 0) != 0:
            self.frame_actual += anim_fps*dt
            if self.frame_actual >= len(self.frames):
                self.frame_actual = 0
        else:
            self.frame_actual = 0  # opcional: poner frame idle

        # Seleccionar frame
        frame = self.frames[int(self.frame_actual)]

    # Flip según dirección
        if not getattr(self, 'facing_right', True):
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame

        # Actualizar timers
        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0.0:
                self.invulnerable_timer = 0.0
                self.invulnerable = False

    def clamp_to_world(self):
        """Evita que el jugador salga de los límites del mundo (no solo de la pantalla)."""
        if self.rect.left < 120:
            self.rect.left = 120
        if self.rect.right > self.world_width:
            self.rect.right = self.world_width

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
