import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chase_core import ChaseGame

print("Тестирование прыжка для seed=42")
print("=" * 60)

game = ChaseGame(seed=42)

print(f"Позиция игрока: {game.player_pos}")
print(f"Позиции перехватчиков: {game.interceptors}")

# Выведем поле
print("\nИгровое поле:")
for i, row in enumerate(game.board):
    print(f"{i:2}: {''.join(row)}")

# Проанализируем возможные позиции прыжка
import random
random.seed(42)

# Пропускаем уже использованные random числа
# (игра уже использовала random для генерации поля)
for _ in range(100):
    random.random()

# Просчитаем, куда прыгнет игрок
jump_row = random.randint(1, 8)
jump_col = random.randint(1, 18)

print(f"\nПредсказанная позиция прыжка: ({jump_row}, {jump_col})")
print(f"Содержимое клетки: '{game.board[jump_row][jump_col]}'")

# Выполним прыжок
print("\nВыполняем прыжок...")
result = game.process_move(0)

print(f"\nРезультат:")
print(f"Сообщение: {result['message']}")
print(f"Тип сообщения: {'JUMP' if 'JUMP' in result['message'] else 'DEATH'}")
print(f"Уничтожен: {result['player_destroyed']}")

# Проверим позицию после прыжка
if not result['player_destroyed']:
    print(f"Новая позиция игрока: {game.player_pos}")
    
    # Проверим движение перехватчиков
    print("\nПозиции перехватчиков после прыжка:")
    for i, pos in enumerate(game.interceptors):
        print(f"  Перехватчик {i+1}: {pos}")