import pygame
import sys
from settings import IMAGES, IMAGES_MENU, SOUNDS_MENU, BLUE, WHITE, RED, FPS, SCREEN_HEIGHT, SCREEN_WIDTH,MENU_MARGIN
#.scene porque esta dentro del mismo paquete
from .scene import Scene
from .level1 import Level1
from .volumeSlider import Volume
class Options(Scene):
    def __init__(self, screen):
        super().__init__(screen) 
        self.screen = screen
        self.clock = pygame.time.Clock() # Velocidad de actualización (FPS).
        self.options = ["Resolución","Idioma", "Volumen", "Volver al menú"]  # Opciones
        self.selected_index = 0 # Opcion seleccionada
        self.background = pygame.image.load(IMAGES_MENU["menu_bg"]).convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.init_audio()

    # dibujar menu 
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        option_height = self.font.get_height()  # altura del texto
        total_height = len(self.options) * option_height + (len(self.options) - 1) * MENU_MARGIN
        start_y = (SCREEN_HEIGHT - total_height) // 2 + 200

        self.option_rects = [] # Lista vacía para los rectangulos / eventos de mouse

        for index, option in enumerate(self.options):
            color = BLUE if index == self.selected_index else RED
            text_surface = self.font.render(option, True, color)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + index * (option_height + MENU_MARGIN)))
            self.option_rects.append(rect)  # guardo el rectángulo / mouse event
            self.draw_text_with_outline(
                option,
                self.font,
                color,
                (0, 0, 0),  # contorno negro
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

    def init_audio(self):
        # Solo inicializa si no se hizo ya
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
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
        match self.selected_index:
            case 0:
                self.move_enter.play()
            case 1:
                self.move_enter.play()
            case 2:
                volumeSlider = Volume(self.screen)
                volumeSlider.run()
                self.move_enter.play()
            case 3:
                self.move_enter.play()
                print("Volver al menu")

    def run(self):
        running = True
        while running:
            self.draw() # Dibuja
            pressedKey = self.handle_events()
            pygame.display.flip() # Actualiza 
            self.clock.tick(FPS) # velocidad del bucle 60 FPS (frames por segundo).
            if self.selected_index == 3 and pressedKey:
                running = False