import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1200, 800
GRID_SIZE = 100
CELL_SIZE = 8
ZOOM_FACTOR = 1.1
MIN_CELL_SIZE_FOR_TEXT = 20  # Минимальный размер ячейки для отображения текста

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid with Numbers")

# Сетка и массив чисел
grid = [[WHITE for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
numbers = [[random.randint(0, 9999) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
show_numbers = False  # Флаг для отображения чисел

# Параметры камеры
camera_x, camera_y = 0, 0
zoom = 1.0

# Кэширование шрифта и текста
font = pygame.font.SysFont(None, 24)  # Шрифт для чисел
text_cache = {}  # Кэш для отрендеренных текстов

# Функция для получения отрендеренного текста
def get_rendered_text(number):
    if number not in text_cache:
        text_cache[number] = font.render(str(number), True, BLACK)
    return text_cache[number]

# Функция для отрисовки сетки
def draw_grid():
    # Определяем видимую область сетки
    start_x = max(0, int(-camera_x / (CELL_SIZE * zoom)))
    start_y = max(0, int(-camera_y / (CELL_SIZE * zoom)))
    end_x = min(GRID_SIZE, int((WIDTH - camera_x) / (CELL_SIZE * zoom)) + 1)
    end_y = min(GRID_SIZE, int((HEIGHT - camera_y) / (CELL_SIZE * zoom)) + 1)

    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            rect = pygame.Rect(
                (x * CELL_SIZE * zoom + camera_x, y * CELL_SIZE * zoom + camera_y),
                (CELL_SIZE * zoom, CELL_SIZE * zoom)
            )
            pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            # Отображаем текст только если ячейка достаточно большая
            if show_numbers and CELL_SIZE * zoom >= MIN_CELL_SIZE_FOR_TEXT:
                text_surface = get_rendered_text(numbers[y][x])
                screen.blit(text_surface, (rect.x + 2, rect.y + 2))

# Функция для отрисовки кнопки
def draw_button():
    button_width = WIDTH // 10
    button_height = HEIGHT // 10
    rect = pygame.Rect(
        (WIDTH - button_width, HEIGHT - button_height),
        (button_width, button_height)
    )
    pygame.draw.rect(screen, BUTTON_COLOR, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Show", True, BLACK)
    screen.blit(text, (rect.x + 10, rect.y + 10))

# Основной цикл
running = True
dragging = False
last_mouse_pos = (0, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                x, y = event.pos
                # Проверка, что клик на кнопке
                if x >= WIDTH - WIDTH // 10 and y >= HEIGHT - HEIGHT // 10:
                    show_numbers = not show_numbers  # Переключаем отображение чисел
                else:
                    dragging = True
                    last_mouse_pos = event.pos
            elif event.button == 4:  # Колесо мыши вверх
                zoom *= ZOOM_FACTOR
            elif event.button == 5:  # Колесо мыши вниз
                zoom /= ZOOM_FACTOR
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                camera_x += dx
                camera_y += dy
                last_mouse_pos = event.pos

    screen.fill(WHITE)
    draw_grid()
    draw_button()
    pygame.display.flip()

pygame.quit()
sys.exit()