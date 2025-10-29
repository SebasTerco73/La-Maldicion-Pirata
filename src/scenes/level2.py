import random
import pygame
import sys
import settings
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGES_LVL2, SOUNDS_LVL1, LVL1_GROUND_Y,LVL2_GROUND_Y, WHITE
from .scene import Scene
from characters.player import Player
from characters.cannon import Cannon 
from characters.boss import Boss
from .level3 import Level3

class Level2(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.gameover_image = pygame.image.load(IMAGES_LVL2["bg_looes_lvl2"]).convert()
        self.bg_middle_offset = 0  # desplazamiento horizontal acumulado( de la capa media)
        self.bg_middle_speed = 30  # velocidad de desplazamiento hacia la izquierda (px/seg)

        self.bg_front_offset = 0       # desplazamiento horizontal acumulado( de la capa cercana)
        self.bg_front_speed = 60       # velocidad de desplazamiento (px/seg)

        self.level_width = SCREEN_WIDTH * 3
        self.bg_layers = [     
            pygame.image.load(IMAGES_LVL2["bg_far"]).convert_alpha(),
            pygame.image.load(IMAGES_LVL2["bg_middle"]).convert_alpha(),
            pygame.image.load(IMAGES_LVL2["bg_near"]).convert_alpha(),
            pygame.image.load(IMAGES_LVL2["bg_front"]).convert_alpha()
            # pygame.image.load(IMAGES_LVL1["level1_bg"]).convert()
        ]
        # Sistema de desplazamiento infinito del fondo

        self.bg_layers = [pygame.transform.scale(bg, (self.level_width, SCREEN_HEIGHT)) for bg in self.bg_layers]
        self.camera_x = 0
        self.bg_x1 = 0
        self.bg_x2 = SCREEN_WIDTH
        self.bg_scroll_speed = 50
        self.mouse_visible = False
        
        self.init_audio()

        self.sound_lose = pygame.mixer.Sound(SOUNDS_LVL1["lvl_lose"])
        self.sound_win = pygame.mixer.Sound(SOUNDS_LVL1["lvl_win"])
        self.reset_level() # Usar reset_level para la configuración inicial
        self.player_last_y = 0
        self.pause_start_time = 0 # Para registrar cuándo se inicia la pausa

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Lógica de Pausa (con la tecla P)
                if event.key == pygame.K_p:
                    if self.state == "playing":
                        self.state = "paused"
                        self.pause_start_time = pygame.time.get_ticks() # Guardar tiempo de inicio de pausa
                        pygame.mixer.music.pause()
                        self.sfx_thunder.stop()
                    elif self.state == "paused":
                        # Calcular duración de la pausa y ajustarla al tiempo total transcurrido
                        pause_duration = pygame.time.get_ticks() - self.pause_start_time
                        self.time_trascurrido += pause_duration
                        
                        self.state = "playing"
                        pygame.mixer.music.unpause()
                        self.sfx_thunder.play(loops=-1)

                # Lógica de fin de juego y menú

                if self.state == "gameover":
                    if event.key == pygame.K_RETURN and self.result == "win":
                        self.running = False  # Avanza al siguiente nivel
                    elif event.key == pygame.K_r:
                        self.reset_level()
                    elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                        pygame.mixer.music.stop()
                        if hasattr(self, "sfx_thunder"):
                            self.sfx_thunder.stop()
                        self.running = False
                # Salir al menú desde la pausa
                elif self.state == "paused" and event.key in (pygame.K_ESCAPE, pygame.K_m):
                    pygame.mixer.music.stop()
                    self.running = False

    def update(self, dt):
        # Si el juego está en pausa o terminado, no se actualiza la lógica
        if self.state != "playing":
            return

        #camara
        self.camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(self.camera_x, self.level_width - SCREEN_WIDTH))
        
        # Movimiento automático de la capa del medio hacia la izquierda
        self.bg_middle_offset -= self.bg_middle_speed * dt

        # Reiniciar cuando el desplazamiento es muy grande (para evitar overflow)
        if self.bg_middle_offset <= -self.level_width:
            self.bg_middle_offset = 0

              
        """Esto hace que la capa se desplace 
        continuamente hacia la izquierda y vuelva a 
        empezar cuando se haya movido un ancho completo."""
        # Movimiento automático de la capa del frente (de derecha a izquierda)
        self.bg_front_offset -= self.bg_front_speed * dt
        if self.bg_front_offset <= -self.level_width:
            self.bg_front_offset = 0
        
        # Actualizar sprites
        self.all_sprites.update(dt)
        self.all_cannons.update(dt, self.player)
        self.group_boss.update(dt, self.player)
     
            # --- Movimiento y orientación del jefe ---
        for boss in self.group_boss:
            # Movimiento de derecha a izquierda
            boss.rect.x += boss.speed_x * dt

            # Cambiar dirección si llega a los bordes
            if boss.rect.right >= self.level_width or boss.rect.left <= 0:
                boss.speed_x *= -1  # invertir dirección

            # Hacer que el jefe mire al jugador
            if boss.rect.centerx < self.player.rect.centerx:
                boss.image = pygame.transform.flip(boss.original_image, True, False)
            else:
                boss.image = boss.original_image

        # Detección de colisiones
        player_velocity_y = self.player.rect.y - self.player_last_y
        player_is_falling = self.player.rect.y > self.player_last_y
        self.player_last_y = self.player.rect.y

        # Activar invulnerabilidad mientras cae
        self.player.invulnerable_from_jump = player_is_falling

        # Creamos la máscara del jugador para detección precisa
        player_mask = pygame.mask.from_surface(self.player.image)
        stomped_this_frame = False  # Para saltar solo una vez aunque haya varios cangrejos

        for cannon in list(self.all_cannons):
            if not self.player.rect.colliderect(cannon.rect):
                continue

            cannon_mask = pygame.mask.from_surface(cannon.image)
            offset = (cannon.rect.x - self.player.rect.x, cannon.rect.y - self.player.rect.y)

            if player_mask.overlap(cannon_mask, offset):
                stomp_threshold = max(15, player_velocity_y * 1.5)
                is_stomp = player_is_falling and (self.player.rect.bottom - cannon.rect.top) < stomp_threshold

                if is_stomp:
                    cannon.kill()
                    if not stomped_this_frame and hasattr(self.player, 'jump'):
                        stomped_this_frame = True

                else:
                    # Si el jugador no lo pisa, recibe daño
                    if hasattr(self.player, 'take_damage'):
                        self.player.take_damage(10, knockback_strength=20,source_x=cannon.rect.centerx)

        # Quitar invulnerabilidad al tocar el suelo
        if self.player.rect.bottom >= LVL2_GROUND_Y:
            self.player.invulnerable_from_jump = False

        # Actualizar temporizador
        time_countdown = 60 - (pygame.time.get_ticks() - self.time_trascurrido) / 1000
        self.time_text = f"{max(0, time_countdown):.0f}"
        keys = pygame.key.get_pressed()
        #---flg_sound_died--------------------------------------------------
        if not hasattr(self, 'sound_died_played'):
            self.sound_died_played = False
        #---------------------------------------------------------------
         #---flg_sound_win---------------------------------------------------
        if not hasattr(self, 'sound_win_played'):
            self.sound_win_played = False
        #-------------------------------------------------------------------

        # Chequear condiciones de fin de juego
        if getattr(self.player, 'health', 1) <= 0 or time_countdown <= 0 or keys[pygame.K_l]:
            self.state = "gameover"
            #---------flag_sound_died-------------------------------------------------
            if not self.sound_died_played:
                self.sound_lose.play()
                self.sound_died_played = True
            #---------------------------------------------------------------------
            self.result = "lose"
        elif not self.all_cannons or keys[pygame.K_q]: 
            self.state = "gameover"
            #---------flag_sound_win--------------------------------------------------------
            if not self.sound_win_played:
                self.sound_win.play()
                self.sound_win_played = True
            #-----------------------------------------------------------------------
             
            self.result = "win"

    def draw(self):
        # Fondo
        for i, bg in enumerate(self.bg_layers):
            parallax_factor = 0.2 + i * 0.4  # 0.2, 0.6, 1.0
            bg_x = -self.camera_x * parallax_factor

            # Si es la capa cercana (índice 2), aplicamos desplazamiento extra
            if i == 1:
                bg_x += self.bg_middle_offset

                        # Movimiento constante hacia la izquierda para la capa frontal
            if i == 3:  # índice 3 = nueva capa frontal
                bg_x += self.bg_front_offset
                # Dibujar dos veces para efecto de loop infinito
                self.screen.blit(bg, (bg_x, 0))
                self.screen.blit(bg, (bg_x + self.level_width, 0))
                continue  # ya dibujamos esta capa, pasar a la siguiente

            self.screen.blit(bg, (bg_x, 0))# Dibujar las demás capas normales

         # Dibujar sprites desplazados por cámara
      
 
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))
        for crab in self.all_cannons:
            self.screen.blit(crab.image, (crab.rect.x - self.camera_x, crab.rect.y))
        for sprite in self.group_boss:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))
        # UI (HUD)
        self.draw_health_bar()
        # Mostrar puntaje
        self.draw_score()
        
        # Dibujar timer (usando el texto calculado en update)
        text_font = self.load_font(size=40)
        time_surface = text_font.render(self.time_text, True, WHITE)
        time_rect = time_surface.get_rect(center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 20))
        self.screen.blit(time_surface, time_rect)

        self.draw_cursor()
        
        if self.state == "gameover":
            self.draw_end_overlay()
        elif self.state == "paused":
            self.draw_pause_overlay()

    def init_audio(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(SOUNDS_LVL1["level1_sound"])
        
        self.sfx_thunder = pygame.mixer.Sound(SOUNDS_LVL1["lvl1_sound_Truenos"])
        self.sfx_thunder.set_volume(0.5)
        self.sfx_thunder.play(loops=-1)
        pygame.mixer.music.play(-1)
  
    def draw_end_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        title = settings.TEXTS.get(settings.LANGUAGE, {}).get('end_title_win') if self.result == 'win' else settings.TEXTS.get(settings.LANGUAGE, {}).get('end_title_lose')
        title_color = (0, 200, 70) if self.result == "win" else (200, 40, 40)

        title_font = self.load_font(size=72)
        info_font = self.load_font(size=28)
        if title == "PERDISTE":
            self.screen.blit(self.gameover_image, (0, 0))
        title_surf = title_font.render(title, True, title_color)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(title_surf, title_rect)
        lines = settings.TEXTS.get(settings.LANGUAGE, {}).get('end_lines_lose', ["R - Reintentar", "M o ESC - Volver al menú"])
        lines2 = settings.TEXTS.get(settings.LANGUAGE, {}).get('end_lines_win', ["Enter - Continuar"])
        if self.result == "lose":
            for i, text in enumerate(lines):
                surf = info_font.render(text, True, WHITE)
                rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30 + i * 36))
                self.screen.blit(surf, rect)
        elif self.result == "win":
             for i, text in enumerate(lines2):
                surf = info_font.render(text, True, WHITE)
                rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30 + i * 36))
                self.screen.blit(surf, rect)

    def draw_pause_overlay(self):
        """Dibuja la pantalla de pausa."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        title_font = self.load_font(size=72)
        info_font = self.load_font(size=28)

        title_text = settings.TEXTS.get(settings.LANGUAGE, {}).get('pause_title', 'PAUSA')
        title_surf = title_font.render(title_text, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(title_surf, title_rect)
        lines = settings.TEXTS.get(settings.LANGUAGE, {}).get('pause_lines', ["P - Continuar", "M o ESC - Volver al menú"])
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
        self.player_last_y = 0
        self.pause_start_time = 0 # Resetear el tiempo de pausa
        self.sound_died_played = False #sonido de muerte
        self.sound_win_played = False #sonido victoria

        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_cannons = pygame.sprite.Group()
        self.group_boss = pygame.sprite.Group()
        # Reiniciar puntaje
        self.score = 0

        # Crear jugador y enemigos
        # self.player = Player(SCREEN_WIDTH/2 - 140, 0, LVL1_GROUND_Y)
        self.player = Player(SCREEN_WIDTH/2 - 140, 0, LVL1_GROUND_Y, world_width=self.level_width)
        self.all_sprites.add(self.player)
        self.boss = Boss(LVL2_GROUND_Y)
        self.group_boss.add(self.boss)

        
        for _ in range(30):
            #randomPos = random.randint(0, SCREEN_WIDTH - 100)
            # randomPos = random.randint(200, SCREEN_WIDTH*3)
            randomPos = random.randint(900, self.level_width)
            cannon = Cannon(randomPos, LVL1_GROUND_Y)
            try:
                cannon.scene = self
            except Exception:
                pass
            self.all_cannons.add(cannon)

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
        
    def play_start_animation(self):
        
            clock = pygame.time.Clock()

            # Cargar frames
            frames = [
                pygame.image.load(path).convert_alpha()
                for path in IMAGES_LVL2["start_anim_frames"]
            ]
            frames = [
                pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in frames
            ]

            frame_duration = 80  # milisegundos por frame (0.25 seg)
            current_frame = 0
            last_update = pygame.time.get_ticks()

    

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                now = pygame.time.get_ticks()
                if now - last_update > frame_duration:
                    current_frame += 1
                    last_update = now
                    if current_frame >= len(frames):
                        running = False  # termina animación

                if current_frame < len(frames):
                    self.screen.blit(frames[current_frame], (0, 0))
                pygame.display.flip()
                clock.tick(60)
        
    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
        # Acumular puntaje local al puntaje global antes de cambiar de escena
        try:
            settings.GLOBAL_SCORE += getattr(self, 'score', 0)
        except Exception:
            pass
        self.play_start_animation()
        level3 = Level3(self.screen)
        level3.run()