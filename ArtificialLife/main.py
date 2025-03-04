import numpy as np

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

print(world)