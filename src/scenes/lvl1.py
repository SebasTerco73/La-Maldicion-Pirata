import pygame
import sys
from typing import Optional
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, 
    IMAGES_PATH, SOUNDS_PATH, LVL1_CONFIG,
    AUDIO_CONFIG
)
from utils.resource_manager import ResourceManager
from states.game_state import GameState
from scenes.scene import Scene
from characters.player import Player
from ui.cursor import Cursor

class Level1(Scene):
    def __init__(self, screen: pygame.Surface, dt: float):
        """Inicializa el nivel 1.
        
        Args:
            screen: Superficie de la pantalla
            dt: Delta time
        """
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.resource_manager = ResourceManager.get_instance()
        self.game_state = GameState.get_instance()
        
        # Cargar recursos
        self.background = self.resource_manager.load_image(f"{IMAGES_PATH}/lvl1.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Configuración del nivel
        self.bg_x = 0
        self.scroll_speed = LVL1_CONFIG["SCROLL_SPEED"]
        self.init_pos = SCREEN_WIDTH/2 - 140

        # UI
        self.cursor = Cursor()
        self.cursor.hide()  # Ocultar cursor en el nivel

        # Inicializar audio
        self.init_audio()

        # Grupo de sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.init_pos, 0, LVL1_CONFIG["GROUND_Y"], dt)
        self.all_sprites.add(self.player)

    def handle_events(self) -> None:
        """Maneja los eventos del juego."""
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt: float) -> None:
        """Actualiza los elementos del nivel.
        
        Args:
            dt: Delta time
        """
        self.all_sprites.update(dt)

    def draw(self) -> None:
        """Dibuja los elementos del nivel."""
        self.screen.blit(self.background, (self.bg_x, 0))
        self.all_sprites.draw(self.screen)   
        self.cursor.draw(self.screen)

    def init_audio(self) -> None:
        """Inicializa el sistema de audio."""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(AUDIO_CONFIG["MUSIC_VOLUME"])
        pygame.mixer.music.load(f"{SOUNDS_PATH}/lvl1_sound.mp3")
        pygame.mixer.music.play(-1)

    def run(self, dt: float) -> None:
        """Ejecuta el bucle principal del nivel.
        
        Args:
            dt: Delta time
        """
        running = True
        while running:
            self.draw()
            self.handle_events()
            self.update(dt)  
            pygame.display.flip()
            self.clock.tick(FPS)