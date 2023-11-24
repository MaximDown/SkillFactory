import random


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, bow, length, direction):
        self.bow = bow
        self.length = length
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            if self.direction == 0:
                ship_dot = Dot(self.bow.x + i, self.bow.y)
            else:
                ship_dot = Dot(self.bow.x, self.bow.y + i)
            ship_dots.append(ship_dot)
        return ship_dots


class Board:
    def __init__(self, hid):
        self.size = 6
        self.field = [['O' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []
        self.hid = hid
        self.alive_ships = 0  # количество кораблей на доске

    def add_ship(self, ship):
        # Входит ли корабль на поле
        for dot in ship.dots():
            if self.out(dot):
                return False

        # Накладывается ли на существующие корабли или их контур
        for existing_ship in self.ships:
            for dot in ship.dots():
                for existing_dot in existing_ship.dots():
                    if abs(dot.x - existing_dot.x) <= 1 and abs(dot.y - existing_dot.y) <= 1:
                        return False

        for dot in ship.dots():
            self.field[dot.x][dot.y] = '■'
        self.ships.append(ship)
        self.alive_ships += 1  # Увеличиваем количество живых кораблей после успешного добавления
        return True  # Возвращаем True, чтобы показать успешное добавление корабля


    # Выход за поле
    def out(self, dot):
        if not (0 <= dot.x < 6 and 0 <= dot.y < 6):
            return True
        else:
            return False


    def display(self):
        header = "   | 0 | 1 | 2 | 3 | 4 | 5 |"
        separator = "-" * len(header)

        print(header)
        print(separator)

        for y in range(self.size):
            row_display = f"{y:2} | "
            for x in range(self.size):
                row_display += f"{self.field[x][y]} | "
            print(row_display)

        print(separator)
        print("\n")


class Game:
    def __init__(self):
        self.user_board = Board(hid=False)
        self.ai_board = Board(hid=True)


    def random_board(self, board):
        ship_lengths = [3, 2, 2, 1, 1, 1, 1]
        for length in ship_lengths:
            placed = False  # Флаг, обозначающий успешное размещение корабля
            attempts_add = 0
            while not placed:
                if attempts_add == 3:
                    return False # Неудача после 3 попыток разместить. Будет пересоздана доска
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                if board.field[x][y] != '■':
                    direction = random.choice([0, 1])
                    new_ship = Ship(Dot(x, y), length, direction)
                    success_add = board.add_ship(new_ship)
                    if success_add:
                        placed = True
                    else:
                        attempts_add += 1


    # Выстрел
    def shot(self, board, dot):
        if board.field[dot.x][dot.y] == '■':  # Цель есть
            for ship in board.ships:
                for ship_dot in ship.dots():
                    if ship_dot == dot:
                        board.field[dot.x][dot.y] = 'X'  # Помечаем попадание 'Х'
                        ship.lives -= 1
                        if ship.lives == 0:
                            board.alive_ships -= 1
                            return ["kill", board]
                        else:
                            return ["hit", board]
        elif board.field[dot.x][dot.y] == 'O':  # Пустое поле
            board.field[dot.x][dot.y] = 'T'  # Помечаем промах 'T'
            return ["miss", board]
        else:
            return ["repeat", board]


    # Приветствие
    def greet(self):
        print("Добро пожаловать в Морской бой!")
        print("Генерируем доски, подождите")


    # Ход игры
    def loop(self):
        print("Начнем игру\n")
        while True:
            print("Доска игрока:")
            self.user_board.display()
            print("Доска противника:")
            self.ai_board.display()
            print("Ваш ход:")

            while True:
                user_shot = self.ask("player")
                res_user_shot = self.shot(self.ai_board, user_shot)
                if res_user_shot[0] == "hit":
                    print(f"\nВы попали в корабль противника! ({user_shot.x},{user_shot.y})")
                    self.ai_board = res_user_shot[1]
                    break
                elif res_user_shot[0] == "kill":
                    print(f"\nВы убили корабль противника! ({user_shot.x},{user_shot.y})")
                    self.ai_board = res_user_shot[1]
                    break
                elif res_user_shot[0] == "miss":
                    print(f"\nВы промахнулись! ({user_shot.x},{user_shot.y})")
                    self.ai_board = res_user_shot[1]
                    break
                elif res_user_shot[0] == "repeat":
                    print(f"\nСюда уже стреляли! ({user_shot.x},{user_shot.y}) Попробуйте ещё\n")

            while True:
                ai_shot = self.ask("ai")
                res_ai_shot = self.shot(self.user_board, ai_shot)
                if res_ai_shot[0] == "hit":
                    print(f"\nПротивник попал по Вашему кораблю! ({ai_shot.x},{ai_shot.y})\n")
                    self.user_board = res_ai_shot[1]
                    break
                elif res_ai_shot[0] == "kill":
                    print(f"\nПротивник убил Ваш корабль! ({ai_shot.x},{ai_shot.y})\n")
                    self.user_board = res_ai_shot[1]
                    break
                elif res_ai_shot[0] == "miss":
                    print(f"\nПротивник промахнулся! ({ai_shot.x},{ai_shot.y})\n")
                    self.user_board = res_ai_shot[1]
                    break

            if self.user_board.alive_ships == 0:
                print("Противник победил. Удачи в следующий раз\n")
                print("Доска противника:")
                self.ai_board.display()
                break
            elif self.ai_board.alive_ships == 0:
                print("Поздравляем! Вы победили!\n")
                print("Доска противника:")
                self.ai_board.display()
                break


    # Старт игры
    def start(self):
        while True:
            self.random_board(self.user_board)
            self.random_board(self.ai_board)

            if self.user_board.alive_ships == 7 and self.ai_board.alive_ships == 7:
                break


    def ask(self, gamer):
        if gamer == "player":
            while True:
                try:
                    x = int(input("Введите координату X (0-5): "))
                    y = int(input("Введите координату Y (0-5): "))
                    if 0 <= x <= 5 and 0 <= y <= 5:
                        return Dot(x, y)
                    else:
                        print("Координаты вне диапазона. Введите координаты от 0 до 5.")
                except ValueError:
                    print("Неверный ввод! Пожалуйста, введите число.")
        elif gamer == "ai":
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            return Dot(x, y)

if __name__ == "__main__":
    game = Game()
    game.greet()
    game.start()
    game.loop()
