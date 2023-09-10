import pygame
import random
import math

HEIGHT, WIDTH = 300, 300
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Simulation")

BACKGROUND = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOWAMOUNT = 100
GREENAMOUNT = 100
BLUEAMOUNT = 100
WHITEAMOUNT = 100

FRICTION = 0.90
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
            a.x = -WIDTH // 2
            a.x_vel *= -1
        elif a.x > WIDTH // 2:
            a.x = WIDTH // 2
            a.x_vel *= -1
        if a.y < -HEIGHT // 2:
            a.y = -HEIGHT // 2
            a.y_vel *= -1
        elif a.y > HEIGHT // 2:
            a.y = HEIGHT // 2
            a.y_vel *= -1

def main(particles, seed):
    clock = pygame.time.Clock()
    random.seed(seed)

    yellow = create(YELLOWAMOUNT, YELLOW)
    green = create(GREENAMOUNT, GREEN)
    blue = create(BLUEAMOUNT, BLUE)
    white = create(WHITEAMOUNT, WHITE)

    selected_color_1 = None
    selected_color_2 = None
    gravity_rules = {
        (YELLOW, YELLOW): -.5,
        (YELLOW, BLUE): 0,
        (YELLOW, WHITE): -1,
        (YELLOW, GREEN): 1,
        (GREEN, GREEN): -.5,
        (GREEN, WHITE): 0,
        (GREEN, YELLOW): -1,
        (GREEN, BLUE): 1,
        (BLUE, BLUE): -.5,
        (BLUE, WHITE): 1,
        (BLUE, GREEN): -1,
        (BLUE, YELLOW): 0,
        (WHITE, WHITE): -.5,
        (WHITE, YELLOW): 1,
        (WHITE, GREEN): 0,
        (WHITE, BLUE): -1,
    }

    color_dict = {
        YELLOW: 'Yellow',
        GREEN: 'Green',
        BLUE: 'Blue',
        WHITE: 'White',
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
                    if selected_color_1 is None:
                        selected_color_1 = YELLOW
                    else:
                        selected_color_2 = YELLOW
                elif event.key == pygame.K_b:
                    if selected_color_1 is None:
                        selected_color_1 = BLUE
                    else:
                        selected_color_2 = BLUE
                elif event.key == pygame.K_g:
                    if selected_color_1 is None:
                        selected_color_1 = GREEN
                    else:
                        selected_color_2 = GREEN
                elif event.key == pygame.K_w:
                    if selected_color_1 is None:
                        selected_color_1 = WHITE
                    else:
                        selected_color_2 = WHITE
                elif event.key == pygame.K_SPACE:
                    if selected_color_1 is not None and selected_color_2 is not None:
                        gravity_rules[(selected_color_1, selected_color_2)] *= -1
                        print(f"Rule changed for ({color_dict[selected_color_1]}, {color_dict[selected_color_2]}): {gravity_rules[(selected_color_1, selected_color_2)]}")
                        selected_color_1 = None
                        selected_color_2 = None
                elif event.key == pygame.K_RETURN:
                    if selected_color_1 is not None and selected_color_2 is None:
                        try:
                            value = float(input(f"Enter gravity value for {color_dict[selected_color_1]} (-1 to 1): "))
                            if -1 <= value <= 1:
                                gravity_rules[(selected_color_1, selected_color_1)] = value
                                print(f"Gravity changed for {color_dict[selected_color_1]}: {value}")
                            else:
                                print("Invalid gravity value. Please enter a value between -1 and 1.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    elif selected_color_1 is not None and selected_color_2 is not None:
                        print("Please input gravity value for the selected colors (-1 to 1): ")
                        try:
                            value = float(input())
                            if -1 <= value <= 1:
                                gravity_rules[(selected_color_1, selected_color_2)] = value
                                gravity_rules[(selected_color_2, selected_color_1)] = value
                                print(f"Gravity changed for ({color_dict[selected_color_1]}, {color_dict[selected_color_2]}): {value}")
                                selected_color_1 = None
                                selected_color_2 = None
                            else:
                                print("Invalid gravity value. Please enter a value between -1 and 1.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

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

        # Displaying text on the screen
        if selected_color_1 is not None:
            selected_color_1_text = pygame.font.SysFont(None, 50).render(str(selected_color_1), True, selected_color_1)
            WIN.blit(selected_color_1_text, (10, 10))

        if selected_color_2 is not None:
            selected_color_2_text = pygame.font.SysFont(None, 50).render(str(selected_color_2), True, selected_color_2)
            WIN.blit(selected_color_2_text, (10, 70))

        pygame.display.update()

    pygame.quit()

main(particles, 1)

