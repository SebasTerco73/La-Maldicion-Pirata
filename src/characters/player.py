import pygame
from utils.constants import (
    IMAGES_PATH, FPS, PLAYER_CONFIG, LVL1_CONFIG
)
from characters.character import Character

class Player(Character):
    def __init__(self, x: float, y: float, ground: float, dt: float):
        super().__init__(
            f"{IMAGES_PATH}/player.png",
            x, y,
            width=PLAYER_CONFIG["WIDTH"],
            height=PLAYER_CONFIG["HEIGHT"],
            speed=PLAYER_CONFIG["SPEED"]
        )
        self.vel_y = 0
        self.gravity = PLAYER_CONFIG["GRAVITY"]
        self.jump_strength = PLAYER_CONFIG["JUMP_STRENGTH"]
        self.on_ground = False
        self.ground_y = ground
        self.posX = 50.0
        self.speed = 20.0
       
    def handle_input(self,dt):
        keys = pygame.key.get_pressed()
        # Reiniciamos el movimiento horizontal en cada frame
        self.posX = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.posX = -self.speed
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.posX = self.speed
        
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Aplicamos el movimiento horizontal con delta time
        if self.posX:
            self.move(self.posX * dt, 0)
    
    def apply_gravity(self):
        """Aplica gravedad y limita el suelo"""
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Colisión con el suelo
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vel_y = 0
            self.on_ground = True

    def update(self,dt):
        self.handle_input(dt)
        self.clamp_to_screen()
        self.apply_gravity()

