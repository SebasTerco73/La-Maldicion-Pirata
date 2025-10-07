"""
Sistema de eventos del juego.
Implementa un sistema de eventos basado en el patrón Observer.
"""
from typing import Dict, List, Callable, Any
import logging

class EventSystem:
    """Sistema de eventos del juego."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventSystem, cls).__new__(cls)
            cls._instance.handlers: Dict[str, List[Callable]] = {} # pyright: ignore[reportInvalidTypeForm]
            cls._instance._logger = logging.getLogger(__name__)
        return cls._instance

    @staticmethod
    def get_instance() -> 'EventSystem':
        """Obtiene la única instancia del sistema de eventos."""
        if EventSystem._instance is None:
            EventSystem._instance = EventSystem()
        return EventSystem._instance

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """
        Suscribe un manejador a un tipo de evento.
        
        Args:
            event_type: Tipo de evento a suscribir
            handler: Función que manejará el evento
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        self._logger.info(f"Nuevo manejador suscrito a: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """
        Desuscribe un manejador de un tipo de evento.
        
        Args:
            event_type: Tipo de evento
            handler: Función manejadora a eliminar
        """
        if event_type in self.handlers:
            try:
                self.handlers[event_type].remove(handler)
                self._logger.info(f"Manejador eliminado de: {event_type}")
            except ValueError:
                self._logger.warning(f"Intento de eliminar manejador no suscrito: {event_type}")

    def emit(self, event_type: str, *args: Any, **kwargs: Any) -> None:
        """
        Emite un evento a todos los manejadores suscritos.
        
        Args:
            event_type: Tipo de evento a emitir
            *args: Argumentos posicionales para los manejadores
            **kwargs: Argumentos nombrados para los manejadores
        """
        if event_type in self.handlers:
            self._logger.debug(f"Emitiendo evento: {event_type}")
            for handler in self.handlers[event_type]:
                try:
                    handler(*args, **kwargs)
                except Exception as e:
                    self._logger.error(f"Error en manejador de evento {event_type}: {str(e)}")

# Tipos de eventos predefinidos
class GameEvents:
    PLAYER_DAMAGE = "player_damage"
    PLAYER_DEATH = "player_death"
    SCORE_CHANGE = "score_change"
    GAME_START = "game_start"
    GAME_PAUSE = "game_pause"
    GAME_RESUME = "game_resume"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"