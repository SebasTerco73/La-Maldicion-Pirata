"""
Constantes y configuraciones globales del juego.
"""
from enum import Enum
from typing import Dict, Any

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
class Colors:
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (120, 6, 6)

# Estados del juego
class GameStates(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# Configuración de jugador
PLAYER_CONFIG = {
    "width": 30,
    "height": 30,
    "speed": 25.0,
    "jump_strength": -15,
    "gravity": 1.0
}

# Configuración de la física
PHYSICS_CONFIG = {
    "gravity": 1.0,
    "ground_y": 500
}

# Configuración del menú
MENU_CONFIG = {
    "font_size": 40,
    "margin": 20
}

# Rutas de recursos
class AssetPaths:
    # Imágenes
    IMAGES: Dict[str, str] = {
        "icon": "assets/images/icon.png",
        "cursor": "assets/images/mouse.png",
        "player": "assets/images/player.png",
        "menu_bg": "assets/images/menu_bg.png",
        "level1_bg": "assets/images/lvl1.jpg"
    }

    # Sonidos
    SOUNDS: Dict[str, str] = {
        "menu_music": "assets/sounds/menu_sound.mp3",
        "menu_move": "assets/sounds/menu_move.mp3",
        "menu_enter": "assets/sounds/menu_enter.mp3",
        "menu_salir": "assets/sounds/menu_salir.mp3",
        "level1_sound": "assets/sounds/lvl1_sound.mp3"
    }

    # Fuentes
    FONTS: Dict[str, str] = {
        "main_font": "assets/fonts/main_font.ttf"
    }
