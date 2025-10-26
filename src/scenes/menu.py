import pygame
import sys
import settings
from settings import IMAGES, IMAGES_MENU, SOUNDS_MENU, BLUE, RED, SCREEN_HEIGHT, SCREEN_WIDTH, MENU_MARGIN
from .scene import Scene
from .level1 import Level1
from .options import Options
class Menu(Scene):
    def __init__(self, screen):
        super().__init__(screen) 
        self.screen = screen
        self.selected_index = 0
        # Cargar opciones del menú según el idioma actual (definido en settings.TEXTS)
        self.current_language = settings.LANGUAGE
        self.options = settings.TEXTS.get(self.current_language, {}).get("menu", ["Iniciar Partida", "Opciones", "Salir"])
        # Cargar y escalar fondo
        self.load_background()
        self.init_audio()

    def load_background(self):
        # Selecciona la clave del fondo según el idioma (cae al fondo por defecto si no existe)
        lang = settings.LANGUAGE
        if lang == "es":
            key = "menu_bg"
        else:
            key = f"menu_bg_{lang}"
        path = IMAGES_MENU.get(key, IMAGES_MENU.get("menu_bg"))
        self.background = pygame.image.load(path).convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        # Si el idioma cambió externamente, actualizar opciones y fondo
        if settings.LANGUAGE != self.current_language:
            self.current_language = settings.LANGUAGE
            self.options = settings.TEXTS.get(settings.LANGUAGE, {}).get("menu", self.options)
            self.load_background()
            # Recargar fuentes según nuevo idioma (por ejemplo para CJK)
            self.font = self.load_font()
            self.text_font = self.load_font(size=14)

        # Dibujar fondo y las opciones
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
        pygame.mixer.music.set_volume(0.9)
        pygame.mixer.music.load(SOUNDS_MENU["menu_music"])
        pygame.mixer.music.play(-1)
        self.move_sound = pygame.mixer.Sound(SOUNDS_MENU["menu_move"])
        self.move_enter = pygame.mixer.Sound(SOUNDS_MENU["menu_enter"])
        self.move_salir = pygame.mixer.Sound(SOUNDS_MENU["menu_salir"])
        self.move_intro = pygame.mixer.Sound(SOUNDS_MENU["intro_music"])
    
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
        
        if self.selected_index == 0:
                self.move_enter.play()
                pygame.time.delay(200)
                pygame.mixer.music.stop()
               # pygame.mixer.Sound.stop(self.move_enter)
              
                    #  Reproducir animación de inicio
                self.move_intro.play() 
                self.play_start_animation()
                 
                #  Iniciar el juego después de la animación
                level1 = Level1(self.screen)
                level1.run()

                # Al regresar del nivel, reiniciar música del menú
                self.init_audio()
             
        if self.selected_index == 1:
                self.move_enter.play()
                options = Options(self.screen)
                options.run()
        if self.selected_index == 2:
                self.move_salir.play()
                pygame.mixer.music.stop()  # Detenemos la música del menú
                pygame.time.wait(int(self.move_salir.get_length() * 1000))  # Espera solo la duración del sonido salir
                pygame.quit()
                sys.exit()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
    """Reproduce una animación antes de iniciar el juego."""

    def play_start_animation(self):
        
        clock = pygame.time.Clock()

        # Cargar frames
        frames = [
            pygame.image.load(path).convert_alpha()
            for path in IMAGES_MENU["start_anim_frames"]
        ]
        frames = [
            pygame.transform.scale(f, (SCREEN_WIDTH, SCREEN_HEIGHT)) for f in frames
        ]

        frame_duration = 100  # milisegundos por frame (0.1 seg)
        current_frame = 0
        last_update = pygame.time.get_ticks()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            now = pygame.time.get_ticks()
            if now - last_update > frame_duration:
                current_frame += 1
                last_update = now
                if current_frame >= len(frames):
                    running = False  # termina animación

            if current_frame < len(frames):
                self.screen.blit(frames[current_frame], (0, 0))
            pygame.display.flip()
            clock.tick(60)
                # Detener música de introducción (opcional)
        self.move_intro.stop()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

    def run(self):
        self.draw()
        self.handle_events()
        pygame.display.flip()
