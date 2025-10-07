"""
Sistema de UI del juego.
Proporciona componentes reutilizables para la interfaz de usuario.
"""
from typing import Tuple, Optional, Callable
import pygame
from ..utils.constants import Colors
from ..utils.resource_manager import ResourceManager

class UIElement:
    """Clase base para elementos de UI."""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el elemento en la superficie."""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Maneja eventos para el elemento.
        
        Returns:
            bool: True si el evento fue manejado
        """
        return False

class Button(UIElement):
    """Botón interactivo con texto."""
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 font: pygame.font.Font, text_color: Tuple[int, int, int] = Colors.WHITE,
                 bg_color: Optional[Tuple[int, int, int]] = None,
                 hover_color: Optional[Tuple[int, int, int]] = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color or (
            tuple(max(0, c - 30) for c in bg_color) if bg_color else None
        )
        self.hovered = False
        self.click_handler: Optional[Callable[[], None]] = None
        
        # Renderizar texto
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def set_click_handler(self, handler: Callable[[], None]) -> None:
        """Establece el manejador de clic para el botón."""
        self.click_handler = handler

    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el botón en la superficie."""
        if not self.visible:
            return

        # Dibujar fondo
        if self.bg_color:
            color = self.hover_color if self.hovered else self.bg_color
            pygame.draw.rect(surface, color, self.rect)

        # Dibujar texto
        surface.blit(self.text_surface, self.text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Maneja eventos del botón."""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            return self.hovered

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.click_handler:
                self.click_handler()
                return True

        return False

class Label(UIElement):
    """Etiqueta de texto."""
    def __init__(self, x: int, y: int, text: str, font: pygame.font.Font,
                 color: Tuple[int, int, int] = Colors.WHITE):
        self.text = text
        self.font = font
        self.color = color
        self.text_surface = self.font.render(text, True, color)
        super().__init__(x, y, self.text_surface.get_width(),
                        self.text_surface.get_height())

    def set_text(self, text: str) -> None:
        """Actualiza el texto de la etiqueta."""
        self.text = text
        self.text_surface = self.font.render(text, True, self.color)
        self.rect.width = self.text_surface.get_width()
        self.rect.height = self.text_surface.get_height()

    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja la etiqueta en la superficie."""
        if self.visible:
            surface.blit(self.text_surface, self.rect)

class Cursor(UIElement):
    """Cursor personalizado."""
    def __init__(self):
        super().__init__(0, 0, 32, 32)
        self.resource_manager = ResourceManager.get_instance()
        self.cursor_img = self.resource_manager.load_image("assets/images/mouse.png")
        self.cursor_img = pygame.transform.scale(self.cursor_img, (32, 32))

    def update(self) -> None:
        """Actualiza la posición del cursor."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.topleft = (mouse_x, mouse_y)

    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el cursor en la superficie."""
        if self.visible:
            surface.blit(self.cursor_img, self.rect)