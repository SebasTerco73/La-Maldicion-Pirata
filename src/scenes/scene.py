import pygame
import sys
from settings import FONTS, MENU_FONT_SIZE, IMAGES

# Padre de todas las pantallas, menu, nivel, pausa, etc
class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font = self.load_font()
        self.text_font = self.load_font(size=14) 
          # --- Cursor personalizado (global para todas las escenas) ---
        self.cursor_img = pygame.image.load(IMAGES["cursor"]).convert_alpha()
        self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))  # tamaño recomendado
        pygame.mouse.set_visible(False)  # ocultar el cursor del sistema
        self.mouse_visible = True
        # ------------------------------------------------------------

    def load_font(self, size=MENU_FONT_SIZE):
        try:
            return pygame.font.Font(FONTS["main_font"], size)
        except FileNotFoundError:
            try:
                return pygame.font.SysFont("Arial", size)
            except:
                return pygame.font.Font(None, size)

    def handle_global_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
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
