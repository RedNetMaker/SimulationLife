import pygame
import sys

# Инициализация pygame
pygame.init()

# Размеры окна и клетки
WINDOW_SIZE = (500, 500)
CELL_SIZE = 8  # Размер клетки в пикселях
GRID_SIZE = (100, 100)  # Размер сетки в клетках

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Grid Game")

# Создание сетки
grid = [[WHITE for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]

def draw_grid():
    for y in range(GRID_SIZE[1]):
        for x in range(GRID_SIZE[0]):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def color_cell(x, y, color):
    if 0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1]:
        grid[y][x] = color

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Получение координат клетки при клике
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cell_x = mouse_x // CELL_SIZE
            cell_y = mouse_y // CELL_SIZE
            # Перекрашивание клетки в красный цвет при клике
            color_cell(cell_x, cell_y, (255, 0, 0))

    # Отрисовка сетки
    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()

# Завершение работы
pygame.quit()
sys.exit()