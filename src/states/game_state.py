"""
Sistema de estados del juego.
Implementa el patrón Observer para notificar cambios de estado.
"""
from typing import List, Protocol, Dict, Any
import logging

class Observer(Protocol):
    """Protocolo para observadores de estado."""
    def update(self, state: 'GameState') -> None:
        """Actualiza el observador con el nuevo estado."""
        pass

class GameState:
    """
    Clase que maneja el estado global del juego.
    Implementa el patrón Observer para notificar cambios.
    """
    def __init__(self):
        self._observers: List[Observer] = []
        self._state: Dict[str, Any] = {
            "score": 0,
            "health": 100,
            "level": 1,
            "game_state": "menu"
        }
        self._logger = logging.getLogger(__name__)

    def add_observer(self, observer: Observer) -> None:
        """Añade un nuevo observador."""
        self._observers.append(observer)
        self._logger.info(f"Nuevo observador añadido: {observer.__class__.__name__}")

    def remove_observer(self, observer: Observer) -> None:
        """Elimina un observador."""
        self._observers.remove(observer)
        self._logger.info(f"Observador eliminado: {observer.__class__.__name__}")

    def notify_observers(self) -> None:
        """Notifica a todos los observadores de un cambio en el estado."""
        for observer in self._observers:
            observer.update(self)

    def set_state(self, key: str, value: Any) -> None:
        """
        Actualiza un valor en el estado y notifica a los observadores.
        
        Args:
            key: Clave del estado a actualizar
            value: Nuevo valor
        """
        if key in self._state:
            old_value = self._state[key]
            self._state[key] = value
            self._logger.info(f"Estado actualizado: {key} = {value} (anterior: {old_value})")
            self.notify_observers()
        else:
            self._logger.warning(f"Intento de actualizar estado inexistente: {key}")

    def get_state(self, key: str) -> Any:
        """
        Obtiene un valor del estado.
        
        Args:
            key: Clave del estado a obtener
            
        Returns:
            Valor del estado
        """
        return self._state.get(key)

    @property
    def score(self) -> int:
        """Obtiene la puntuación actual."""
        return self._state["score"]

    @score.setter
    def score(self, value: int) -> None:
        """Establece la puntuación actual."""
        self.set_state("score", value)

    @property
    def health(self) -> int:
        """Obtiene la salud actual."""
        return self._state["health"]

    @health.setter
    def health(self, value: int) -> None:
        """Establece la salud actual."""
        self.set_state("health", value)

    @property
    def level(self) -> int:
        """Obtiene el nivel actual."""
        return self._state["level"]

    @level.setter
    def level(self, value: int) -> None:
        """Establece el nivel actual."""
        self.set_state("level", value)

    @property
    def game_state(self) -> str:
        """Obtiene el estado actual del juego."""
        return self._state["game_state"]

    @game_state.setter
    def game_state(self, value: str) -> None:
        """Establece el estado actual del juego."""
        self.set_state("game_state", value)
