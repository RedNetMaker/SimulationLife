import pygame
import numpy as np
from world import World

# Константы
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
ZOOM_STEP = 1.2
MOVE_SPEED = 10
FONT_CACHE = {}

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Создание мира
world = World()

offset_x, offset_y = 0, 0
zoom = 1.0
running = True

while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                offset_x += MOVE_SPEED
            elif event.key == pygame.K_RIGHT:
                offset_x -= MOVE_SPEED
            elif event.key == pygame.K_UP:
                offset_y += MOVE_SPEED
            elif event.key == pygame.K_DOWN:
                offset_y -= MOVE_SPEED
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Прокрутка вверх (приближение)
                zoom *= ZOOM_STEP
            elif event.button == 5:  # Прокрутка вниз (отдаление)
                zoom /= ZOOM_STEP
    
    # Отрисовка сетки
    scaled_cell_size = int(CELL_SIZE * zoom)
    render_numbers = zoom > 2
    
    if render_numbers and scaled_cell_size not in FONT_CACHE:
        FONT_CACHE[scaled_cell_size] = pygame.font.Font(None, scaled_cell_size // 2)
    
    font = FONT_CACHE.get(scaled_cell_size, None)
    
    # Вычисление границ видимой области
    start_x = max(0, -offset_x // scaled_cell_size)
    start_y = max(0, -offset_y // scaled_cell_size)
    end_x = min(world.world_width, (WIDTH - offset_x) // scaled_cell_size + 1)
    end_y = min(world.world_height, (HEIGHT - offset_y) // scaled_cell_size + 1)
    
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            rect = pygame.Rect(
                x * scaled_cell_size + offset_x,
                y * scaled_cell_size + offset_y,
                scaled_cell_size, scaled_cell_size
            )
            
            color = (0, 255, 0) if world.world[y, x] != 0 else (100, 100, 100)
            pygame.draw.rect(screen, color, rect, 1)
            
            # Отображение чисел при достаточном масштабе
            if render_numbers and font:
                text_surface = font.render(str(world.world[y, x]), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
    
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
