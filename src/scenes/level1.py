# lvl1.py
import random
import time
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGES_LVL1, SOUNDS_LVL1, LVL1_GROUND_Y, WHITE, FONTS
from .scene import Scene
from characters.player import Player
from characters.crab import Crab 

class Level1(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(IMAGES_LVL1["level1_bg"]).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.time_thunder = 0
        # Sistema de desplazamiento infinito del fondo
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.bg_scroll_speed = 50  # píxeles por segundo (ajustable)
        self.mouse_visible = False
        self.init_audio()
        # Estado de juego
        self.state = "playing"  # playing | gameover
        self.result = None       # 'win' | 'lose' | None
        self.running = True

        # Objetos del nivel
        self.all_sprites = pygame.sprite.Group()
        self.all_crabs = pygame.sprite.Group()
        self.player = Player(SCREEN_WIDTH/2 - 140, 0, LVL1_GROUND_Y)
        self.all_sprites.add(self.player)
        for _ in range(10):
            randomPos = random.randint(0, SCREEN_WIDTH - 100)  # Generar 10 NPCs
            crab = Crab(randomPos, LVL1_GROUND_Y)
            self.all_crabs.add(crab)
        self.time_trascurrido = pygame.time.get_ticks()
            
    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Controles de fin de partida
            if self.state != "playing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_level()
                elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                    # Detener música del nivel antes de volver al menú
                    pygame.mixer.music.stop()
                    # Volver al menú (romper el bucle de run)
                    self.running = False

    def update(self, dt):
        # Si el juego terminó, no actualizar lógicas
        if self.state != "playing":
            return

        # Actualizar desplazamiento del fondo
        self.bg_x1 -= self.bg_scroll_speed * dt
        self.bg_x2 -= self.bg_scroll_speed * dt

        # Resetear posición cuando el fondo sale completamente de pantalla
        if self.bg_x1 <= -SCREEN_WIDTH:
            self.bg_x1 = SCREEN_WIDTH
        if self.bg_x2 <= -SCREEN_WIDTH:
            self.bg_x2 = SCREEN_WIDTH

        self.all_sprites.update(dt)
        # Actualizamos cada cangrejo pasándole el jugador para manejo de colisiones
        for crab in self.all_crabs.sprites():
            # Cada Crab.define update(self, dt, player=None)
            try:
                crab.update(dt, self.player)
            except TypeError:
                # Retrocompatibilidad: si el método no acepta player, llamarlo sin él
                crab.update(dt)

        # Chequear condiciones de fin
        if getattr(self.player, 'health', 1) <= 0:
            self.state = "gameover"
            self.result = "lose"
        elif len(self.all_crabs) == 0:
            self.state = "gameover"
            self.result = "win"

        # Timer en pantalla
        time_init = (pygame.time.get_ticks() - self.time_trascurrido) / 1000
        time_countdown = 20 - time_init
        if time_countdown >= 0:
            time_text = f"{time_countdown:.0f}"
        else:
            time_text = "0"
            
        if time_countdown <= 0:
            self.state = "gameover"
            self.result = "lose"    
        
        self.text_font = self.load_font(size=40)
        self.time_surface = self.text_font.render(time_text, True, WHITE)
        time_rect = self.time_surface.get_rect(center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 20))
        self.screen.blit(self.time_surface, time_rect)

    def draw(self):
        # Dibujar fondo con desplazamiento infinito
        self.screen.blit(self.background, (self.bg_x1, 0))
        self.screen.blit(self.background, (self.bg_x2, 0))
        
        self.all_sprites.draw(self.screen)
        # Dibujar barra de vida del jugador
        self.draw_health_bar()
        self.draw_cursor()
        self.all_crabs.draw(self.screen)
        # Si terminó el juego, dibujar overlay
        if self.state != "playing":
            self.draw_end_overlay()

    def init_audio(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(SOUNDS_LVL1["level1_sound"])
        pygame.mixer.music.play(-1)

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.draw()
            self.handle_events()
            self.update(dt)
            pygame.display.flip()
            self.time_thunder = (pygame.time.get_ticks() - self.time_thunder) / 1000
            if self.time_thunder % 4 > 0 and self.time_thunder % 4 < 0.02:
                pygame.mixer.Sound.play(pygame.mixer.Sound(SOUNDS_LVL1["lvl1_sound_Truenos"]))



    def draw_end_overlay(self):
        # Fondo semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        title = "GANASTE" if self.result == "win" else "PERDISTE"
        title_color = (0, 200, 70) if self.result == "win" else (200, 40, 40)

        title_font = self.load_font(size=72)
        info_font = self.load_font(size=28)

        title_surf = title_font.render(title, True, title_color)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(title_surf, title_rect)

        lines = [
            "R - Reintentar",
            "M o ESC - Volver al menú",
        ]
        for i, text in enumerate(lines):
            surf = info_font.render(text, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30 + i * 36))
            self.screen.blit(surf, rect)

    def reset_level(self):
        # Vaciar grupos
        self.all_sprites.empty()
        self.all_crabs.empty()

        # Crear jugador y enemigos nuevamente
        self.player = Player(SCREEN_WIDTH/2 - 140, 0, LVL1_GROUND_Y)
        self.all_sprites.add(self.player)
        for _ in range(10):
            randomPos = random.randint(0, SCREEN_WIDTH - 100)
            crab = Crab(randomPos, LVL1_GROUND_Y)
            self.all_crabs.add(crab)

        # Resetear estado
        self.state = "playing"
        self.result = None
        self.time_trascurrido = pygame.time.get_ticks()
        # Resetear fondo
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH

    def draw_health_bar(self):
        """Dibuja una barra de vida simple en la esquina superior izquierda."""
        if not hasattr(self, 'player') or self.player is None:
            return
        # Parámetros de la barra
        bar_width = 220
        bar_height = 22
        x, y = 20, 20
        max_health = getattr(self.player, 'max_health', 100)
        current = getattr(self.player, 'health', max_health)
        # Normalizar valores
        if max_health <= 0:
            ratio = 0
        else:
            current = max(0, min(current, max_health))
            ratio = current / max_health

        # Rectángulos
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, int(bar_width * ratio), bar_height)

        # Color por umbral de vida
        if ratio > 0.6:
            base_color = (0, 200, 70)      # Verde
        elif ratio > 0.3:
            base_color = (230, 200, 0)     # Amarillo
        else:
            base_color = (200, 40, 40)     # Rojo

        # Parpadeo cuando está invulnerable
        invul = getattr(self.player, 'invulnerable', False)
        if invul:
            # Alternar color cada ~150ms
            blink = (pygame.time.get_ticks() // 150) % 2 == 0
            if blink:
                base_color = (255, 255, 255)  # Blanco al parpadear

        # Dibujar fondo de la barra (gris oscuro)
        pygame.draw.rect(self.screen, (50, 50, 50), outline_rect)
        # Relleno según la vida (color dinámico)
        if fill_rect.width > 0:
            pygame.draw.rect(self.screen, base_color, fill_rect)
        # Borde blanco
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)

        # Texto de HP
        try:
            font = self.load_font(size=20)
        except Exception:
            font = None
        if font:
            hp_text = f"HP: {int(current)}/{int(max_health)}"
            text_surf = font.render(hp_text, True, WHITE)
            text_rect = text_surf.get_rect(midleft=(x + 8, y + bar_height // 2))
            self.screen.blit(text_surf, text_rect)
