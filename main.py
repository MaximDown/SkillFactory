# Вывод игрового поля
def print_board(board):
    print(f"""
  0   1   2
0 {board[0]} | {board[1]} | {board[2]}
  -- -- ---
1 {board[3]} | {board[4]} | {board[5]}
  -- -- ---
2 {board[6]} | {board[7]} | {board[8]}
""")


# Поиск победителя
def check_winner(board, player):
    # Проверка строк
    for i in range(0, 9, 3):
        if all(cell == player for cell in board[i:i + 3]):
            return True

    # Проверка столбцов
    for i in range(3):
        if all(board[i] == player for i in range(i, 9, 3)):
            return True

    # Проверка диагоналей
    if all(board[i] == player for i in range(0, 9, 4)) or all(board[i] == player for i in range(2, 7, 2)):
        return True

    # Иначе игра не окончена
    return False


# Игра
def x_and_o():
    # Создание списка с определенной длиной
    board = [" " for _ in range(9)]
    player = "X"

    while True:
        # Вывод игрового поля
        print_board(board)
        try:
            # Выбор места метки
            position = int(input(f"Игрок {player}, выберите ячейку (1-9): ")) - 1

            # Если введенное значение is Цифра и на ёё позиции пусто
            if 0 <= position < 9 and board[position] == " ":
                # Ставим значок игрока
                board[position] = player
                # Поиск победителя
                if check_winner(board, player):
                    print_board(board)
                    print(f"Игрок {player} победил!")
                    break
                elif all(cell != " " for cell in board):
                    print_board(board)
                    print("Ничья!")
                    break
                # Иначе продолжаем
                else:
                    player = "O" if player == "X" else "X"
            else:
                print("Некорректный выбор ячейки, пожалуйста, выберите другую.")
        except:
            print("Некорректный выбор ячейки, пожалуйста, выберите другую.")


if __name__ == "__main__":
    x_and_o()
