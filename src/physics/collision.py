from typing import List, Tuple, Optional
import pygame

class CollisionSystem:
    """Sistema que maneja las colisiones entre entidades."""
    
    _instance = None
    
    def __init__(self):
        """Inicializa el sistema de colisiones."""
        self.static_colliders: List[pygame.Rect] = []
    
    @classmethod
    def get_instance(cls) -> 'CollisionSystem':
        """Obtiene la instancia única del sistema de colisiones (patrón Singleton)."""
        if cls._instance is None:
            cls._instance = CollisionSystem()
        return cls._instance
    
    def add_static_collider(self, rect: pygame.Rect) -> None:
        """Añade un colisionador estático al sistema.
        
        Args:
            rect: El rectángulo de colisión a añadir.
        """
        self.static_colliders.append(rect)
    
    def remove_static_collider(self, rect: pygame.Rect) -> None:
        """Elimina un colisionador estático del sistema.
        
        Args:
            rect: El rectángulo de colisión a eliminar.
        """
        if rect in self.static_colliders:
            self.static_colliders.remove(rect)
    
    def check_collision(self, rect: pygame.Rect) -> Optional[pygame.Rect]:
        """Comprueba si hay colisión con algún colisionador estático.
        
        Args:
            rect: El rectángulo a comprobar.
            
        Returns:
            El primer rectángulo con el que colisiona o None si no hay colisión.
        """
        for collider in self.static_colliders:
            if rect.colliderect(collider):
                return collider
        return None
    
    def resolve_collision(self, moving_rect: pygame.Rect, static_rect: pygame.Rect) -> Tuple[float, float]:
        """Resuelve una colisión entre dos rectángulos.
        
        Args:
            moving_rect: El rectángulo en movimiento.
            static_rect: El rectángulo estático.
            
        Returns:
            Una tupla con el desplazamiento necesario en X e Y para resolver la colisión.
        """
        # Calcula la intersección
        intersection = moving_rect.clip(static_rect)
        
        if intersection.width < intersection.height:
            # Colisión horizontal
            if moving_rect.centerx < static_rect.centerx:
                return (-intersection.width, 0)
            else:
                return (intersection.width, 0)
        else:
            # Colisión vertical
            if moving_rect.centery < static_rect.centery:
                return (0, -intersection.height)
            else:
                return (0, intersection.height)
    
    def clear(self) -> None:
        """Limpia todos los colisionadores estáticos."""
        self.static_colliders.clear()