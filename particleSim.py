import pygame
import random
import math

HEIGHT, WIDTH = 250, 250
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

BACKGROUND = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FRICTION = 0.70

particles = []

class Particle():
    def __init__(self, x, y, x_vel, y_vel, color):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
    
    def draw(self, win):
        x = self.x + WIDTH//2
        y = self.y + HEIGHT//2
        pygame.draw.circle(win, self.color, (x,y), 6)
        
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)
    
def create(n, color):
    group = []
    for _ in range(n):
        x = random.randint(-WIDTH//2, WIDTH//2)
        y = random.randint(-HEIGHT//2, HEIGHT//2)
        x_vel = random.uniform(-1, 1)
        y_vel = random.uniform(-1, 1)
        group.append(Particle(x, y, x_vel, y_vel, color))
    particles.append(group)
    return group

def rule(particles1, particles2, g):
    for a in particles1:
        for b in particles2:
            if a != b:
                dx = a.x - b.x
                dy = a.y - b.y
                d = math.sqrt(dx ** 2 + dy ** 2)

                if 0 < d < 80:
                    F = g / d
                    theta = math.atan2(dy, dx)
                    fx = F * math.cos(theta)
                    fy = F * math.sin(theta)

                    a.x_vel += fx
                    a.y_vel += fy
                    
        a.x_vel *= FRICTION
        a.y_vel *= FRICTION
        
        a.x += a.x_vel
        a.y += a.y_vel

        if a.x <= -WIDTH // 2:
            a.x_vel *= -1
            a.x = -WIDTH // 2
        elif a.x >= WIDTH // 2:
            a.x_vel *= -1
            a.x = WIDTH // 2
        if a.y <= -HEIGHT // 2:
            a.y_vel *= -1
            a.y = -HEIGHT // 2
        elif a.y >= HEIGHT // 2:
            a.y_vel *= -1
            a.y = HEIGHT // 2

def main(seed):
    random.seed(seed)
    clock = pygame.time.Clock()

    yellow = create(100, YELLOW)
    green = create(100, GREEN)
    blue = create(100, BLUE)
    white = create(100, WHITE)

    run = True
    while run:
        clock.tick(60)
        WIN.fill(BACKGROUND)

        rule(yellow, yellow, -1)
        rule(yellow, blue, -1)
        rule(yellow, white, 1)
        rule(yellow, green, 1)
        
        
        rule(green, green, -1)
        rule(green, white, 1)
        rule(green, yellow, -1)
        rule(green, blue, 1)
        
        rule(blue, blue, -1)
        rule(blue, white, -1)
        rule(blue, green, 1)
        rule(blue, yellow, 1)
        
        rule(white, white, -1)
        rule(white, yellow, 1)
        rule(white, green, -1)
        rule(white, blue, 1)
        
        

        for group in particles:
            for particle in group:
                particle.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    
    pygame.quit()

main(1)