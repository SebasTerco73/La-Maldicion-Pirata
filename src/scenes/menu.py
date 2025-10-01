import pygame
import sys
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    IMAGES_PATH, SOUNDS_PATH,
    COLORS, MENU_CONFIG, AUDIO_CONFIG,
    GameStates
)
from utils.resource_manager import ResourceManager
from states.game_state import GameState
from ui.menu_elements import Menu as UIMenu, MenuItem
from scenes.scene import Scene
from scenes.lvl1 import Level1

class Menu(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.screen = screen
        self.resource_manager = ResourceManager.get_instance()
        self.game_state = GameState.get_instance()
        
        # Opciones del menú
        self.options = ["Iniciar Partida", "Opciones", "Salir"]
        self.selected_index = 0
        
        # Cargar recursos
        self.background = self.resource_manager.load_image(f"{IMAGES_PATH}/menu_bg.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.init_audio()

    # dibujar menu 
    def draw(self):
        """Dibuja el menú y sus elementos."""
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))
        
        # Calcular posiciones
        option_height = self.font.get_height()
        total_height = len(self.options) * option_height + (len(self.options) - 1) * MENU_CONFIG["MARGIN"]
        start_y = (SCREEN_HEIGHT - total_height) // 2 + 200

        self.option_rects = []

        # Dibujar opciones
        for index, option in enumerate(self.options):
            color = COLORS["BLUE"] if index == self.selected_index else COLORS["RED"]
            text_surface = self.font.render(option, True, color)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + index * (option_height + MENU_CONFIG["MARGIN"])))
            self.option_rects.append(rect)
            
            self.draw_text_with_outline(
                option,
                self.font,
                color,
                COLORS["BLACK"],
                SCREEN_WIDTH // 2,
                start_y + index * (option_height + MENU_CONFIG["MARGIN"])
            )

        # Dibujar créditos
        credits_text = "Trabajo práctico - Rodriguez, Guiñazú, Solari, Ugarte, Puche - Programación de videojuegos"
        credits_surface = self.text_font.render(credits_text, True, COLORS["RED"])
        credits_rect = credits_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(credits_surface, credits_rect)

        # Dibujar cursor
        self.draw_cursor()

    # función auxiliar para texto con contorno
    def draw_text_with_outline(self, text, font, text_color, outline_color, x, y):
        base = font.render(text, True, text_color)
        outline = font.render(text, True, outline_color)
        rect = base.get_rect(center=(x, y))
        # Dibuja contorno alrededor
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
            self.screen.blit(outline, rect.move(dx, dy))
        # Texto principal encima
        self.screen.blit(base, rect)

    def init_audio(self):
        """Inicializa el sistema de audio del menú."""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        pygame.mixer.music.set_volume(AUDIO_CONFIG["MUSIC_VOLUME"])
        
        # Cargar sonidos usando ResourceManager
        pygame.mixer.music.load(f"{SOUNDS_PATH}/menu_sound.mp3")
        pygame.mixer.music.play(-1)
        
        self.move_sound = self.resource_manager.load_sound(f"{SOUNDS_PATH}/menu_move.mp3")
        self.move_enter = self.resource_manager.load_sound(f"{SOUNDS_PATH}/menu_enter.mp3")
        self.move_salir = self.resource_manager.load_sound(f"{SOUNDS_PATH}/menu_salir.mp3")
    
    # Eventos de teclas
    def handle_events(self,dt):
        for event in pygame.event.get():
            self.handle_global_events(event) 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # teclado
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    self.move_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    self.move_sound.play()
                elif event.key == pygame.K_RETURN:
                    self.select_option(dt)

            # mouse hover
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        if self.selected_index != index:
                            self.selected_index = index
                            self.move_sound.play()
            # mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # botón izquierdo
                    mouse_pos = event.pos
                    for index, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected_index = index
                            self.select_option(dt)

    def select_option(self, dt: float) -> None:
        """Maneja la selección de opciones del menú.
        
        Args:
            dt: Delta time
        """
        match self.selected_index:
            case 0:  # Iniciar partida
                print("Iniciar partida")
                self.move_enter.play()
                pygame.time.delay(200)
                pygame.mixer.music.stop()
                self.game_state.change_game_state(GameStates.PLAYING)
                level1 = Level1(self.screen, dt)
                level1.run(dt)
            case 1:  # Opciones
                print("Opciones")
                self.move_enter.play()
                # TODO: Implementar menú de opciones
            case 2:  # Salir
                self.move_salir.play()
                # Esperar a que termine el sonido
                while pygame.mixer.get_busy():
                    pygame.time.delay(50)
                self.game_state.change_game_state(GameStates.MENU)
                pygame.quit()
                sys.exit()

    def run(self, dt):
        self.draw() # Dibuja
        self.handle_events(dt)  # manejar eventos de teclas
        pygame.display.flip() # Actualiza 