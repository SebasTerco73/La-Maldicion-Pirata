import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, width=100, height=100, speed=5):
        super().__init__()
        # Cargar y escalar sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = speed

    def move(self, dx, dy):
        """Mueve al personaje en una dirección (dx, dy)."""
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def clamp_to_screen(self):
        """Mantiene al personaje dentro de la pantalla."""
        screen = pygame.display.get_surface()
        if screen:
            screen_width, screen_height = screen.get_size()
            self.rect.x = max(-50, min(self.rect.x, screen_width - self.rect.width+20))
            self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height+10))

    def update(self):
        """Cada subclase implementa su propia lógica de actualización."""
        pass