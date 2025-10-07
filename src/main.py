# main.py
import pygame
import sys
from scenes.menu import Menu
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, IMAGES, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("La maldición pirata")

    icon = pygame.image.load(IMAGES["icon"]) 
    pygame.display.set_icon(icon)
    #clock = pygame.time.Clock() 
    menu = Menu(screen)
    
    running = True
    while running:
        menu.run()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
