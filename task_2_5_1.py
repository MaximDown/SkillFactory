import random

class Ship:
    def __init__(self, size, coordinates):
        self.size = size
        self.coordinates = coordinates
        self.hits = 0

class Board:
    def __init__(self):
        self.ships = []
        self.board = [['О' for _ in range(6)] for _ in range(6)]

    def place_ship(self, ship):
        for x, y in ship.coordinates:
            self.board[x][y] = '■'
        self.ships.append(ship)

    def is_valid_move(self, x, y):
        return 0 <= x < 6 and 0 <= y < 6 and self.board[x][y] == 'О'

    def make_move(self, x, y):
        if not self.is_valid_move(x, y):
            raise ValueError("Invalid move!")

        for ship in self.ships:
            if (x, y) in ship.coordinates:
                ship.hits += 1
                self.board[x][y] = 'X'
                if ship.hits == ship.size:
                    print("Потоплен корабль размером", ship.size)
                return True

        self.board[x][y] = 'T'
        print("Промах!")
        return False

    def display_board(self):
        print("   | 1 | 2 | 3 | 4 | 5 | 6|")
        for i in range(6):
            print(f"{i + 1} | {' | '.join(self.board[i])} |")

def main():
    player_board = Board()
    computer_board = Board()

    player_ships = [Ship(3, [(1, 1), (1, 2), (1, 3)]),
                    Ship(2, [(4, 0), (4, 2)]),
                    Ship(1, [(0, 3)]),
                    Ship(2, [(4, 4), (5, 4)]),
                    Ship(1, [(2, 1)])]

    computer_ships = [Ship(3, [(0, 0), (0, 1), (0, 2)]),
                      Ship(2, [(1, 4), (1, 5)]),
                      Ship(1, [(3, 0)]),
                      Ship(2, [(3, 2), (3, 4)]),
                      Ship(1, [(5, 1)])]

    for ship in player_ships:
        player_board.place_ship(ship)

    for ship in computer_ships:
        computer_board.place_ship(ship)

    player_moves = set()

    while True:
        print("Ваша доска:")
        player_board.display_board()
        print("\nДоска противника:")
        computer_board.display_board()

        try:
            x = int(input("Введите номер строки (1-6): ")) - 1
            y = int(input("Введите номер столбца (1-6): ")) - 1
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")
            continue

        if (x, y) in player_moves:
            print("Вы уже стреляли в эту клетку. Попробуйте снова.")
            continue

        player_moves.add((x, y))
        player_hit = computer_board.make_move(x, y)

        if all(ship.hits == ship.size for ship in computer_ships):
            print("Поздравляем! Вы победили!")
            break

        if player_hit:
            continue

        computer_x, computer_y = random.randint(0, 5), random.randint(0, 5)
        while (computer_x, computer_y) in player_moves:
            computer_x, computer_y = random.randint(0, 5), random.randint(0, 5)

        player_hit = player_board.make_move(computer_x, computer_y)

        if all(ship.hits == ship.size for ship in player_ships):
            print("Компьютер победил! Попробуйте еще раз.")
            break

if __name__ == "__main__":
    main()
