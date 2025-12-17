import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chase_core import ChaseGame, WALL, INTERCEPTOR, PLAYER

print("Тестирование условия победы")
print("=" * 60)

# Создаем игровую ситуацию где все перехватчики на стенах
game = ChaseGame(seed=999)

# Упростим поле
for row in range(game.rows):
    for col in range(game.cols):
        game.board[row][col] = ' '

# Сделаем стены по краям
for row in range(game.rows):
    game.board[row][0] = WALL
    game.board[row][game.cols-1] = WALL
for col in range(game.cols):
    game.board[0][col] = WALL
    game.board[game.rows-1][col] = WALL

# Добавим несколько стен внутри
game.board[1][1] = WALL
game.board[1][2] = WALL
game.board[1][3] = WALL
game.board[1][4] = WALL
game.board[1][5] = WALL

# Разместим игрока
game.board[5][5] = PLAYER
game.player_pos = (5, 5)

# Разместим всех перехватчиков НА СТЕНАХ
game.interceptors = [
    (1, 1),  # На стене
    (1, 2),  # На стене
    (1, 3),  # На стене
    (1, 4),  # На стене
    (1, 5)   # На стене
]

# На поле перехватчики должны быть стенами (они уничтожены)
for row, col in game.interceptors:
    game.board[row][col] = WALL

print("Поле перед проверкой победы:")
print(game.get_board_string())
print(f"Перехватчики: {game.interceptors}")

# Делаем любой ход (например, стоять на месте)
print("\nДелаем ход игрока (5 - стоять на месте)...")
result = game.process_move(5)

print(f"Сообщение: {result['message']}")
print(f"Игра окончена: {result['game_over']}")
print(f"Игра выиграна: {result.get('game_won', False)}")

if result.get('game_won', False):
    print("✓ Условие победы работает!")
else:
    print("✗ Условие победы НЕ сработало!")
    print("Проверьте логику в process_move() после движения перехватчиков")