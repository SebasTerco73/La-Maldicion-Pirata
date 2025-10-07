import pygame
import sys
import random
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, IMAGES_LVL1, SOUNDS_LVL1, LVL1_GROUND_Y, WHITE
from .scene import Scene
from characters.player import Player
from characters.enemy import Crab
from states.event_system import EventSystem, GameEvents

class Level1(Scene):
    def __init__(self, screen, dt):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(IMAGES_LVL1["level1_bg"]).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.bg_x = 0  # posición inicial del fondo
        self.scroll_speed = 4

        self.mouse_visible = False
        self.init_audio()
        self.init = SCREEN_WIDTH/2 - 140

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Crear jugador
        self.player = Player(self.init, 0, LVL1_GROUND_Y, dt)
        self.all_sprites.add(self.player)
        
        # Generar cangrejos
        self.spawn_crabs(5)  # Iniciar con 5 cangrejos
        
        # Estado del juego
        self.game_over = False
        self.victory = False
        
        # Sistema de eventos
        self.event_system = EventSystem.get_instance()
        self.event_system.subscribe(GameEvents.PLAYER_DEATH, self.on_player_death)

    def spawn_crabs(self, count):
        """Genera cangrejos enemigos en posiciones aleatorias"""
        for _ in range(count):
            x = random.randint(100, SCREEN_WIDTH - 100)
            crab = Crab(x, 0, LVL1_GROUND_Y)
            self.all_sprites.add(crab)
            self.enemies.add(crab)

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_global_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (self.game_over or self.victory):
                if event.key == pygame.K_RETURN:
                    self.reset_level()

    def update(self, dt):
        if not self.game_over and not self.victory:
            # Actualizar jugador
            self.player.update(dt)
            
            # Actualizar enemigos individualmente
            for enemy in list(self.enemies):  # Crear una copia de la lista para evitar modificaciones durante la iteración
                if enemy in self.enemies:  # Verificar que el enemigo aún existe
                    enemy.update(dt, self.player)
            
            # Comprobar victoria (cuando no quedan enemigos)
            if len(self.enemies) == 0:
                self.victory = True
                self.game_over = True
                self.show_victory_message()
                
            # Comprobar derrota
            if self.player.health <= 0:
                self.game_over = True

    def draw(self):
        self.screen.blit(self.background, (self.bg_x, 0))
        self.all_sprites.draw(self.screen)
        
        # Dibujar barra de vida
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20
        
        # Borde de la barra de vida
        pygame.draw.rect(self.screen, WHITE, (health_x-2, health_y-2, health_width+4, health_height+4))
        # Barra de vida
        health_percent = max(0, self.player.health / 100.0)
        pygame.draw.rect(self.screen, (255, 0, 0), 
                        (health_x, health_y, health_width * health_percent, health_height))
        
        # Dibujar mensajes de estado
        if self.game_over:
            self.draw_message()
            
        self.draw_cursor()

    def init_audio(self):
        # Solo inicializa si no se hizo ya
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load(SOUNDS_LVL1["level1_sound"])
        pygame.mixer.music.play(-1)
    
    def draw_message(self):
        """Dibuja el mensaje de victoria o derrota"""
        font = pygame.font.Font(None, 74)
        if self.victory:
            text = font.render('¡Has Ganado!', True, WHITE)
        else:
            text = font.render('Game Over', True, WHITE)
        
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.screen.blit(text, text_rect)
        
        # Instrucciones para reiniciar
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render('Presiona ENTER para reiniciar', True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def show_victory_message(self):
        """Muestra el mensaje de victoria"""
        self.victory = True
        self.game_over = True

    def on_player_death(self):
        """Manejador para cuando el jugador muere"""
        self.game_over = True
        
    def reset_level(self):
        """Reinicia el nivel al estado inicial"""
        self.game_over = False
        self.victory = False
        
        # Limpiar sprites
        self.all_sprites.empty()
        self.enemies.empty()
        
        # Recrear jugador
        self.player = Player(self.init, 0, LVL1_GROUND_Y, 0)
        self.all_sprites.add(self.player)
        
        # Regenerar enemigos
        self.spawn_crabs(5)

    def run(self, dt):
        running = True
        while running:
            self.draw()
            self.handle_events()
            self.update(dt)  
            pygame.display.flip()
            self.clock.tick(FPS)