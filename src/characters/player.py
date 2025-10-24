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

        self.knockback_vel_x = 0
        self.knockback_duration = 0

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
        self.invulnerable = False
        self.invulnerable_time = 1000  # milisegundos (1 segundo)
        self.last_hit_time = 0

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
        """Aplica daño al jugador y activa la invulnerabilidad temporal."""
        if amount <= 0 or self.invulnerable:
            return

        # Aplicar daño
        self.health = max(0, self.health - amount)
        print(f"💥 Daño recibido! Salud: {self.health}")

        # Activar invulnerabilidad
        self.invulnerable = True
        self.last_hit_time = pygame.time.get_ticks()  # tiempo actual en ms
        self.image.set_alpha(128)  # semitransparente (feedback visual)

        # Knockback (retroceso al ser golpeado)
        if knockback_strength and source_x is not None:
            direction = -1 if self.rect.centerx < source_x else 1
            self.knockback_vel_x = direction * knockback_strength  # velocidad de retroceso
            self.knockback_duration = 0.2  # segundos de retroceso


        # Emitir evento opcional
        if hasattr(self, 'event_system') and hasattr(self.event_system, 'emit'):
            try:
                self.event_system.emit(GameEvents.PLAYER_DAMAGE, damage=amount)
            except Exception:
                pass

        # Si muere
        if self.health <= 0:
            self.health = 0
            if hasattr(self, 'event_system') and hasattr(self.event_system, 'emit'):
                try:
                    self.event_system.emit(GameEvents.PLAYER_DEATH)
                except Exception:
                    pass

    def update(self, dt):
        """Actualiza movimiento, gravedad e invulnerabilidad."""
        self.handle_input(dt)
        self.clamp_to_world()
        self.apply_gravity(dt)

        if self.knockback_duration > 0:
            self.rect.x += self.knockback_vel_x * dt
            self.knockback_duration -= dt
            if self.knockback_duration <= 0:
                self.knockback_vel_x = 0
        else:
            self.handle_input(dt)

        self.clamp_to_world()
        self.apply_gravity(dt)

        # --- Control de invulnerabilidad ---
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time >= self.invulnerable_time:
                self.invulnerable = False
                self.image.set_alpha(255)
            else:
                alpha = 128 if (current_time // 100) % 2 == 0 else 255
                self.image.set_alpha(alpha)


