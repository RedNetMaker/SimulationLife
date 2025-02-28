import random

# Константы
WC_EMPTY = 0
WC_WALL = 1
LV_ORGANIC_HOLD = 0
LV_ORGANIC_SINK = 1
LV_ALIVE = 2
MIND_SIZE = 64
MAX_CYCLES = 15

# Глобальные переменные
bots = {}  # Словарь для хранения данных о ботах
world = {}  # Словарь для хранения мира (координаты и боты)
season = 10  # Условный параметр для фотосинтеза

# Вспомогательные функции
def mod(a, b):
    return a % b

def rand():
    return random.randint(0, 1000)

def find_empty():
    # Находим свободный индекс для нового бота
    for i in range(1, 1000):
        if i not in bots:
            return i
    return -1

def find_empty_direction(bot):
    # Находим свободное направление для перемещения
    for i in range(8):
        x = X_from_vektor_r(bot, i)
        y = Y_from_vektor_r(bot, i)
        if world.get((x, y), WC_EMPTY) == WC_EMPTY:
            return i
    return 8  # Все направления заняты

def X_from_vektor_r(bot, direction):
    # Вычисляем координату X для относительного направления
    x = bots[bot]['X_COORD']
    if direction in [0, 1, 7]:
        return x + 1
    elif direction in [3, 4, 5]:
        return x - 1
    return x

def Y_from_vektor_r(bot, direction):
    # Вычисляем координату Y для относительного направления
    y = bots[bot]['Y_COORD']
    if direction in [1, 2, 3]:
        return y + 1
    elif direction in [5, 6, 7]:
        return y - 1
    return y

def X_from_vektor_a(bot, direction):
    # Вычисляем координату X для абсолютного направления
    x = bots[bot]['X_COORD']
    if direction in [0, 1, 7]:
        return x + 1
    elif direction in [3, 4, 5]:
        return x - 1
    return x

def Y_from_vektor_a(bot, direction):
    # Вычисляем координату Y для абсолютного направления
    y = bots[bot]['Y_COORD']
    if direction in [1, 2, 3]:
        return y + 1
    elif direction in [5, 6, 7]:
        return y - 1
    return y

def is_relative(bot1, bot2):
    # Проверяем, являются ли боты родственниками
    return 1 if bots[bot1]['MNEXT'] == bot2 or bots[bot1]['MPREV'] == bot2 else 0

def isMulti(bot):
    # Проверяем, является ли бот частью многоклеточной цепочки
    if bots[bot]['MPREV'] == 0 and bots[bot]['MNEXT'] == 0:
        return 0
    elif bots[bot]['MPREV'] != 0 and bots[bot]['MNEXT'] != 0:
        return 3
    elif bots[bot]['MPREV'] != 0:
        return 1
    else:
        return 2

def bot_inc_command_address(bot, value):
    # Увеличиваем адрес команды
    bots[bot]['ADR'] = (bots[bot]['ADR'] + value) % MIND_SIZE

def bot_indirect_inc_cmd_address(bot, value):
    # Увеличиваем адрес команды на значение параметра
    bots[bot]['ADR'] = (bots[bot]['ADR'] + bots[bot][bots[bot]['ADR'] + 1 + value]) % MIND_SIZE

def bot_get_param(bot):
    # Получаем параметр команды
    return bots[bot][bots[bot]['ADR'] + 1]

