# menu.py
import pygame
import sys
import settings
from settings import IMAGES_MENU, SOUNDS_MENU, RED, SCREEN_HEIGHT, SCREEN_WIDTH, FONTS
from .scene import Scene

class GameOver(Scene):
    def __init__(self, screen):
        super().__init__(screen) 
        self.screen = screen
        self.background = pygame.image.load(IMAGES_MENU["fin1"]).convert_alpha()
        self.background = pygame.transform.scale(self.background, (400, 400))
        self.running = True
        self.init_audio()
        # créditos (la línea de gracias cambia a continuación cuando termina la música)
        self.credits_text = "Trabajo práctico - Rodriguez, Guiñazú, Solari, Ugarte, Puche - Programación de videojuegos"
    
    def volver_al_menu(self):
            from .menu import Menu  # import local, no global
            menu = Menu(self.screen)
            menu.run()

    def draw(self):
        self.screen.fill((0, 0, 0))
        bg_rect = self.background.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(self.background, bg_rect)
        # Créditos
        credits_surface = self.text_font.render(self.credits_text, True, RED)
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
        pygame.mixer.music.load(SOUNDS_MENU["fin1"])
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT + 1:
                self.background = pygame.image.load(IMAGES_MENU["fin2"]).convert_alpha()
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.credits_text = settings.TEXTS.get(settings.LANGUAGE, {}).get('thanks_exit', "¡Gracias por jugar! - Enter para salir")
                # usar la carga de fuentes de la escena (respetando CJK si aplica)
                self.text_font = self.load_font(size=36)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    self.running = False

        

    def run(self):
            while self.running:
                self.handle_events()    
                self.draw()             
                pygame.display.flip()  

            self.volver_al_menu() 
            

 