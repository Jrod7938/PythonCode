import pygame
import random
from collections import deque
import numpy as np

# Parameters
WIDTH = 900
HEIGHT = 850
CELL_SIZE = 13
GRID_SIZE_X = WIDTH // CELL_SIZE
GRID_SIZE_Y = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
LIGHT_RED = (255, 100, 100)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze Generator')
clock = pygame.time.Clock()

# Initialize the grid using NumPy
grid = np.zeros((GRID_SIZE_Y, GRID_SIZE_X), dtype=int)

def reset_grid():
    grid.fill(0)
    return grid

def get_neighbors(x, y):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < GRID_SIZE_X and 0 <= ny < GRID_SIZE_Y:
            neighbors.append((nx, ny, dx, dy))
    return neighbors

def draw_grid():
    screen.fill(BLACK)
    for y in range(GRID_SIZE_Y):
        for x in range(GRID_SIZE_X):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell_value = grid[y][x]
            if cell_value == 0:
                pygame.draw.rect(screen, BLACK, rect)
            elif cell_value == 1:
                pygame.draw.rect(screen, WHITE, rect)
            elif cell_value == 2:
                pygame.draw.rect(screen, LIGHT_BLUE, rect)
            elif cell_value == 3:
                pygame.draw.rect(screen, GREEN, rect)
            elif cell_value == 4:
                pygame.draw.rect(screen, LIGHT_RED, rect)
    pygame.display.flip()

def generate_maze(x, y):
    stack = deque([(x, y)])
    grid[y][x] = 1
    paused = False
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            current_x, current_y = stack[-1]
            grid[current_y][current_x] = 2
            draw_grid()

            neighbors = get_neighbors(current_x, current_y)
            random.shuffle(neighbors)
            next_cell = None
            for nx, ny, dx, dy in neighbors:
                if grid[ny][nx] == 0:
                    next_cell = (nx, ny, dx, dy)
                    break

            if next_cell is None:
                stack.pop()
                if stack:
                    grid[current_y][current_x] = 1
                    draw_grid()
            else:
                nx, ny, dx, dy = next_cell
                stack.append((nx, ny))
                grid[ny][nx] = 1
                grid[current_y + dy][current_x + dx] = 1

def bfs_solve(start, end):
    queue = deque([(start)])
    visited = set([start])
    path = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break

        cx, cy = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            neighbor = (nx, ny)

            if 0 <= nx < GRID_SIZE_X and 0 <= ny < GRID_SIZE_Y and grid[ny][nx] != 0 and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path[neighbor] = current
                if grid[ny][nx] == 1:
                    grid[ny][nx] = 2
                    draw_grid()
                    clock.tick(60)

    if end in path:
        current = end
        while current != start:
            cx, cy = current
            grid[cy][cx] = 4
            current = path[current]

        draw_grid()

def dfs_solve(start, end):
    stack = deque([(start)])
    visited = set([start])
    path = {start: None}

    while stack:
        current = stack.pop()
        if current == end:
            break

        cx, cy = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            neighbor = (nx, ny)

            if 0 <= nx < GRID_SIZE_X and 0 <= ny < GRID_SIZE_Y and grid[ny][nx] != 0 and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                path[neighbor] = current
                if grid[ny][nx] == 1:
                    grid[ny][nx] = 2
                    draw_grid()
                    clock.tick(60)

    if end in path:
        current = end
        while current != start:
            cx, cy = current
            grid[cy][cx] = 4
            current = path[current]

        draw_grid()
    

def main():
    running = True
    maze_started = False
    start_placed = False
    end_placed = False
    start = None
    end = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not maze_started:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if grid[grid_y][grid_x] == 0:
                        maze_started = True
                        generate_maze(grid_x, grid_y)
                        draw_grid()
                elif not start_placed:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if grid[grid_y][grid_x] == 1:
                        start = (grid_x, grid_y)
                        grid[grid_y][grid_x] = 3
                        draw_grid()
                        start_placed = True
                elif not end_placed:
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if grid[grid_y][grid_x] == 1:
                        end = (grid_x, grid_y)
                        grid[grid_y][grid_x] = 4
                        draw_grid()
                        end_placed = True
                        bfs_solve(start, end)
            

        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()

