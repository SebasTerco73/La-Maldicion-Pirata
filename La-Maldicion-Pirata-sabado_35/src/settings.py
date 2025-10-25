# --- Imágenes ---
IMAGES = {
    "icon": "assets/images/icon.png",
    "cursor": "assets/images/mouse.png",
    "player-right": "assets/images/pirate-right.png",
    "player-left": "assets/images/pirate-left.png",
    "player-walk": "assets/images/player-walk.png",
    "player-jump": "assets/images/player-jump.png",
}

IMAGES_MENU = {
    "menu_bg": "assets/images/menu_bg.png",
    "menu_bg_en": "assets/images/menu_bg_en.png",
    "menu_bg_zh": "assets/images/menu_bg_zh.png",
    "start_anim_frames": [
        f"assets/images/cinematica_01/frame_{i:02d}.png" for i in range(1, 26)
    ]
}


IMAGES_LVL1 = {
    "enemy_crab": "assets/images/cangrejo.png",
    "bg_far": "assets/images/bg_far.PNG",
    "bg_middle": "assets/images/bg_middle.PNG",
    "bg_near": "assets/images/bg_near.PNG",
     "start_anim_frames": [
        f"assets/images/cinem_finlvl1/frame_{i:02d}.png" for i in range(1, 10)
    ]
}

IMAGES_LVL2= {
    "enemy_crab": "assets/images/lvl2_crab.png",
    "bg_far": "assets/images/nivel_02_far.png",
    "bg_middle": "assets/images/bg_middle_cloud.png",
    "bg_near": "assets/images/nivel_02_middle.png",
    "bg_front": "assets/images/fantass2.png",
    "enemy_ghost": "assets/images/ghost.png",
    "enemy_cannon": "assets/images/cannon.png", 
 
    "enemy_boss":"assets/images/boss.png"  
}
# --- Sonidos ---
SOUNDS_MENU = {
    "menu_music": "assets/sounds/menu_sound.mp3",
    "menu_move": "assets/sounds/menu_move.mp3",
    "menu_enter":"assets/sounds/menu_enter.mp3",
    "menu_salir":"assets/sounds/menu_salir.mp3",
    "intro_music": "assets/sounds/cinem_audio.mp3"
}

SOUNDS_LVL1 = {
    "level1_sound": "assets/sounds/lvl1_sound_LLuvia.mp3",
    "lvl1_sound_Truenos": "assets/sounds/lvl1_sound_Trueno.mp3",
    "lvl1_sound_jump": "assets/sounds/jump_sound.mp3",
    "crab_died":"assets/sounds/crab_died.mp3",
    "lvl_win" : "assets/sounds/victory.mp3",
    "lvl_lose" : "assets/sounds/lose_violin.mp3",
}
SOUNDS_PLAYER = {
    "player_sound_jump": "assets/sounds/jump_sound.mp3",
    "player_sound_damage": "assets/sounds/player_damage.mp3",
    "player_sound_died" : "assets/sounds/player_di.mp3"
}
SOUNDS_LVL2 = {
    
    "ghost_died":"assets/sounds/ghost_died.mp3",
   
}

FONTS = {
    "main_font": "assets/fonts/main_font.ttf"
}

# --- Configuración general ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (120, 6, 6)
MENU_FONT_SIZE = 40
MENU_MARGIN = 20
LANGUAGE = "es" 
LVL1_GROUND_Y = 500
LVL2_GROUND_Y = 500