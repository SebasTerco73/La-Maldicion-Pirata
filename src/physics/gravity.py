from typing import List, Tuple, Optional
import pygame
from utils.constants import PLAYER_CONFIG

class PhysicsEntity:
    """Clase base para entidades con físicas."""
    
    def __init__(self):
        """Inicializa una entidad con físicas."""
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.acceleration: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.on_ground: bool = False

class GravitySystem:
    """Sistema que aplica gravedad a las entidades físicas."""
    
    _instance = None
    
    def __init__(self, gravity: float = PLAYER_CONFIG["GRAVITY"]):
        """Inicializa el sistema de gravedad.
        
        Args:
            gravity: Fuerza de la gravedad.
        """
        self.gravity = gravity
    
    @classmethod
    def get_instance(cls) -> 'GravitySystem':
        """Obtiene la instancia única del sistema de gravedad (patrón Singleton)."""
        if cls._instance is None:
            cls._instance = GravitySystem()
        return cls._instance
    
    def apply(self, entity: PhysicsEntity) -> None:
        """Aplica la gravedad a una entidad.
        
        Args:
            entity: La entidad a la que aplicar gravedad.
        """
        if not entity.on_ground:
            entity.acceleration.y = self.gravity