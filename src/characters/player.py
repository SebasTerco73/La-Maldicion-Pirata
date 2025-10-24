# player.py
import pygame
from settings import IMAGES, SCREEN_WIDTH, SOUNDS_PLAYER
from .character import Character
from .events import GameEvents, EventSystem  # Use relative import if events.py is in the same directory

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, ground_y, world_width=None, restriction_x=0):
        super().__init__()
        spritesheet = pygame.image.load(IMAGES["player-walk"]).convert_alpha()
        spritesheet_jump = pygame.image.load(IMAGES["player-jump"]).convert_alpha()      

        self.frames = self.extraer_frames(spritesheet, cols=8, rows=1, scale=(100,100))
        self.frames_jump = self.extraer_frames(spritesheet_jump, cols=7, rows=1, scale=(100,100))
        
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.frames_jump_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_jump]

        self.sound_jump = pygame.mixer.Sound(SOUNDS_PLAYER["player_sound_jump"])

        self.frame_actual = 0.0  # índice del frame
        # No se usa pantalla.blit(...) porque Level1.draw() ya hace self.screen.blit(sprite.image, ...) para todos los sprites.
        self.image = self.frames[int(self.frame_actual)]
        self.rect = self.image.get_rect(topleft=(x, y))
        # Cambio de direccion
        self.facing = 1
        self.vel_y = 0
        self.restriction = restriction_x
        self.speed = 200
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
        self.invulnerable_from_hit = False
        self.invulnerable_duration = 1.0
        # Sistema de eventos (opcional). Si no se pasa uno externo, creamos uno local
        self.event_system = EventSystem()

    def extraer_frames(self, sheet, cols, rows, scale=None):
        frames = []
        w, h = sheet.get_size()
        frame_w = w / cols   # usar división flotante, no //
        frame_h = h / rows

        for y in range(rows):
            for x in range(cols):
                # redondear posiciones y tamaños
                rect = pygame.Rect(round(x * frame_w),round(y * frame_h),round(frame_w),round(frame_h))
                frame = sheet.subsurface(rect).copy()
                if scale:
                    frame = pygame.transform.smoothscale(frame, scale)
                frames.append(frame)
        return frames
        
    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        # Cambiamos dirección y, si la dirección cambió, resetear el frame para girar inmediato
            if self.facing != -1:
                self.facing = -1
                self.frame_actual = 0.0

            dx = -1
            # avanzar animación
            self.frame_actual += 0.15
            if self.frame_actual >= len(self.frames_left):
                self.frame_actual = 0.0
            # ASIGNAR siempre la imagen, no sólo en el "wrap"
            self.image = self.frames_left[int(self.frame_actual)]

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            # Cambiamos dirección y resetear frame si veníamos hacia la izquierda
            if self.facing != 1:
                self.facing = 1
                self.frame_actual = 0.0

            dx = 1
            self.frame_actual += 0.15
            if self.frame_actual >= len(self.frames):
                self.frame_actual = 0.0
            self.image = self.frames[int(self.frame_actual)]

        else:
            # Quieto: opcionalmente dejar el primer frame o el último
            # Si querés que quede en el último frame mostrado, comentá la línea que resetea frame_actual.
            self.frame_actual = 0.0
            # Elegí la lista según la última dirección para que mire hacia donde corresponda
            self.image = (self.frames if self.facing == 1 else self.frames_left)[int(self.frame_actual)]

        self.rect.x += dx * self.speed * dt

        # --- Salto ---
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.sound_jump.play()
            self.vel_y = self.jump_strength
            self.on_ground = False
        
        # --- Animación de salto ---
        if not self.on_ground:
            # elegir la lista de salto correcta según dirección
            frames_jump = self.frames_jump if self.facing == 1 else self.frames_jump_left
            # podés animarlo o dejar un frame fijo si querés
            self.frame_actual += 0.1
            if self.frame_actual >= len(frames_jump):
                self.frame_actual = len(frames_jump) - 1  # último frame (en el aire)
            self.image = frames_jump[int(self.frame_actual)]
        
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
     
        # Actualizar timers
        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0.0:
                self.invulnerable_timer = 0.0
                self.invulnerable_from_hit = False
                self.invulnerable = False

    def clamp_to_world(self):
        """Evita que el jugador salga de los límites del mundo (no solo de la pantalla)."""
        if self.rect.left < self.restriction:
            self.rect.left = self.restriction
        if self.rect.right > self.world_width:
            self.rect.right = self.world_width

    @property
    def is_falling(self):
        return self.vel_y > 0 and not self.on_ground

    def take_damage(self, amount, knockback_strength=0, source_x=None):
    
        if amount <= 0:
            return
        if self.invulnerable_from_hit:
            return
        # No aplicar daño si está invulnerable
        if getattr(self, 'invulnerable_from_hit', False):
            return

        # Restar vida
        self.health = max(0, self.health - amount)
        # Activar invulnerabilidad temporal
        

        # Activar invulnerabilidad temporal
        self.invulnerable_from_hit = True
        self.invulnerable_timer = self.invulnerable_duration  # 1 segundo por defecto
        self.invulnerable = True  # <-- para parpadeo visual    
        # Knockback (si se indica)
        if knockback_strength and source_x is not None:
            if self.rect.centerx < source_x:
                self.rect.x -= knockback_strength  # retrocede a la izquierda
            else:
                self.rect.x += knockback_strength  # retrocede a la derecha

        # Emitir evento de daño si existe
        if hasattr(self, 'event_system') and hasattr(self.event_system, 'emit'):
            try:
                self.event_system.emit(GameEvents.PLAYER_DAMAGE, damage=amount)
            except Exception:
                pass

        # Chequear si murió
        if self.health <= 0:
            self.health = 0
            if hasattr(self, 'event_system') and hasattr(self.event_system, 'emit'):
                try:
                    self.event_system.emit(GameEvents.PLAYER_DEATH)
                except Exception:
                    pass

