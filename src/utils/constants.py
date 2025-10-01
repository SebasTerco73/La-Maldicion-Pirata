from enum import Enum
from typing import Dict, Any

# Estados del juego
class GameStates(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
COLORS = {
    "WHITE": (255, 255, 255),
    "BLUE": (0, 0, 255),
    "RED": (120, 6, 6),
    "BLACK": (0, 0, 0)
}

# Rutas de recursos
ASSETS_PATH = "assets"
IMAGES_PATH = f"{ASSETS_PATH}/images"
SOUNDS_PATH = f"{ASSETS_PATH}/sounds"
FONTS_PATH = f"{ASSETS_PATH}/fonts"

# Configuración del jugador
PLAYER_CONFIG = {
    "WIDTH": 100,
    "HEIGHT": 100,
    "SPEED": 5,
    "JUMP_STRENGTH": -15,
    "GRAVITY": 1
}

# Configuración del menú
MENU_CONFIG = {
    "FONT_SIZE": 40,
    "MARGIN": 20
}

# Configuración del nivel 1
LVL1_CONFIG = {
    "GROUND_Y": 500,
    "SCROLL_SPEED": 4
}

# Configuración de audio
AUDIO_CONFIG = {
    "MUSIC_VOLUME": 0.2,
    "SFX_VOLUME": 1.0
}