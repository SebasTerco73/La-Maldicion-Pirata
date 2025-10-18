# lvl1.py
import random
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGES_LVL1, SOUNDS_LVL1, LVL1_GROUND_Y, WHITE
from .scene import Scene
from characters.player import Player
from characters.crab import Crab 

class Level1(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(IMAGES_LVL1["level1_bg"]).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Sistema de desplazamiento infinito del fondo
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.bg_scroll_speed = 50
        self.mouse_visible = False
        
        self.init_audio()
        self.reset_level() # Usar reset_level para la configuración inicial
        self.player_last_y = 0 # Añadir esta línea

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state != "playing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_level()
                elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                    pygame.mixer.music.stop()
                    if hasattr(self, "sfx_thunder"):
                        self.sfx_thunder.stop()
                    self.running = False

    def update(self, dt):
        if self.state != "playing":
            return

        # Actualizar fondo
        self.bg_x1 -= self.bg_scroll_speed * dt
        self.bg_x2 -= self.bg_scroll_speed * dt
        if self.bg_x1 <= -SCREEN_WIDTH: self.bg_x1 = SCREEN_WIDTH
        if self.bg_x2 <= -SCREEN_WIDTH: self.bg_x2 = SCREEN_WIDTH

        # Actualizar sprites
        self.all_sprites.update(dt)
        self.all_crabs.update(dt, self.player)
        
        # Detección de colisiones
        player_is_falling = self.player.rect.y > self.player_last_y
        self.player_last_y = self.player.rect.y

        player_mask = pygame.mask.from_surface(self.player.image)
        for crab in list(self.all_crabs):
            if not self.player.rect.colliderect(crab.rect):
                continue

            crab_mask = pygame.mask.from_surface(crab.image)
            offset = (crab.rect.x - self.player.rect.x, crab.rect.y - self.player.rect.y)

            if player_mask.overlap(crab_mask, offset):
                # Condición de pisotón mejorada:
                # 1. El jugador está cayendo (su posición 'y' actual es mayor que la anterior).
                # 2. La parte inferior del jugador está muy cerca de la parte superior del cangrejo.
                is_stomp = player_is_falling and abs(self.player.rect.bottom - crab.rect.top) < 15 # Aumentamos un poco el umbral

                if is_stomp:
                    crab.kill()
                    if hasattr(self.player, 'jump'):
                        self.player.jump(strength=-8) 
                else:
                    if hasattr(self.player, 'take_damage'):
                        self.player.take_damage(10)

        # Actualizar temporizador
        time_countdown = 20 - (pygame.time.get_ticks() - self.time_trascurrido) / 1000
        self.time_text = f"{max(0, time_countdown):.0f}"

        # Chequear condiciones de fin de juego
        if getattr(self.player, 'health', 1) <= 0 or time_countdown <= 0:
            self.state = "gameover"
            self.result = "lose"
        elif not self.all_crabs: 
            self.state = "gameover"
            self.result = "win"

    def draw(self):
        # Fondo
        self.screen.blit(self.background, (self.bg_x1, 0))
        self.screen.blit(self.background, (self.bg_x2, 0))
        
        # Sprites
        self.all_sprites.draw(self.screen)
        self.all_crabs.draw(self.screen)
        
        # UI (HUD)
        self.draw_health_bar()
        
        # Dibujar timer (usando el texto calculado en update)
        text_font = self.load_font(size=40)
        time_surface = text_font.render(self.time_text, True, WHITE)
        time_rect = time_surface.get_rect(center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 20))
        self.screen.blit(time_surface, time_rect)
        
        self.draw_cursor()
        
        if self.state != "playing":
            self.draw_end_overlay()

    def init_audio(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(SOUNDS_LVL1["level1_sound"])
        
        self.sfx_thunder = pygame.mixer.Sound(SOUNDS_LVL1["lvl1_sound_Truenos"])
        self.sfx_thunder.set_volume(0.5)
        self.sfx_thunder.play(loops=-1)
        pygame.mixer.music.play(-1)

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def draw_end_overlay(self):
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

        lines = ["R - Reintentar", "M o ESC - Volver al menú"]
        for i, text in enumerate(lines):
            surf = info_font.render(text, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30 + i * 36))
            self.screen.blit(surf, rect)

    def reset_level(self):
        # Estado de juego
        self.state = "playing"
        self.result = None
        self.time_trascurrido = pygame.time.get_ticks()
        self.time_text = "20"
        self.player_last_y = 0 # Añadir esta línea

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_crabs = pygame.sprite.Group()

        # Crear jugador y enemigos
        self.player = Player(SCREEN_WIDTH/2 - 140, 0, LVL1_GROUND_Y)
        self.all_sprites.add(self.player)
        for _ in range(10):
            randomPos = random.randint(0, SCREEN_WIDTH - 100)
            crab = Crab(randomPos, LVL1_GROUND_Y)
            self.all_crabs.add(crab)

        # Resetear fondo
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH

    def draw_health_bar(self):
        if not hasattr(self, 'player') or self.player is None: return
        
        bar_width, bar_height, x, y = 220, 22, 20, 20
        max_health = getattr(self.player, 'max_health', 100)
        current = max(0, getattr(self.player, 'health', 0))
        ratio = current / max_health if max_health > 0 else 0

        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, int(bar_width * ratio), bar_height)

        if ratio > 0.6: base_color = (0, 200, 70)
        elif ratio > 0.3: base_color = (230, 200, 0)
        else: base_color = (200, 40, 40)

        if getattr(self.player, 'invulnerable', False) and (pygame.time.get_ticks() // 150) % 2 == 0:
            base_color = (255, 255, 255)

        pygame.draw.rect(self.screen, (50, 50, 50), outline_rect)
        if fill_rect.width > 0:
            pygame.draw.rect(self.screen, base_color, fill_rect)
        pygame.draw.rect(self.screen, WHITE, outline_rect, 2)

        try:
            font = self.load_font(size=20)
            hp_text = f"HP: {int(current)}/{int(max_health)}"
            text_surf = font.render(hp_text, True, WHITE)
            text_rect = text_surf.get_rect(midleft=(x + 8, y + bar_height // 2))
            self.screen.blit(text_surf, text_rect)
        except Exception:
            pass # Fallo silencioso si la fuente no carga
