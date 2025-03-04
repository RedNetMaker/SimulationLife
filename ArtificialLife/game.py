import numpy as np
import pygame
import sys

# Инициализация pygame
pygame.init()

# Размер мира
world_width = 180
world_height = 96
# Размер мозга бота
bot_mind_size = 64
# Сезоны: 11-лето, 10-весна\осень, 9-зима
season = 11
season_max = 10
season_time = 0

# Создание мира
world = np.zeros((world_height, world_width))
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


CELL_SIZE = 4  # Размер клетки в пикселях
WINDOW_SIZE = (world_width * CELL_SIZE, world_height * CELL_SIZE) # Размеры окна и клетки
GRID_SIZE = (world_width, world_height)  # Размер сетки в клетках

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Grid Game")

def draw_grid():
    for y in range(GRID_SIZE[1]):
        for x in range(GRID_SIZE[0]):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# def color_cell(x, y, color):
#     if 0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1]:
#         grid[y][x] = color

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
            # color_cell(cell_x, cell_y, (255, 0, 0))

    # Отрисовка сетки
    screen.fill(WHITE)
    draw_grid()
    pygame.display.flip()

# Завершение работы
pygame.quit()
sys.exit()