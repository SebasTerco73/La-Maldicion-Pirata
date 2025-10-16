# menu.py
import pygame
import sys
from settings import IMAGES, IMAGES_MENU, SOUNDS_MENU, BLUE, RED, SCREEN_HEIGHT, SCREEN_WIDTH, MENU_MARGIN
from .scene import Scene
from .level1 import Level1
from .options import Options
class Menu(Scene):
    def __init__(self, screen):
        super().__init__(screen) 
        self.screen = screen
        self.options = ["Iniciar Partida", "Opciones", "Salir"]
        self.selected_index = 0
        self.background = pygame.image.load(IMAGES_MENU["menu_bg"]).convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.init_audio()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        option_height = self.font.get_height()
        total_height = len(self.options) * option_height + (len(self.options) - 1) * MENU_MARGIN
        start_y = (SCREEN_HEIGHT - total_height) // 2 + 200

        self.option_rects = []
        for index, option in enumerate(self.options):
            color = BLUE if index == self.selected_index else RED
            text_surface = self.font.render(option, True, color)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + index * (option_height + MENU_MARGIN)))
            self.option_rects.append(rect)
            self.draw_text_with_outline(option, self.font, color, (0, 0, 0),
                                        SCREEN_WIDTH // 2, start_y + index * (option_height + MENU_MARGIN))

        # Créditos
        credits_text = "Trabajo práctico - Rodriguez, Guiñazú, Solari, Ugarte, Puche - Programación de videojuegos"
        credits_surface = self.text_font.render(credits_text, True, RED)
        credits_rect = credits_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.screen.blit(credits_surface, credits_rect)

        self.draw_cursor()

    def draw_text_with_outline(self, text, font, text_color, outline_color, x, y):
        base = font.render(text, True, text_color)
        outline = font.render(text, True, outline_color)
        rect = base.get_rect(center=(x, y))
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]:
            self.screen.blit(outline, rect.move(dx, dy))
        self.screen.blit(base, rect)

    def init_audio(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(SOUNDS_MENU["menu_music"])
        pygame.mixer.music.play(-1)
        self.move_sound = pygame.mixer.Sound(SOUNDS_MENU["menu_move"])
        self.move_enter = pygame.mixer.Sound(SOUNDS_MENU["menu_enter"])
        self.move_salir = pygame.mixer.Sound(SOUNDS_MENU["menu_salir"])
    
    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    self.move_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    self.move_sound.play()
                elif event.key == pygame.K_RETURN:
                    self.select_option()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for index, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos) and self.selected_index != index:
                        self.selected_index = index
                        self.move_sound.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for index, rect in enumerate(self.option_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected_index = index
                            self.select_option()

    def select_option(self):
        match self.selected_index:
            case 0:
                self.move_enter.play()
                pygame.time.delay(200)
                pygame.mixer.music.stop()
                level1 = Level1(self.screen)
                level1.run()
                # Al regresar del nivel, reiniciar música del menú
                self.init_audio()
            case 1:
                self.move_enter.play()
                options = Options(self.screen)
                options.run()
            case 2:
                self.move_salir.play()
                while pygame.mixer.get_busy():
                    pygame.time.delay(50)
                pygame.quit()
                sys.exit()
    def run(self):
        self.draw()
        self.handle_events()
        pygame.display.flip()
