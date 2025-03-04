import random

class Bot:
    brain = [26 for x in range(64)]
    counter = 0


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])  # Вправо, вниз, влево, вверх

    def move(self, occupied_positions):
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]
        
        if (new_x, new_y) not in occupied_positions and 0 <= new_x < 100 and 0 <= new_y < 100:
            self.x, self.y = new_x, new_y
        else:
            self.change_direction()

    def change_direction(self):
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])