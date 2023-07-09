import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen and cell parameters
width, height = 900, 900
cell_size = 5
num_cells_x = width // cell_size
num_cells_y = height // cell_size

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY_BLUE = (100, 100, 150)
GREY_GREEN = (100, 150, 100)

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cellular Automaton - Langton's Ant Modified")
clock = pygame.time.Clock()

def initialize_cells():
    return np.zeros((num_cells_x, num_cells_y), dtype=int)

def draw_cells(cells):
    for x in range(num_cells_x):
        for y in range(num_cells_y):
            color = BLACK if cells[x, y] == 0 else WHITE if cells[x, y] == 1 else GREY_BLUE if cells[x, y] == 2 else GREY_GREEN
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

class Ant:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def move(self, cells):
        if cells[self.x, self.y] == 0:  # On a black cell, turn right
            self.direction = (self.direction + 1) % 4
            cells[self.x, self.y] = 1
        elif cells[self.x, self.y] == 1:  # On a white cell, turn right
            self.direction = (self.direction + 1) % 4
            cells[self.x, self.y] = 2
        elif cells[self.x, self.y] == 2:  # On a grey blue cell, turn left
            self.direction = (self.direction - 1) % 4
            cells[self.x, self.y] = 3
        else: # On a grey green cell, turn left
            self.direction = (self.direction - 1) % 4
            cells[self.x, self.y] = 0


        if self.direction == 0:
            self.y = (self.y - 1) % num_cells_y
        elif self.direction == 1:
            self.x = (self.x + 1) % num_cells_x
        elif self.direction == 2:
            self.y = (self.y + 1) % num_cells_y
        else:
            self.x = (self.x - 1) % num_cells_x


def draw_ant(x, y):
    pygame.draw.rect(screen, RED, (x * cell_size, y * cell_size, cell_size, cell_size))

def main():
    cells = initialize_cells()
    ants = []
    running = True
    paused = True

    while running:
        screen.fill(BLACK)
        draw_cells(cells)

        for ant in ants:
            if not paused:
                ant.move(cells)
            draw_ant(ant.x, ant.y)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    ant_x, ant_y = x // cell_size, y // cell_size
                    ants.append(Ant(ant_x, ant_y, 0))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    cells = initialize_cells()
                    ants = []
                    paused = True

        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()
