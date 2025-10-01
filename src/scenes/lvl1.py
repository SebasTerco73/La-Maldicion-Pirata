# lvl1.py
import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGES_LVL1, SOUNDS_LVL1, LVL1_GROUND_Y
from .scene import Scene
from characters.player import Player

class Level1(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(IMAGES_LVL1["level1_bg"]).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_x = 0
        self.scroll_speed = 4
        self.mouse_visible = False
        self.init_audio()
        self.init = SCREEN_WIDTH/2 - 140
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.init, 0, LVL1_GROUND_Y)
        self.all_sprites.add(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        self.screen.blit(self.background, (self.bg_x, 0))
        self.all_sprites.draw(self.screen)
        self.draw_cursor()

    def init_audio(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(SOUNDS_LVL1["level1_sound"])
        pygame.mixer.music.play(-1)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000
            self.draw()
            self.handle_events()
            self.update(dt)
            pygame.display.flip()
