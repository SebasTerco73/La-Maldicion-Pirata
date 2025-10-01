import unittest
import pygame
import os
import sys

# Añadir el directorio src al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.resource_manager import ResourceManager
from states.game_state import GameState
from physics.gravity import GravitySystem
from utils.constants import GameStates, PLAYER_CONFIG

class TestGameSystems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # Crear una ventana pequeña para los tests
        pygame.display.set_mode((100, 100))

    def setUp(self):
        # Reiniciar estados antes de cada test
        self.resource_manager = ResourceManager.get_instance()
        self.game_state = GameState.get_instance()
        self.gravity_system = GravitySystem.get_instance()
        self.game_state.reset()

    def test_game_state_singleton(self):
        """Prueba que GameState implementa correctamente el patrón Singleton."""
        state1 = GameState.get_instance()
        state2 = GameState.get_instance()
        self.assertIs(state1, state2)

    def test_game_state_changes(self):
        """Prueba los cambios de estado del juego."""
        self.game_state.change_game_state(GameStates.PLAYING)
        self.assertEqual(self.game_state.current_state, GameStates.PLAYING)

    def test_resource_manager_singleton(self):
        """Prueba que ResourceManager implementa correctamente el patrón Singleton."""
        rm1 = ResourceManager.get_instance()
        rm2 = ResourceManager.get_instance()
        self.assertIs(rm1, rm2)

    def test_gravity_system(self):
        """Prueba el sistema de gravedad."""
        from physics.gravity import PhysicsEntity
        
        entity = PhysicsEntity()
        self.gravity_system.apply(entity)
        self.assertEqual(entity.acceleration.y, PLAYER_CONFIG["GRAVITY"])

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()