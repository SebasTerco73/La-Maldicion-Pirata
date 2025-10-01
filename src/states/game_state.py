from typing import List, Any, Callable
from utils.constants import GameStates

class Observer:
    """Interfaz para el patrón observador."""
    
    def update(self, subject: 'GameState') -> None:
        """Actualiza el observador cuando el estado cambia.
        
        Args:
            subject: El estado del juego que ha cambiado.
        """
        pass

class GameState:
    """Gestiona el estado global del juego."""
    
    _instance = None
    
    def __init__(self):
        """Inicializa el estado del juego."""
        self.score: int = 0
        self.health: int = 100
        self.current_state: GameStates = GameStates.MENU
        self.observers: List[Observer] = []
        self._custom_states: dict = {}
    
    @classmethod
    def get_instance(cls) -> 'GameState':
        """Obtiene la instancia única del estado del juego (patrón Singleton)."""
        if cls._instance is None:
            cls._instance = GameState()
        return cls._instance
    
    def add_observer(self, observer: Observer) -> None:
        """Añade un observador al estado.
        
        Args:
            observer: El observador a añadir.
        """
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer: Observer) -> None:
        """Elimina un observador del estado.
        
        Args:
            observer: El observador a eliminar.
        """
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self) -> None:
        """Notifica a todos los observadores de un cambio en el estado."""
        for observer in self.observers:
            observer.update(self)
    
    def change_game_state(self, new_state: GameStates) -> None:
        """Cambia el estado actual del juego.
        
        Args:
            new_state: El nuevo estado del juego.
        """
        self.current_state = new_state
        self.notify_observers()
    
    def update_score(self, points: int) -> None:
        """Actualiza la puntuación del juego.
        
        Args:
            points: Puntos a añadir (o restar si es negativo).
        """
        self.score += points
        self.notify_observers()
    
    def update_health(self, amount: int) -> None:
        """Actualiza la salud del jugador.
        
        Args:
            amount: Cantidad de salud a añadir (o restar si es negativo).
        """
        self.health = max(0, min(100, self.health + amount))
        self.notify_observers()
    
    def set_custom_state(self, key: str, value: Any) -> None:
        """Establece un estado personalizado.
        
        Args:
            key: Clave del estado personalizado.
            value: Valor del estado personalizado.
        """
        self._custom_states[key] = value
        self.notify_observers()
    
    def get_custom_state(self, key: str, default: Any = None) -> Any:
        """Obtiene un estado personalizado.
        
        Args:
            key: Clave del estado personalizado.
            default: Valor por defecto si la clave no existe.
            
        Returns:
            El valor del estado personalizado o el valor por defecto.
        """
        return self._custom_states.get(key, default)
    
    def reset(self) -> None:
        """Reinicia el estado del juego a sus valores iniciales."""
        self.score = 0
        self.health = 100
        self.current_state = GameStates.MENU
        self._custom_states.clear()
        self.notify_observers()