import numpy as np

class World:
    # Размер мира
    world_width = 180
    world_height = 96
    # Размер мозга бота
    bot_mind_size = 64
    # Сезоны: 11-лето, 10-весна\осень, 9-зима
    season = 11
    season_max = 10
    season_time = 0

    def __init__(self):
        self.world = np.zeros((self.world_height, self.world_width))

        self.world[10][20] = 1
        self.world[30][40] = 1
        self.world[50][60] = 1