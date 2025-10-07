import pygame
import sys
from scenes.menu import Menu
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, IMAGES, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("La maldición pirata")

    icon = pygame.image.load(IMAGES["icon"]) 
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock() 
    menu = Menu(screen)
    
    running = True
    while running:
        dt_ms = clock.tick(FPS) # velocidad del bucle 60 FPS (frames por segundo).
        dt = dt_ms /1000
        menu.run(dt)
        pygame.display.flip() # Actualiza 
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    dt = 0 
    main()