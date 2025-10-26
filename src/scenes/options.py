# Imports
import pygame
import sys
import settings
from settings import IMAGES, IMAGES_MENU, SOUNDS_MENU, BLUE, WHITE, RED, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, MENU_MARGIN
#.scene porque esta dentro del mismo paquete
from .scene import Scene
from .level1 import Level1

class Options(Scene):
    def __init__(self, screen):
        super().__init__(screen) 
        self.screen = screen
        self.clock = pygame.time.Clock()
        # Inicializar opciones según configuración global de textos si existe
        self.options = settings.TEXTS.get(settings.LANGUAGE, {}).get("options", ["Resolución", "Idioma", "Volumen", "Volver al menú"])
        self.selected_index = 0
        # Cargar fondo según el idioma actual
        lang = settings.LANGUAGE
        if lang == "es":
            bg_key = "menu_bg"
        else:
            bg_key = f"menu_bg_{lang}"
        self.background = pygame.image.load(IMAGES_MENU.get(bg_key, IMAGES_MENU["menu_bg"])) .convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Nivel de volumen (de 0 a 10)
        self.volume_level = int(pygame.mixer.music.get_volume() * 10)
        
        self.init_audio()
        # Tomar idioma actual desde settings
        self.language = settings.LANGUAGE
        self.language_options = {
            "es": ["Resolución", "Idioma", "Volumen", "Volver al menú"],
            "en": ["Resolution", "Language", "Volume", "Return to Menu"],
            "zh": ["分辨率", "语言", "音量", "返回菜单"]
            }
        self.language_menu = {
            "es": ["Iniciar Partida", "Opciones", "Salir"],
            "en": ["Play", "Options", "Exit"],
            "zh": ["开始游戏", "选项", "退出"]
        }



    # dibujar menu 
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        option_height = self.font.get_height()
        total_height = len(self.options) * option_height + (len(self.options) - 1) * MENU_MARGIN
        start_y = (SCREEN_HEIGHT - total_height) // 2 + 200

        self.option_rects = []

        for index, option in enumerate(self.options):
            color = BLUE if index == self.selected_index else RED
            
            display_text = option
            # Lógica para texto dinámico de Resolución
            if index == 0:
                is_fullscreen = self.screen.get_flags() & pygame.FULLSCREEN
                if is_fullscreen:
                    display_text = settings.TEXTS.get(settings.LANGUAGE, {}).get("resolution_fullscreen", "Resolución: Pantalla Completa")
                else:
                    display_text = settings.TEXTS.get(settings.LANGUAGE, {}).get("resolution_window", "Resolución: Ventana")
            # Lógica para texto dinámico de Volumen
            elif index == 2:
                vol_format = settings.TEXTS.get(settings.LANGUAGE, {}).get("volume_format", "{label}: < {level} >")
                display_text = vol_format.format(label=option, level=self.volume_level)

            text_surface = self.font.render(display_text, True, color)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + index * (option_height + MENU_MARGIN)))
            self.option_rects.append(rect)
            
            self.draw_text_with_outline(
                display_text,
                self.font,
                color,
                (0, 0, 0),
                SCREEN_WIDTH // 2,
                start_y + index * (option_height + MENU_MARGIN)
            )

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

    def change_language(self):
        """Cambia entre los idiomas disponibles."""
        languages = ["es", "en", "zh"]
        current_index = languages.index(self.language)
        new_index = (current_index + 1) % len(languages)
        self.language = languages[new_index]

        # Actualizar texto del menú
        # actualizar opciones según settings.TEXTS (si está disponible)
        self.options = settings.TEXTS.get(self.language, {}).get("options", self.language_options[self.language])
        # actualizar settings global para que otras escenas lo vean
        settings.LANGUAGE = self.language

        # Recargar fuentes en esta escena para que muestren los glyphs correctos (p. ej. chino)
        self.font = self.load_font()
        self.text_font = self.load_font(size=14)

        # Cambiar fondo y música según idioma
        if self.language == "es":
            self.background = pygame.image.load(IMAGES_MENU.get("menu_bg")).convert_alpha()
        elif self.language == "en":
            self.background = pygame.image.load(IMAGES_MENU.get("menu_bg_en")).convert_alpha()
        elif self.language == "zh":
            self.background = pygame.image.load(IMAGES_MENU.get("menu_bg_zh")).convert_alpha()

        # Redimensionar fondo y reproducir nueva música
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        #pygame.mixer.music.play(-1)


    def init_audio(self):
        # Solo inicializa si no se hizo ya
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # NO reiniciamos el volumen aquí. Usamos el que ya está configurado.
        # pygame.mixer.music.set_volume(0.2) <--- LÍNEA ELIMINADA

        # Si la música del menú no está sonando, la cargamos y reproducimos.
        # Esto evita recargar la música innecesariamente si volvemos desde el menú principal.
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(SOUNDS_MENU["menu_music"])
            pygame.mixer.music.play(-1)
            
        self.move_sound = pygame.mixer.Sound(SOUNDS_MENU["menu_move"])
        self.move_enter = pygame.mixer.Sound(SOUNDS_MENU["menu_enter"])
        self.move_salir = pygame.mixer.Sound(SOUNDS_MENU["menu_salir"])
    
    # Eventos de teclas
    def handle_events(self):
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
                    self.select_option()
                    return True
                
                # --- Lógica para ajustar el volumen ---
                elif self.selected_index == 2: # Si "Volumen" está seleccionado
                    if event.key == pygame.K_LEFT:
                        self.volume_level = max(0, self.volume_level - 1)
                        self.set_volume()
                        self.move_sound.play()
                    elif event.key == pygame.K_RIGHT:
                        self.volume_level = min(10, self.volume_level + 1)
                        self.set_volume()
                        self.move_sound.play()

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
                            self.select_option()
                            return True

    def select_option(self):
        
        if self.selected_index == 0: # Resolución
                self.move_enter.play()
                self.toggle_fullscreen()
        if self.selected_index == 1:  # Idioma
            self.move_enter.play()
            self.change_language()

        if self.selected_index == 2: # Volumen (ya no hace nada al presionar Enter)
                self.move_enter.play()
        if self.selected_index == 3: # Volver al menú
                self.move_enter.play()
                print("Volver al menu")

    def toggle_fullscreen(self):
        """Cambia entre modo ventana y pantalla completa."""
        is_fullscreen = self.screen.get_flags() & pygame.FULLSCREEN
        if is_fullscreen:
            # Cambiar a modo ventana
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            # Cambiar a pantalla completa
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    def set_volume(self):
        """Ajusta el volumen global de la música basado en self.volume_level."""
        volume_float = self.volume_level / 10.0
        pygame.mixer.music.set_volume(volume_float)

    def run(self):
        running = True
        while running:
            self.draw() # Dibuja
            pressedKey = self.handle_events()
            pygame.display.flip() # Actualiza 
            self.clock.tick(FPS) # velocidad del bucle 60 FPS (frames por segundo).
            if self.selected_index == 3 and pressedKey:
                running = False