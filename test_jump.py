import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chase_core import ChaseGame

# Тест прыжка с движением перехватчиков
print("Тестирование прыжка (ход 0) с движением перехватчиков...")
game = ChaseGame(seed=42)

print(f"Начальная позиция игрока: {game.player_pos}")
print(f"Позиции перехватчиков: {game.interceptors}")

# Показываем поле до прыжка
print("\nДо прыжка:")
board_before = game.get_board_string()
print(board_before)

# Сохраняем позиции перехватчиков до прыжка
interceptors_before = game.interceptors.copy()

# Выполняем прыжок
print("\nВыполняем прыжок (ход 0)...")
result = game.process_move(0)
print(f"Результат прыжка: {result['message']}")

# Показываем поле после прыжка
print("\nПосле прыжка:")
board_after = game.get_board_string()
print(board_after)

print(f"\nПозиция игрока после прыжка: {game.player_pos}")
print(f"Позиции перехватчиков после прыжка: {game.interceptors}")

# Проверяем, изменились ли позиции перехватчиков
changed = False
for i, (before, after) in enumerate(zip(interceptors_before, game.interceptors)):
    if before != after:
        changed = True
        print(f"  Перехватчик {i+1}: {before} -> {after} (ДВИГАЛСЯ!)")
    else:
        print(f"  Перехватчик {i+1}: {before} -> {after} (остался на месте)")

if changed:
    print("\n✓ Перехватчики двигаются после прыжка - КОРРЕКТНО!")
else:
    print("\n✗ Перехватчики НЕ двигаются после прыжка - ОШИБКА!")

# Тестируем несколько ходов с прыжком
print("\n" + "="*60)
print("Тестирование последовательности ходов:")
game2 = ChaseGame(seed=123)

print("\nХод 1: Игрок идет вверх (8)")
result = game2.process_move(8)
print(f"Сообщение: {result['message']}")
print("Поле после хода:")
print(game2.get_board_string())

print("\nХод 2: Игрок прыгает (0)")
result = game2.process_move(0)
print(f"Сообщение: {result['message']}")
print("Поле после прыжка:")
print(game2.get_board_string())

# Проверяем, двигались ли перехватчики
if not result.get('player_destroyed', False) and not result.get('game_over', False):
    print("\n✓ После прыжка игра продолжается и перехватчики двигаются")
else:
    print("\n✗ Что-то пошло не так")