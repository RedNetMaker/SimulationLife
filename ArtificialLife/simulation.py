import tkinter as tk
import random
from collections import defaultdict

BASE_CELL_SIZE = 5
GRID_SIZE = 100

EMPTY = 0
ORGANIC = 1
BOT = 2

COLORS = {
    EMPTY: "white",
    ORGANIC: "green",
    BOT: "red"
}

class Bot:
    def __init__(self, x, y, energy=100):
        self.x = x
        self.y = y
        self.energy = energy
        self.age = 0
        
    def move(self, grid):
        # Простое случайное движение для примера
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = (self.x + dx) % GRID_SIZE
        new_y = (self.y + dy) % GRID_SIZE
        
        if grid[new_y][new_x] == EMPTY:
            self.x = new_x
            self.y = new_y
            self.energy -= 1
            self.age += 1

class CellGrid:
    def __init__(self, root):
        self.root = root
        self.grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.bots = []
        self.bot_positions = defaultdict(list)
        self.zoom_level = 1.0
        self.base_cell_size = BASE_CELL_SIZE
        
        # GUI setup
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.hscroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vscroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hscroll.set, yscrollcommand=self.vscroll.set)
        
        self.hscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        self.canvas.bind("<Button-4>", lambda e: self.on_zoom(e, 1))
        self.canvas.bind("<Button-5>", lambda e: self.on_zoom(e, -1))
        
        self.rects = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.redraw_grid()
        
        # Запуск цикла обновления
        self.update_bots()

    def get_cell_size(self):
        return max(1, int(self.base_cell_size * self.zoom_level))

    def redraw_grid(self):
        cell_size = self.get_cell_size()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = COLORS[self.grid[y][x]]
                x0 = x * cell_size
                y0 = y * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                
                if self.rects[y][x] is None:
                    self.rects[y][x] = self.canvas.create_rectangle(x0, y0, x1, y1, 
                                                                   fill=color, outline="black")
                else:
                    self.canvas.coords(self.rects[y][x], x0, y0, x1, y1)
                    self.canvas.itemconfig(self.rects[y][x], fill=color)
                    
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_grid_state(self):
        # Обновляем состояние сетки на основе позиций ботов
        self.grid = [[ORGANIC if random.random() < 0.01 else EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.bot_positions.clear()
        
        for bot in self.bots:
            if 0 <= bot.x < GRID_SIZE and 0 <= bot.y < GRID_SIZE:
                self.grid[bot.y][bot.x] = BOT
                self.bot_positions[(bot.x, bot.y)].append(bot)

    def on_zoom(self, event, delta=None):
        # Аналогично предыдущей реализации
        pass

    def on_click(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        cell_size = self.get_cell_size()
        
        grid_x = int(x // cell_size)
        grid_y = int(y // cell_size)
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            # Добавляем нового бота по клику
            new_bot = Bot(grid_x, grid_y)
            self.bots.append(new_bot)
            self.update_grid_state()
            self.redraw_cell(grid_x, grid_y)

    def update_bots(self):
        # Основной цикл обновления
        for bot in self.bots:
            old_x, old_y = bot.x, bot.y
            bot.move(self.grid)
            
            # Обновляем отображение старых и новых позиций
            if (old_x, old_y) != (bot.x, bot.y):
                self.redraw_cell(old_x, old_y)
                self.redraw_cell(bot.x, bot.y)
        
        self.update_grid_state()
        self.root.after(100, self.update_bots)  # Обновление каждые 100 мс

    def redraw_cell(self, x, y):
        cell_size = self.get_cell_size()
        color = COLORS[self.grid[y][x]]
        
        x0 = x * cell_size
        y0 = y * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size
        
        self.canvas.coords(self.rects[y][x], x0, y0, x1, y1)
        self.canvas.itemconfig(self.rects[y][x], fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bot Simulation")
    app = CellGrid(root)
    
    # Добавляем начальных ботов
    for _ in range(50):
        x = random.randint(0, GRID_SIZE-1)
        y = random.randint(0, GRID_SIZE-1)
        app.bots.append(Bot(x, y))
    
    root.mainloop()