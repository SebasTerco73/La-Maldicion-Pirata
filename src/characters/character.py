# character.py
import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=100, height=100, speed=200):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def move(self, dx, dt=1):
        self.rect.x += dx * self.speed * dt

    def clamp_to_screen(self):
        screen = pygame.display.get_surface()
       
        if screen:
       
 

            screen_width, screen_height = screen.get_size()
           
            
            self.rect.x = max(-50, min(self.rect.x, screen_width - self.rect.width + 20))
            self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height + 10))
            
            
            

    def update(self):
        pass
