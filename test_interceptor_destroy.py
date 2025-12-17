import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chase_core import ChaseGame, WALL, INTERCEPTOR, EMPTY

def test_interceptor_on_wall():
    """Тест, что перехватчик уничтожается при попадании на стену"""
    print("Тестирование уничтожения перехватчика на стене...")
    
    # Создаем простую тестовую конфигурацию
    game = ChaseGame(seed=999)
    
    # Упростим поле для теста
    for row in range(game.rows):
        for col in range(game.cols):
            if row == 0 or row == game.rows-1 or col == 0 or col == game.cols-1:
                game.board[row][col] = WALL
            else:
                game.board[row][col] = EMPTY
    
    # Размещаем игрока
    game.board[5][5] = '*'
    game.player_pos = (5, 5)
    
    # Размещаем перехватчика рядом со стеной
    game.board[1][1] = '+'
    game.interceptors = [(1, 1)]
    
    print("Начальное состояние:")
    print(game.get_board_string())
    
    # Заставляем перехватчика двигаться к игроку через стену
    # Игрок в (5,5), перехватчик в (1,1)
    # Перехватчик будет пытаться идти вправо-вниз
    
    # Делаем ход, чтобы перехватчик двинулся
    print("\nДелаем ход игрока (стоять на месте)...")
    result = game.process_move(5)  # Ход на месте
    
    print("Состояние после хода:")
    print(game.get_board_string())
    
    # Проверяем, что перехватчик либо на стене, либо исчез
    interceptor_row, interceptor_col = game.interceptors[0]
    cell_content = game.board[interceptor_row][interceptor_col]
    
    print(f"\nПозиция перехватчика: ({interceptor_row}, {interceptor_col})")
    print(f"Содержимое клетки: '{cell_content}'")
    
    if cell_content == WALL:
        print("✓ Перехватчик успешно уничтожен на стене!")
        return True
    elif cell_content == INTERCEPTOR:
        print("✗ Перехватчик все еще жив")
        # Проверяем, может он уже на стене?
        # Если координаты (1,1) - это граница поля? (столбец 1 это второй столбец, не граница)
        return False
    else:
        print("✗ Перехватчик исчез с поля (может быть правильно?)")
        return False

if __name__ == "__main__":
    test_interceptor_on_wall()