def bot_eat_sun(bot):
    # Фотосинтез
    if bots[bot]['MINERAL'] < 100:
        t = 0
    elif bots[bot]['MINERAL'] < 400:
        t = 1
    else:
        t = 2
    hlt = season - ((bots[bot]['Y_COORD'] - 1) // 6 + t)
    if hlt > 0:
        bots[bot]['HEALTH'] += hlt
        go_GREEN(bot, hlt)

def bot_mineral2energy(bot):
    # Преобразование минералов в энергию
    if bots[bot]['MINERAL'] > 100:
        bots[bot]['MINERAL'] -= 100
        bots[bot]['HEALTH'] += 400
        go_BLUE(bot, 100)
    else:
        go_BLUE(bot, bots[bot]['MINERAL'])
        bots[bot]['HEALTH'] += 4 * bots[bot]['MINERAL']
        bots[bot]['MINERAL'] = 0

def bot_move(bot, dr, ra):
    # Перемещение бота
    if ra == 0:
        x = X_from_vektor_r(bot, dr)
        y = Y_from_vektor_r(bot, dr)
    else:
        x = X_from_vektor_a(bot, dr)
        y = Y_from_vektor_a(bot, dr)
    if world.get((x, y), WC_EMPTY) == WC_EMPTY:
        move_bot(bot, x, y)
        return 2
    elif world.get((x, y), WC_EMPTY) == WC_WALL:
        return 3
    elif bots[world[(x, y)]]['LIVING'] <= LV_ORGANIC_SINK:
        return 4
    elif is_relative(bot, world[(x, y)]):
        return 6
    else:
        return 5

def bot_eat(bot, dr, ra):
    # Бот ест органику или другого бота
    bots[bot]['HEALTH'] -= 4
    if ra == 0:
        x = X_from_vektor_r(bot, dr)
        y = Y_from_vektor_r(bot, dr)
    else:
        x = X_from_vektor_a(bot, dr)
        y = Y_from_vektor_a(bot, dr)
    if world.get((x, y), WC_EMPTY) == WC_EMPTY:
        return 2
    elif world.get((x, y), WC_EMPTY) == WC_WALL:
        return 3
    elif bots[world[(x, y)]]['LIVING'] <= LV_ORGANIC_SINK:
        delete_bot(world[(x, y)])
        bots[bot]['HEALTH'] += 100
        go_RED(bot, 100)
        return 4
    else:
        min0 = bots[bot]['MINERAL']
        min1 = bots[world[(x, y)]]['MINERAL']
        hl = bots[world[(x, y)]]['HEALTH']
        if min0 >= min1:
            bots[bot]['MINERAL'] = min0 - min1
            delete_bot(world[(x, y)])
            cl = 100 + (hl // 2)
            bots[bot]['HEALTH'] += cl
            go_RED(bot, cl)
            return 5
        else:
            bots[bot]['MINERAL'] = 0
            min1 = min1 - min0
            if bots[bot]['HEALTH'] >= 2 * min1:
                delete_bot(world[(x, y)])
                cl = 100 + (hl // 2) - 2 * min1
                bots[bot]['HEALTH'] += cl
                go_RED(bot, cl)
                return 5
            else:
                bots[world[(x, y)]]['MINERAL'] = min1 - (bots[bot]['HEALTH'] // 2)
                bots[bot]['HEALTH'] = -10
                return 5

def bot_see_bots(bot, dr, ra):
    # Бот "смотрит" в направлении
    if ra == 0:
        wc = is_anything_there_r(bot, dr)
    else:
        wc = is_anything_there_a(bot, dr)
    if wc == WC_EMPTY:
        return 2
    elif wc == WC_WALL:
        return 3
    elif bots[wc]['LIVING'] <= LV_ORGANIC_SINK:
        return 4
    elif is_relative(bot, wc):
        return 6
    else:
        return 5

def bot_gen_attack(bot):
    # Генная атака
    x = X_from_vektor_r(bot, 0)
    y = Y_from_vektor_r(bot, 0)
    if bots[world[(x, y)]]['LIVING'] == LV_ALIVE:
        bots[bot]['HEALTH'] -= 10
        if bots[bot]['HEALTH'] > 0:
            ma = rand() // 520
            mc = rand() // 520
            bots[world[(x, y)]][ma] = mc

def bot_care(bot, dr, ra):
    # Бот делится энергией и минералами
    if ra == 0:
        x = X_from_vektor_r(bot, dr)
        y = Y_from_vektor_r(bot, dr)
    else:
        x = X_from_vektor_a(bot, dr)
        y = Y_from_vektor_a(bot, dr)
    if world.get((x, y), WC_EMPTY) == WC_EMPTY:
        return 2
    elif world.get((x, y), WC_EMPTY) == WC_WALL:
        return 3
    elif bots[world[(x, y)]]['LIVING'] <= LV_ORGANIC_SINK:
        return 4
    else:
        hlt0 = bots[bot]['HEALTH']
        hlt1 = bots[world[(x, y)]]['HEALTH']
        min0 = bots[bot]['MINERAL']
        min1 = bots[world[(x, y)]]['MINERAL']
        if hlt0 > hlt1:
            hlt = (hlt0 - hlt1) // 2
            bots[bot]['HEALTH'] -= hlt
            bots[world[(x, y)]]['HEALTH'] += hlt
        if min0 > min1:
            min = (min0 - min1) // 2
            bots[bot]['MINERAL'] -= min
            bots[world[(x, y)]]['MINERAL'] += min
        return 5

def bot_give(bot, dr, ra):
    # Бот отдает энергию и минералы
    if ra == 0:
        x = X_from_vektor_r(bot, dr)
        y = Y_from_vektor_r(bot, dr)
    else:
        x = X_from_vektor_a(bot, dr)
        y = Y_from_vektor_a(bot, dr)
    if world.get((x, y), WC_EMPTY) == WC_EMPTY:
        return 2
    elif world.get((x, y), WC_EMPTY) == WC_WALL:
        return 3
    elif bots[world[(x, y)]]['LIVING'] <= LV_ORGANIC_SINK:
        return 4
    else:
        hlt0 = bots[bot]['HEALTH']
        hlt = hlt0 // 4
        bots[bot]['HEALTH'] -= hlt
        bots[world[(x, y)]]['HEALTH'] += hlt
        min0 = bots[bot]['MINERAL']
        if min0 > 3:
            min = min0 // 4
            bots[bot]['MINERAL'] -= min
            bots[world[(x, y)]]['MINERAL'] += min
            if bots[world[(x, y)]]['MINERAL'] > 999:
                bots[world[(x, y)]]['MINERAL'] = 999
        return 5

def bot_double(bot):
    # Размножение бота
    bots[bot]['HEALTH'] -= 150
    if bots[bot]['HEALTH'] <= 0:
        return
    n = find_empty_direction(bot)
    if n == 8:
        bots[bot]['HEALTH'] = 0
        return
    newbot = find_empty()
    for i in range(MIND_SIZE):
        bots[newbot][i] = bots[bot][i]
    if rand() % 4 == 0:
        ma = rand() // 520
        mc = rand() // 520
        bots[newbot][ma] = mc
    bots[newbot]['ADR'] = 0
    bots[newbot]['HEALTH'] = bots[bot]['HEALTH'] // 2
    bots[bot]['HEALTH'] = bots[bot]['HEALTH'] // 2
    bots[newbot]['MINERAL'] = bots[bot]['MINERAL'] // 2
    bots[bot]['MINERAL'] = bots[bot]['MINERAL'] // 2
    bots[newbot]['X_COORD'] = X_from_vektor_r(bot, n)
    bots[newbot]['Y_COORD'] = Y_from_vektor_r(bot, n)
    world[(bots[newbot]['X_COORD'], bots[newbot]['Y_COORD'])] = newbot
    bots[newbot]['C_RED'] = bots[bot]['C_RED']
    bots[newbot]['C_BLUE'] = bots[bot]['C_BLUE']
    bots[newbot]['C_GREEN'] = bots[bot]['C_GREEN']
    bots[newbot]['LIVING'] = LV_ALIVE
    bots[newbot]['DIRECT'] = rand() % 8
    px = bots[bot]['PREV']
    bots[newbot]['PREV'] = px
    bots[px]['NEXT'] = newbot
    bots[newbot]['NEXT'] = bot
    bots[bot]['PREV'] = newbot
    bots[newbot]['MNEXT'] = 0
    bots[newbot]['MPREV'] = 0

def bot_multi(bot):
    # Создание многоклеточного бота
    pbot = bots[bot]['MPREV']
    nbot = bots[bot]['MNEXT']
    if pbot != 0 and nbot != 0:
        return
    bots[bot]['HEALTH'] -= 150
    if bots[bot]['HEALTH'] <= 0:
        return
    n = find_empty_direction(bot)
    if n == 8:
        bots[bot]['HEALTH'] = 0
        return
    newbot = find_empty()
    for i in range(MIND_SIZE):
        bots[newbot][i] = bots[bot][i]
    if rand() % 4 == 0:
        ma = rand() // 520
        mc = rand() // 520
        bots[newbot][ma] = mc
    bots[newbot]['ADR'] = 0
    bots[newbot]['HEALTH'] = bots[bot]['HEALTH'] // 2
    bots[bot]['HEALTH'] = bots[bot]['HEALTH'] // 2
    bots[newbot]['MINERAL'] = bots[bot]['MINERAL'] // 2
    bots[bot]['MINERAL'] = bots[bot]['MINERAL'] // 2
    bots[newbot]['X_COORD'] = X_from_vektor_r(bot, n)
    bots[newbot]['Y_COORD'] = Y_from_vektor_r(bot, n)
    world[(bots[newbot]['X_COORD'], bots[newbot]['Y_COORD'])] = newbot
    bots[newbot]['C_RED'] = bots[bot]['C_RED']
    bots[newbot]['C_BLUE'] = bots[bot]['C_BLUE']
    bots[newbot]['C_GREEN'] = bots[bot]['C_GREEN']
    bots[newbot]['LIVING'] = LV_ALIVE
    bots[newbot]['DIRECT'] = rand() % 8
    px = bots[bot]['PREV']
    bots[newbot]['PREV'] = px
    bots[px]['NEXT'] = newbot
    bots[newbot]['NEXT'] = bot
    bots[bot]['PREV'] = newbot
    if nbot == 0:
        bots[bot]['MNEXT'] = newbot
        bots[newbot]['MPREV'] = bot
        bots[newbot]['MNEXT'] = 0
    else:
        bots[bot]['MPREV'] = newbot
        bots[newbot]['MNEXT'] = bot
        bots[newbot]['MPREV'] = 0

def organic_down(bot):
    # Органика опускается вниз
    x = bots[bot]['X_COORD']
    y = bots[bot]['Y_COORD'] + 1
    if world.get((x, y), WC_EMPTY) == WC_EMPTY:
        world[(x, y - 1)] = WC_EMPTY
        world[(x, y)] = bot
        bots[bot]['Y_COORD'] = y
    else:
        bots[bot]['LIVING'] = LV_ORGANIC_HOLD

def generate_Adam():
    # Генерация первого бота
    bots[0] = {'NEXT': 1, 'PREV': 1}
    bots[1] = {
        'NEXT': 0, 'PREV': 0, 'C_RED': 170, 'C_BLUE': 170, 'C_GREEN': 170,
        'HEALTH': 990, 'MINERAL': 0, 'LIVING': LV_ALIVE, 'DIRECT': 5,
        'X_COORD': 90, 'Y_COORD': 48, 'MPREV': 0, 'MNEXT': 0
    }
    world[(90, 48)] = 1
    for i in range(MIND_SIZE):
        bots[1][i] = 25  # Команда фотосинтеза

# Основная функция
def bot_step(bot):
    if bots[bot]['LIVING'] == LV_ORGANIC_HOLD:
        return bots[bot]['NEXT']
    if bots[bot]['LIVING'] == LV_ORGANIC_SINK:
        organic_down(bot)
        return bots[bot]['NEXT']
    cyc = 0
    while cyc < MAX_CYCLES:
        cyc += 1
        command = bots[bot][bots[bot]['ADR']]
        if command == 23:  # Сменить направление относительно
            param = mod(bot_get_param(bot), 8)
            newdrct = bots[bot]['DIRECT'] + param
            if newdrct > 7:
                newdrct -= 8
            bots[bot]['DIRECT'] = newdrct
            bot_inc_command_address(bot, 2)
        elif command == 24:  # Сменить направление абсолютно
            bots[bot]['DIRECT'] = mod(bot_get_param(bot), 8)
            bot_inc_command_address(bot, 2)
        elif command == 25:  # Фотосинтез
            bot_eat_sun(bot)
            bot_inc_command_address(bot, 1)
            return bots[bot]['NEXT']
        elif command == 26:  # Шаг в относительном направлении
            if isMulti(bot) == 0:
                drct = mod(bot_get_param(bot), 8)
                bot_indirect_inc_cmd_address(bot, bot_move(bot, drct, 0))
            return bots[bot]['NEXT']
        elif command == 27:  # Шаг в абсолютном направлении
            if isMulti(bot) == 0:
                drct = mod(bot_get_param(bot), 8)
                bot_indirect_inc_cmd_address(bot, bot_move(bot, drct, 1))
            return bots[bot]['NEXT']
        elif command == 28:  # Съесть в относительном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_eat(bot, drct, 0))
            return bots[bot]['NEXT']
        elif command == 29:  # Съесть в абсолютном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_eat(bot, drct, 1))
            return bots[bot]['NEXT']
        elif command == 30:  # Посмотреть в относительном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_see_bots(bot, drct, 0))
        elif command == 31:  # Посмотреть в абсолютном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_see_bots(bot, drct, 1))
        elif command in [32, 42]:  # Делиться в относительном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_care(bot, drct, 0))
        elif command in [33, 51]:  # Делиться в абсолютном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_care(bot, drct, 1))
        elif command in [34, 50]:  # Отдать в относительном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_give(bot, drct, 0))
        elif command in [35, 52]:  # Отдать в абсолютном направлении
            drct = mod(bot_get_param(bot), 8)
            bot_indirect_inc_cmd_address(bot, bot_give(bot, drct, 1))
        elif command == 36:  # Выровняться по горизонтали
            if rand() % 2 == 0:
                bots[bot]['DIRECT'] = 3
            else:
                bots[bot]['DIRECT'] = 7
            bot_inc_command_address(bot, 1)
        elif command == 37:  # Проверить уровень
            param = bot_get_param(bot) * 1.5
            if bots[bot]['Y_COORD'] < param:
                bot_indirect_inc_cmd_address(bot, 2)
            else:
                bot_indirect_inc_cmd_address(bot, 3)
        elif command == 38:  # Проверить здоровье
            param = bot_get_param(bot) * 15
            if bots[bot]['HEALTH'] < param:
                bot_indirect_inc_cmd_address(bot, 2)
            else:
                bot_indirect_inc_cmd_address(bot, 3)
        elif command == 39:  # Проверить минералы
            param = bot_get_param(bot) * 15
            if bots[bot]['MINERAL'] < param:
                bot_indirect_inc_cmd_address(bot, 2)
            else:
                bot_indirect_inc_cmd_address(bot, 3)
        elif command == 40:  # Многоклеточность
            a = isMulti(bot)
            if a == 3:
                bot_double(bot)
            else:
                bot_multi(bot)
            bot_inc_command_address(bot, 1)
            return bots[bot]['NEXT']
        elif command == 41:  # Деление
            a = isMulti(bot)
            if a == 0 or a == 3:
                bot_double(bot)
            else:
                bot_multi(bot)
            bot_inc_command_address(bot, 1)
            return bots[bot]['NEXT']
        elif command == 43:  # Проверить, окружен ли бот
            bot_indirect_inc_cmd_address(bot, full_aroud(bot))
        elif command == 44:  # Проверить, прибавляется ли энергия
            bot_indirect_inc_cmd_address(bot, is_health_grow(bot))
        elif command == 45:  # Проверить, прибавляются ли минералы
            if bots[bot]['Y_COORD'] > 48:
                bot_indirect_inc_cmd_address(bot, 1)
            else:
                bot_indirect_inc_cmd_address(bot, 2)
        elif command == 46:  # Проверить, многоклеточный ли бот
            mu = isMulti(bot)
            if mu == 0:
                bot_indirect_inc_cmd_address(bot, 1)
            elif mu == 3:
                bot_indirect_inc_cmd_address(bot, 3)
            else:
                bot_indirect_inc_cmd_address(bot, 2)
        elif command == 47:  # Преобразовать минералы в энергию
            bot_mineral2energy(bot)
            bot_inc_command_address(bot, 1)
            return bots[bot]['NEXT']
        elif command == 48:  # Мутировать
            ma = rand() // 520
            mc = rand() // 520
            bots[bot][ma] = mc
            ma = rand() // 520
            mc = rand() // 520
            bots[bot][ma] = mc
            bot_inc_command_address(bot, 1)
            return bots[bot]['NEXT']
        elif command == 49:  # Генная атака
            bot_gen_attack(bot)
            bot_inc_command_address(bot, 1)
            return bots[bot]['NEXT']
        else:  # Безусловный переход
            bot_inc_command_address(bot, command)
    return bots[bot]['NEXT']

# Инициализация
generate_Adam()

# Пример запуска
current_bot = 1
while True:
    current_bot = bot_step(current_bot)
    if current_bot == 0:
        break