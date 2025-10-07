"""
Gestor de recursos para el juego.
Implementa el patrón Singleton para asegurar una única instancia de gestión de recursos.
"""
import pygame
import logging
from typing import Dict, Optional, Any

class ResourceNotFoundError(Exception):
    """Excepción personalizada para recursos no encontrados."""
    pass

class ResourceManager:
    _instance: Optional['ResourceManager'] = None
    _resources: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance._logger = logging.getLogger(__name__)
        return cls._instance

    @staticmethod
    def get_instance() -> 'ResourceManager':
        """Obtiene la única instancia del ResourceManager."""
        if ResourceManager._instance is None:
            ResourceManager._instance = ResourceManager()
        return ResourceManager._instance

    def load_image(self, path: str) -> pygame.Surface:
        """
        Carga una imagen y la almacena en caché.
        
        Args:
            path: Ruta al archivo de imagen.
            
        Returns:
            Surface de Pygame con la imagen cargada.
            
        Raises:
            ResourceNotFoundError: Si no se puede cargar la imagen.
        """
        try:
            if path not in self._resources:
                self._logger.info(f"Cargando imagen: {path}")
                self._resources[path] = pygame.image.load(path).convert_alpha()
            return self._resources[path]
        except (pygame.error, FileNotFoundError) as e:
            self._logger.error(f"Error al cargar imagen {path}: {str(e)}")
            raise ResourceNotFoundError(f"No se pudo cargar la imagen: {path}")

    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """
        Carga un sonido y lo almacena en caché.
        
        Args:
            path: Ruta al archivo de sonido.
            
        Returns:
            Objeto Sound de Pygame con el sonido cargado.
            
        Raises:
            ResourceNotFoundError: Si no se puede cargar el sonido.
        """
        try:
            if path not in self._resources:
                self._logger.info(f"Cargando sonido: {path}")
                self._resources[path] = pygame.mixer.Sound(path)
            return self._resources[path]
        except (pygame.error, FileNotFoundError) as e:
            self._logger.error(f"Error al cargar sonido {path}: {str(e)}")
            raise ResourceNotFoundError(f"No se pudo cargar el sonido: {path}")

    def clear_cache(self):
        """Limpia la caché de recursos."""
        self._resources.clear()
        self._logger.info("Caché de recursos limpiada")
