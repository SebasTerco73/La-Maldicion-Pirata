import pygame
import sys
import settings
from settings import FONTS, MENU_FONT_SIZE, IMAGES, SCREEN_WIDTH


# Padre de todas las pantallas, menu, nivel, pausa, etc
class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font = self.load_font()
        self.text_font = self.load_font(size=14)
        # Contador de puntaje (por enemigos derrotados). Cada nivel reinicia esto en su reset_level.
        self.score = 0
        
        # --- Cursor personalizado (global para todas las escenas) ---
        self.cursor_img = pygame.image.load(IMAGES["cursor"]).convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))  # tamaño recomendado
        pygame.mouse.set_visible(False)  # ocultar el cursor del sistema
        self.mouse_visible = True
        # ------------------------------------------------------------

    def load_font(self, size=MENU_FONT_SIZE):
        # Si el idioma actual es chino (zh) y se dispone de una fuente CJK, usarla
        try:
            if getattr(settings, 'LANGUAGE', 'es') == 'zh' and 'NotoSansCJKBold' in FONTS:
                return pygame.font.Font(FONTS['NotoSansCJKBold'], size)
            return pygame.font.Font(FONTS["main_font"], size)
        except FileNotFoundError:
            try:
                return pygame.font.SysFont("Arial", size)
            except:
                return pygame.font.Font(None, size)

    def handle_global_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_RETURN and (pygame.key.get_mods() & pygame.KMOD_ALT):
                pygame.display.toggle_fullscreen()

# pygame.key.get_mods() devuelve un número entero que representa todas las teclas modificadoras que están presionadas en ese momento.
# Las teclas modificadoras incluyen: Shift, Ctrl, Alt, Meta, etc.
# El operador & es un AND a nivel de bits. Compara el valor de get_mods() con la constante pygame.KMOD_ALT (que representa la tecla Alt).
# Si el resultado es distinto de cero, significa que Alt está siendo presionado.

    def draw_cursor(self):
        # Dibuja el cursor en la posición actual del mouse.
        if self.mouse_visible:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(self.cursor_img, (mouse_x, mouse_y))

    def draw_score(self):
        """Dibuja el contador de puntos en la UI (si existe)."""
        try:
            font = self.load_font(size=20)
            # Etiquetas localizadas
            texts = settings.TEXTS.get(settings.LANGUAGE, {})
            score_label = texts.get('score_label', 'Score')
            global_label = texts.get('global_score_label', 'Total')

            local_score = getattr(self, 'score', 0)
            global_score = getattr(settings, 'GLOBAL_SCORE', 0)

            # Posicionar debajo de la barra de vida (x=20,y=20, altura=22)
            health_x, health_y, health_h = 20, 20, 22
            local_surf = font.render(f"{score_label}: {local_score}", True, (255, 215, 0))
            global_surf = font.render(f"{global_label}: {global_score}", True, (200, 200, 200))

            local_rect = local_surf.get_rect(topleft=(health_x + 8, health_y + health_h + 6))
            global_rect = global_surf.get_rect(topleft=(health_x + 8, health_y + health_h + 6 + local_rect.height + 4))

            self.screen.blit(local_surf, local_rect)
            self.screen.blit(global_surf, global_rect)
        except Exception:
            # No bloquear el juego si la fuente falla
            pass
