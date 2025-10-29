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
    ],
    "fin1": "assets/images/player.png",
    "fin2": "assets/images/team.png"
}

IMAGES_LVL1 = {
    "enemy_crab": "assets/images/cangrejo.png",
    "bg_far": "assets/images/bg_far.PNG",
    "bg_middle": "assets/images/bg_middle.PNG",
    "bg_near": "assets/images/bg_near.PNG",
    "start_anim_frames": [
        f"assets/images/cinem_finlvl1/frame_{i:02d}.png" for i in range(1, 10)
    ],
    "bg_looes_lvl1": "assets/images/loose_lvl1.JPEG",
}

IMAGES_LVL3= {
    "bg_far": "assets/images/lvl2_bg.png",
    "bg_middle": "assets/images/lvl2_bg2.png",
    "bg_near": "assets/images/lvl2_bg2.png",
    "enemy_ghost": "assets/images/ghost.png",
    "enemy_boss":"assets/images/boss.png",
    "cannon_boss":"assets/images/cannonBoss.png",
    "bg_looes_lvl3": "assets/images/loose_lvl3.JPEG",
}

# --- Sonidos ---
SOUNDS_MENU = {
    "menu_music": "assets/sounds/menu_sound.mp3",
    "menu_move": "assets/sounds/menu_move.mp3",
    "menu_enter":"assets/sounds/menu_enter.mp3",
    "menu_salir":"assets/sounds/menu_salir.mp3",
    "intro_music": "assets/sounds/cinem_audio.mp3",
    "fin1": "assets/sounds/solito.mp3"
}

SOUNDS_PLAYER = {
    "player_sound_jump": "assets/sounds/jump_sound.mp3",
    "player_sound_damage": "assets/sounds/player_damage.mp3",
}

SOUNDS_LVL1 = {
    "level1_sound": "assets/sounds/lvl1_sound_LLuvia.mp3",
    "lvl1_sound_Truenos": "assets/sounds/lvl1_sound_Trueno.mp3",
    "lvl1_sound_jump": "assets/sounds/jump_sound.mp3",
    "crab_died":"assets/sounds/crab_died.mp3",
    "lvl_win" : "assets/sounds/victory.mp3",
    "lvl_lose" : "assets/sounds/lose_violin.mp3",
}

SOUNDS_LVL3 = {
    "ghost_died":"assets/sounds/ghost_died.mp3", 
    "cannon_ready":"assets/sounds/cannon-ready.mp3",
    "cannon_fire":"assets/sounds/cannon-fire.mp3",
    "boss_damage":"assets/sounds/boss_damage.mp3",
    "boss_kill": "assets/sounds/bossKill.mp3"
}

IMAGES_LVL2= {
    "enemy_crab": "assets/images/lvl2_crab.png",
    "bg_far": "assets/images/nivel_02_far.png",
    "bg_middle": "assets/images/bg_middle_cloud.png",
    "bg_near": "assets/images/nivel_02_middle.png",
    "bg_front": "assets/images/fantass2.png",
    "enemy_ghost": "assets/images/ghost.png",
    "enemy_cannon": "assets/images/cannon.png", 
    "bg_looes_lvl2": "assets/images/loose_lvl2.JPEG",
    "enemy_boss":"assets/images/boss.png" ,
    "start_anim_frames": [
        f"assets/images/cinem_finlvl2/frame_{i:02d}.png" for i in range(1, 31)
    ], 
}

SOUNDS_LVL2 = {
    "ghost_died":"assets/sounds/ghost_died.mp3",
}

FONTS = {
    "main_font": "assets/fonts/main_font.ttf",
    "NotoSansCJKBold": "assets/fonts/Noto Sans CJK Bold.otf"
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

# Textos localizados usados por las escenas (menú principal y opciones).
# Añadir aquí las cadenas que se usan en varias pantallas facilita la internacionalización.
TEXTS = {
    "es": {
        "menu": ["Iniciar Partida", "Opciones", "Salir"],
        "options": ["Resolución", "Idioma", "Volumen", "Volver al menú"],
        "resolution_window": "Resolución: Ventana",
        "resolution_fullscreen": "Resolución: Pantalla Completa",
        "volume_format": "{label}: < {level} >",
        "score_label": "Puntos",
        "global_score_label": "Total"
    },
    "en": {
        "menu": ["Play", "Options", "Exit"],
        "options": ["Resolution", "Language", "Volume", "Return to Menu"],
        "resolution_window": "Resolution: Window",
        "resolution_fullscreen": "Resolution: Fullscreen",
        "volume_format": "{label}: < {level} >",
        "score_label": "Score",
        "global_score_label": "Total"
    },
    "zh": {
        "menu": ["开始游戏", "选项", "退出"],
        "options": ["分辨率", "语言", "音量", "返回菜单"],
        "resolution_window": "分辨率：窗口",
        "resolution_fullscreen": "分辨率：全屏",
        "volume_format": "{label}: < {level} >",
        "score_label": "分数",
        "global_score_label": "总计"
    }
}

# Mensajes genéricos usados en overlays (fin de nivel, pausa, créditos)
for lang, table in TEXTS.items():
    if lang == 'es':
        table.update({
            'end_title_win': 'GANASTE',
            'end_title_lose': 'PERDISTE',
            'end_lines_lose': ['R - Reintentar', 'M o ESC - Volver al menú'],
            'end_lines_win': ['Enter - Continuar'],
            'pause_title': 'PAUSA',
            'pause_lines': ['P - Continuar', 'M o ESC - Volver al menú'],
            'thanks_exit': '¡Gracias por jugar! - Enter para salir'
        })
    elif lang == 'en':
        table.update({
            'end_title_win': 'YOU WIN',
            'end_title_lose': 'YOU LOSE',
            'end_lines_lose': ['R - Retry', 'M or ESC - Return to Menu'],
            'end_lines_win': ['Enter - Continue'],
            'pause_title': 'PAUSE',
            'pause_lines': ['P - Continue', 'M or ESC - Return to Menu'],
            'thanks_exit': 'Thanks for playing! - Enter to exit'
        })
    elif lang == 'zh':
        table.update({
            'end_title_win': '你赢了',
            'end_title_lose': '你输了',
            'end_lines_lose': ['R - 重试', 'M 或 ESC - 返回菜单'],
            'end_lines_win': ['回车 - 继续'],
            'pause_title': '暂停',
            'pause_lines': ['P - 继续', 'M 或 ESC - 返回菜单'],
            'thanks_exit': '感谢游玩！按回车退出'
        })

LANGUAGE = "es"

LVL1_GROUND_Y = 500
LVL2_GROUND_Y = 500
# Puntaje global acumulado entre niveles
GLOBAL_SCORE = 0