import pygame
import sys
import os

# Añadir el directorio raíz del proyecto al path de Python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scenes.menu import Menu
from states.game_state import GameState
from utils.resource_manager import ResourceManager
from utils.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    IMAGES_PATH,
    GameStates
)

def main():
    # Inicialización de Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("La maldición pirata")

    # Inicializar sistemas
    resource_manager = ResourceManager.get_instance()
    game_state = GameState.get_instance()
    
    # Cargar recursos
    icon = resource_manager.load_image(f"{IMAGES_PATH}/icon.png")
    pygame.display.set_icon(icon)
    
    # Configurar el juego
    clock = pygame.time.Clock()
    game_state.change_game_state(GameStates.MENU)
    menu = Menu(screen)
    
    running = True
    while running:
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000
        
        # Actualizar la escena actual según el estado del juego
        if game_state.current_state == GameStates.MENU:
            menu.run(dt)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()