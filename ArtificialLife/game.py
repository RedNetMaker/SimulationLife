import pygame
from bots import Bot
import random

# Константы
WIDTH, HEIGHT = 500, 500
CELL_SIZE = WIDTH // 100
BOT_COUNT = 500

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Создаём ботов
bots = [Bot(random.randint(0, 99), random.randint(0, 99)) for _ in range(BOT_COUNT)]

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

def main():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_grid()
        
        occupied_positions = {(bot.x, bot.y) for bot in bots}
        for bot in bots:
            bot.move(occupied_positions)
            pygame.draw.rect(screen, (0, 255, 0), (bot.x * CELL_SIZE, bot.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        clock.tick(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
