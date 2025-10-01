import pygame
import logging
from typing import Dict, Any, Optional

class ResourceNotFoundError(Exception):
    """Excepción lanzada cuando no se puede cargar un recurso."""
    pass

class ResourceManager:
    """Gestor de recursos del juego (imágenes, sonidos, fuentes)."""
    
    _instance: Optional['ResourceManager'] = None
    
    def __init__(self):
        """Inicializa el gestor de recursos."""
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[tuple, pygame.font.Font] = {}
        self.logger = logging.getLogger(__name__)
        
    @classmethod
    def get_instance(cls) -> 'ResourceManager':
        """Obtiene la instancia única del gestor de recursos (patrón Singleton)."""
        if cls._instance is None:
            cls._instance = ResourceManager()
        return cls._instance
    
    def load_image(self, path: str) -> pygame.Surface:
        """Carga una imagen desde el disco o la devuelve desde la caché.
        
        Args:
            path: Ruta al archivo de imagen.
            
        Returns:
            pygame.Surface: La imagen cargada.
            
        Raises:
            ResourceNotFoundError: Si no se puede cargar la imagen.
        """
        try:
            if path not in self._images:
                self.logger.info(f"Cargando imagen: {path}")
                self._images[path] = pygame.image.load(path).convert_alpha()
            return self._images[path]
        except pygame.error as e:
            self.logger.error(f"Error al cargar imagen {path}: {e}")
            raise ResourceNotFoundError(f"No se pudo cargar la imagen: {path}")
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """Carga un sonido desde el disco o lo devuelve desde la caché.
        
        Args:
            path: Ruta al archivo de sonido.
            
        Returns:
            pygame.mixer.Sound: El sonido cargado.
            
        Raises:
            ResourceNotFoundError: Si no se puede cargar el sonido.
        """
        try:
            if path not in self._sounds:
                self.logger.info(f"Cargando sonido: {path}")
                self._sounds[path] = pygame.mixer.Sound(path)
            return self._sounds[path]
        except pygame.error as e:
            self.logger.error(f"Error al cargar sonido {path}: {e}")
            raise ResourceNotFoundError(f"No se pudo cargar el sonido: {path}")
    
    def load_font(self, path: str, size: int) -> pygame.font.Font:
        """Carga una fuente desde el disco o la devuelve desde la caché.
        
        Args:
            path: Ruta al archivo de fuente.
            size: Tamaño de la fuente en puntos.
            
        Returns:
            pygame.font.Font: La fuente cargada.
            
        Raises:
            ResourceNotFoundError: Si no se puede cargar la fuente.
        """
        key = (path, size)
        try:
            if key not in self._fonts:
                self.logger.info(f"Cargando fuente: {path} (tamaño: {size})")
                self._fonts[key] = pygame.font.Font(path, size)
            return self._fonts[key]
        except pygame.error as e:
            self.logger.error(f"Error al cargar fuente {path}: {e}")
            raise ResourceNotFoundError(f"No se pudo cargar la fuente: {path}")
    
    def clear_cache(self):
        """Limpia la caché de recursos."""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()
        self.logger.info("Caché de recursos limpiada")