import pygame
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGES_LVL1, SOUNDS_LVL1, LVL1_GROUND_Y
from .scene import Scene
from characters.player import Player
from characters.enemy import Crab

class Level1(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(IMAGES_LVL1["level1_bg"]).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.bg_x = 0  # posición inicial del fondo
        self.scroll_speed = 4

        self.mouse_visible = False
        self.init_audio()
        # Donde inicia el personaje en el eje x
        self.init = SCREEN_WIDTH/2 - 140

        # Grupo de sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.init, 0, LVL1_GROUND_Y)
        self.all_sprites.add(self.player)
        self.player.rect.x

        
        self.all_crabs = pygame.sprite.Group()
        for _ in range(10):  # Generar 10 NPCs
            x = random.randint(400, 800)
            crab = Crab(x,LVL1_GROUND_Y)
            self.all_crabs.add(crab)
            crab.rect.x

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, all_crabs):
        keys = pygame.key.get_pressed()
        
        # Scroll infinito
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.bg_x -= self.scroll_speed
            for crab in all_crabs:
                crab.rect.x += self.scroll_speed
            # for ind in range(len(self.all_crabs)):
            #     pass    


        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.bg_x += self.scroll_speed

        # Reiniciar cuando se salga del ancho
        if self.bg_x <= -SCREEN_WIDTH:
            self.bg_x = 0
        if self.bg_x >= SCREEN_WIDTH:
            self.bg_x = 0

        self.all_sprites.update()

    def draw(self):
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + SCREEN_WIDTH, 0))
        self.screen.blit(self.background, (self.bg_x - SCREEN_WIDTH, 0))
        self.all_sprites.draw(self.screen)   
        self.draw_cursor()

    def init_audio(self):
        # Solo inicializa si no se hizo ya
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(SOUNDS_LVL1["level1_sound"])
        pygame.mixer.music.play(-1)

    def run(self):
        running = True
        while running:
            self.draw()
            self.handle_events()

            self.update(self.all_crabs)
            pygame.display.flip()
            self.clock.tick(FPS)