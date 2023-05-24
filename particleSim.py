import pygame
import math
import random

pygame.init()
HEIGHT = 800
WIDTH = 1200

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Life")
clock = pygame.time.Clock()

def main():
    run = True
    while run:
        clock.tick(60)
        WIN.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        pygame.display.update()
        
    pygame.quit()
    
main()
                
    