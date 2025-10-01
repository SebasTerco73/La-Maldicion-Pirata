import pygame
import sys
from src.utils.constants import MENU_CONFIG, IMAGES_PATH, FONTS_PATH
from src.utils.resource_manager import ResourceManager

class Scene:
    """Clase base para todas las pantallas del juego (menú, nivel, pausa, etc.)"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.resource_manager = ResourceManager.get_instance()
        self.font = self.load_font()
        self.text_font = self.load_font(size=14)
        
        # Cursor personalizado
        self.cursor_img = self.resource_manager.load_image(f"{IMAGES_PATH}/mouse.png")
        self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))
        pygame.mouse.set_visible(False)
        self.mouse_visible = True

    def load_font(self, size: int = MENU_CONFIG["FONT_SIZE"]) -> pygame.font.Font:
        """Carga una fuente con el tamaño especificado.
        
        Args:
            size: Tamaño de la fuente en puntos
            
        Returns:
            La fuente cargada
        """
        try:
            return self.resource_manager.load_font(f"{FONTS_PATH}/main_font.ttf", size)
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
