import pygame
import random
import math

HEIGHT, WIDTH = 600, 600
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

BACKGROUND = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FRICTION = 0.70
MIN_DISTANCE = 100
EPSILON = 1e-6

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
                if d < MIN_DISTANCE:
                    F = -g / (d + EPSILON)  
                else:
                    F = g / (d + EPSILON)  

                theta = math.atan2(dy, dx)
                fx = F * math.cos(theta)
                fy = F * math.sin(theta)

                a.x_vel += fx
                a.y_vel += fy
                    
        a.x_vel *= FRICTION
        a.y_vel *= FRICTION
        
        a.x += a.x_vel
        a.y += a.y_vel

        # Particle boundary conditions
        if a.x < -WIDTH // 2:
            a.x = WIDTH // 2
        elif a.x > WIDTH // 2:
            a.x = -WIDTH // 2
        if a.y < -HEIGHT // 2:
            a.y = HEIGHT // 2
        elif a.y > HEIGHT // 2:
            a.y = -HEIGHT // 2

def main(particles):
    clock = pygame.time.Clock()

    yellow = create(80, YELLOW)
    green = create(80, GREEN)
    blue = create(80, BLUE)
    white = create(80, WHITE)

    selected_color = None  # No color selected initially
    gravity_rules = {
        (YELLOW, YELLOW): 1,
        (YELLOW, BLUE): -2,
        (YELLOW, WHITE): -2,
        (YELLOW, GREEN): -2,
        (GREEN, GREEN): 1,
        (GREEN, WHITE): -2,
        (GREEN, YELLOW): -2,
        (GREEN, BLUE): -2,
        (BLUE, BLUE): 1,
        (BLUE, WHITE): -2,
        (BLUE, GREEN): -2,
        (BLUE, YELLOW): -2,
        (WHITE, WHITE): 1,
        (WHITE, YELLOW): -2,
        (WHITE, GREEN): -2,
        (WHITE, BLUE): -2,
    }

    run = True
    while run:
        clock.tick(60)
        WIN.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    selected_color = YELLOW
                elif event.key == pygame.K_b:
                    selected_color = BLUE
                elif event.key == pygame.K_g:
                    selected_color = GREEN
                elif event.key == pygame.K_w:
                    selected_color = WHITE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_color is not None:
                    for color, particle_group in [(YELLOW, yellow), (GREEN, green), (BLUE, blue), (WHITE, white)]:
                        if color != selected_color:
                            if event.button == 1:  # Left click
                                gravity_rules[(selected_color, color)] = -1
                            elif event.button == 3:  # Right click
                                gravity_rules[(selected_color, color)] = 1

        rule(yellow, yellow, gravity_rules[(YELLOW, YELLOW)])
        rule(yellow, blue, gravity_rules[(YELLOW, BLUE)])
        rule(yellow, white, gravity_rules[(YELLOW, WHITE)])
        rule(yellow, green, gravity_rules[(YELLOW, GREEN)])

        rule(green, green, gravity_rules[(GREEN, GREEN)])
        rule(green, white, gravity_rules[(GREEN, WHITE)])
        rule(green, yellow, gravity_rules[(GREEN, YELLOW)])
        rule(green, blue, gravity_rules[(GREEN, BLUE)])
        
        rule(blue, blue, gravity_rules[(BLUE, BLUE)])
        rule(blue, white, gravity_rules[(BLUE, WHITE)])
        rule(blue, green, gravity_rules[(BLUE, GREEN)])
        rule(blue, yellow, gravity_rules[(BLUE, YELLOW)])
        
        rule(white, white, gravity_rules[(WHITE, WHITE)])
        rule(white, yellow, gravity_rules[(WHITE, YELLOW)])
        rule(white, green, gravity_rules[(WHITE, GREEN)])
        rule(white, blue, gravity_rules[(WHITE, BLUE)])

        for group in particles:
            for particle in group:
                particle.draw(WIN)

        pygame.display.update()

    pygame.quit()

main(particles)

