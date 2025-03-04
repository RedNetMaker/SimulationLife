# Обьект бота, хранящий все нужные данные
class Bot:
    # Адрес текущей команды
    adr = 0
    # Положение бота
    x = 0
    y = 0
    # Кол-во жизней
    health = 0
    # Кол-во минералов
    mineral = 0
    # Тип бота: 0-Пусто, 1-Органика, 2-Органика движется, 3-Живой, 4-Многоклеточное
    living = 0
    # Цвет бота
    c_red = 0
    c_green = 0
    c_blue = 0
    # Направление
    direct = 0
    # Id предыдущего и следующего бота
    prev = 0
    next = 0
    # Id предыдущего и следующего бота в многоклеточной цепочке
    mprev = 0
    mnext = 0

    def __init__(self, bot_mind_size):
        pass

    # Функция фотосинтеза
    def eat_sun(self, season):
        if self.mineral < 100:
            t = 0
        elif self.mineral < 400:
            t = 1
        else:
            t = 2

        hlt = season - ((self.y - 1) / 6) + t

        if hlt > 0:
            self.health += hlt

    

    