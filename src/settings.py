from enum import Enum
from typing import Dict, Any, Tuple

# --- Configuración de rutas ---
ASSETS_PATH = "assets"
IMAGES_PATH = f"{ASSETS_PATH}/images"
SOUNDS_PATH = f"{ASSETS_PATH}/sounds"
FONTS_PATH = f"{ASSETS_PATH}/fonts"

# --- Estados del juego ---
class GameStates(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

# --- Colores ---
COLORS: Dict[str, Tuple[int, int, int]] = {
    "WHITE": (255, 255, 255),
    "BLUE": (0, 0, 255),
    "RED": (120, 6, 6),
    "BLACK": (0, 0, 0)
}

# --- Configuración de pantalla ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Configuración del jugador ---
PLAYER_CONFIG: Dict[str, Any] = {
    "WIDTH": 100,
    "HEIGHT": 100,
    "SPEED": 5,
    "JUMP_STRENGTH": -15,
    "GRAVITY": 1
}

# --- Configuración del menú ---
MENU_CONFIG: Dict[str, Any] = {
    "FONT_SIZE": 40,
    "MARGIN": 20
}

# --- Configuración del nivel 1 ---
LVL1_CONFIG: Dict[str, Any] = {
    "GROUND_Y": 500,
    "SCROLL_SPEED": 4
}

# --- Configuración de audio ---
AUDIO_CONFIG: Dict[str, float] = {
    "MUSIC_VOLUME": 0.2,
    "SFX_VOLUME": 1.0
}

# --- Rutas de recursos ---
RESOURCE_PATHS = {
    "IMAGES": {
        "ICON": f"{IMAGES_PATH}/icon.png",
        "CURSOR": f"{IMAGES_PATH}/mouse.png",
        "PLAYER": f"{IMAGES_PATH}/player.png",
        "MENU_BG": f"{IMAGES_PATH}/menu_bg.png",
        "LEVEL1_BG": f"{IMAGES_PATH}/lvl1.jpg"
    },
    "SOUNDS": {
        "MENU": {
            "MUSIC": f"{SOUNDS_PATH}/menu_sound.mp3",
            "MOVE": f"{SOUNDS_PATH}/menu_move.mp3",
            "ENTER": f"{SOUNDS_PATH}/menu_enter.mp3",
            "EXIT": f"{SOUNDS_PATH}/menu_salir.mp3"
        },
        "LEVEL1": {
            "MUSIC": f"{SOUNDS_PATH}/lvl1_sound.mp3"
        }
    },
    "FONTS": {
        "MAIN": f"{FONTS_PATH}/main_font.ttf"
    }
}