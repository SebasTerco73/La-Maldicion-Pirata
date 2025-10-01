import pygame
from typing import Tuple
from physics.gravity import PhysicsEntity
from utils.resource_manager import ResourceManager
from utils.constants import PLAYER_CONFIG, SCREEN_WIDTH, SCREEN_HEIGHT

class Character(pygame.sprite.Sprite, PhysicsEntity):
    def __init__(self, image_path: str, x: float, y: float, 
                 width: int = PLAYER_CONFIG["WIDTH"], 
                 height: int = PLAYER_CONFIG["HEIGHT"], 
                 speed: float = PLAYER_CONFIG["SPEED"]):
        """Inicializa un personaje del juego.
        
        Args:
            image_path: Ruta a la imagen del personaje
            x: Posición inicial X
            y: Posición inicial Y
            width: Ancho del sprite
            height: Alto del sprite
            speed: Velocidad de movimiento
        """
        pygame.sprite.Sprite.__init__(self)
        PhysicsEntity.__init__(self)
        
        # Cargar y escalar sprite usando ResourceManager
        resource_manager = ResourceManager.get_instance()
        self.image = resource_manager.load_image(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.speed = speed
        self.facing_right = True

    def move(self, dx: float, dy: float) -> None:
        """Mueve al personaje en una dirección.
        
        Args:
            dx: Desplazamiento en X
            dy: Desplazamiento en Y
        """
        # Actualizar velocidad
        self.velocity.x = dx * self.speed
        self.velocity.y = dy * self.speed
        
        # Actualizar posición
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Actualizar dirección
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

    def clamp_to_screen(self) -> None:
        """Mantiene al personaje dentro de la pantalla."""
        self.rect.x = max(-50, min(self.rect.x, SCREEN_WIDTH - self.rect.width + 20))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height + 10))

    def get_position(self) -> Tuple[float, float]:
        """Obtiene la posición actual del personaje.
        
        Returns:
            Tupla con las coordenadas (x, y)
        """
        return self.rect.x, self.rect.y

    def update(self, dt: float) -> None:
        """Actualiza el estado del personaje.
        
        Args:
            dt: Tiempo transcurrido desde el último update
        """
        # Aplicar física
        self.velocity += self.acceleration * dt
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
        
        # Restablecer aceleración
        self.acceleration.x = 0
        self.acceleration.y = 0
        
        # Mantener dentro de la pantalla
        self.clamp_to_screen()