import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chase_core import ChaseGame

# Тест прыжка
print("Тестирование прыжка (ход 0)...")
game = ChaseGame(seed=42)

print(f"Начальная позиция игрока: {game.player_pos}")
print(f"Позиции перехватчиков: {game.interceptors}")

# Показываем поле до прыжка
print("\nДо прыжка:")
print(game.get_board_string())

# Выполняем прыжок
result = game.process_move(0)
print(f"\nРезультат прыжка:")
print(f"  Сообщение: {result['message']}")
print(f"  Уничтожен: {result.get('player_destroyed', False)}")
print(f"  Игра окончена: {result.get('game_over', False)}")

print(f"\nПозиция игрока после прыжка: {game.player_pos}")

# Показываем поле после прыжка
print("\nПосле прыжка:")
print(game.get_board_string())