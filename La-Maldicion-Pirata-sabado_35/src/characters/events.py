"""Módulo mínimo de eventos usado por personajes.

Proporciona:
- GameEvents: enumeración simple de eventos usados en el juego.
- EventSystem: implementación ligera con `emit` que llama handlers registrados.

Este archivo permite que `from .events import GameEvents` funcione incluso si
el proyecto no tenía un sistema de eventos completo.
"""
from enum import Enum, auto
from collections import defaultdict


class GameEvents(Enum):
    PLAYER_DAMAGE = auto()
    PLAYER_DEATH = auto()


class EventSystem:
    def __init__(self):
        self._handlers = defaultdict(list)

    def on(self, event, handler):
        self._handlers[event].append(handler)

    def emit(self, event, **kwargs):
        for h in self._handlers.get(event, []):
            try:
                h(**kwargs)
            except Exception:
                # No dejamos que un handler rompa el juego
                pass
