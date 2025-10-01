import pygame
from typing import List, Tuple, Callable, Optional
from utils.resource_manager import ResourceManager
from utils.constants import COLORS, MENU_CONFIG, FONTS_PATH

class MenuItem:
    """Representa un elemento del menú."""
    
    def __init__(self, text: str, action: Callable, position: Tuple[int, int],
                 font_size: int = MENU_CONFIG["FONT_SIZE"],
                 color: Tuple[int, int, int] = COLORS["WHITE"],
                 hover_color: Tuple[int, int, int] = COLORS["BLUE"]):
        """Inicializa un elemento del menú.
        
        Args:
            text: Texto del elemento.
            action: Función a ejecutar cuando se seleccione el elemento.
            position: Posición (x, y) del elemento en la pantalla.
            font_size: Tamaño de la fuente.
            color: Color normal del texto.
            hover_color: Color del texto cuando el ratón está encima.
        """
        self.text = text
        self.action = action
        self.position = position
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
        self.resource_manager = ResourceManager.get_instance()
        self.font = self.resource_manager.load_font(f"{FONTS_PATH}/main_font.ttf", font_size)
        self.render()
    
    def render(self) -> None:
        """Renderiza el texto del elemento."""
        color = self.hover_color if self.is_hovered else self.color
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect(center=self.position)
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Actualiza el estado del elemento.
        
        Args:
            mouse_pos: Posición actual del ratón.
        """
        prev_hover = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if prev_hover != self.is_hovered:
            self.render()
    
    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el elemento en la pantalla.
        
        Args:
            screen: Superficie donde dibujar el elemento.
        """
        screen.blit(self.image, self.rect)
    
    def handle_click(self) -> None:
        """Maneja el clic en el elemento."""
        if self.is_hovered:
            self.action()

class Menu:
    """Gestiona un menú con múltiples elementos."""
    
    def __init__(self, screen: pygame.Surface):
        """Inicializa el menú.
        
        Args:
            screen: Superficie donde se dibujará el menú.
        """
        self.screen = screen
        self.items: List[MenuItem] = []
        self.background: Optional[pygame.Surface] = None
        
    def set_background(self, image_path: str) -> None:
        """Establece la imagen de fondo del menú.
        
        Args:
            image_path: Ruta a la imagen de fondo.
        """
        self.resource_manager = ResourceManager.get_instance()
        self.background = self.resource_manager.load_image(image_path)
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
    
    def add_item(self, item: MenuItem) -> None:
        """Añade un elemento al menú.
        
        Args:
            item: Elemento a añadir.
        """
        self.items.append(item)
    
    def update(self) -> None:
        """Actualiza todos los elementos del menú."""
        mouse_pos = pygame.mouse.get_pos()
        for item in self.items:
            item.update(mouse_pos)
    
    def draw(self) -> None:
        """Dibuja el menú y todos sus elementos."""
        if self.background:
            self.screen.blit(self.background, (0, 0))
            
        for item in self.items:
            item.draw(self.screen)
    
    def handle_click(self) -> None:
        """Maneja los clics en los elementos del menú."""
        for item in self.items:
            item.handle_click()