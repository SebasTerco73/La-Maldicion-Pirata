import pygame
from typing import Tuple, Optional
from utils.resource_manager import ResourceManager
from utils.constants import COLORS, IMAGES_PATH

class Cursor:
    """Gestiona el cursor personalizado del juego."""
    
    def __init__(self, cursor_image_path: str = f"{IMAGES_PATH}/mouse.png"):
        """Inicializa el cursor.
        
        Args:
            cursor_image_path: Ruta a la imagen del cursor.
        """
        self.resource_manager = ResourceManager.get_instance()
        self.cursor_img = self.resource_manager.load_image(cursor_image_path)
        self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))
        self.visible = True
        pygame.mouse.set_visible(False)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el cursor en la pantalla.
        
        Args:
            screen: Superficie donde dibujar el cursor.
        """
        if self.visible:
            pos = pygame.mouse.get_pos()
            screen.blit(self.cursor_img, pos)
    
    def show(self) -> None:
        """Hace visible el cursor personalizado."""
        self.visible = True
        pygame.mouse.set_visible(False)
    
    def hide(self) -> None:
        """Oculta el cursor personalizado."""
        self.visible = False
        pygame.mouse.set_visible(True)