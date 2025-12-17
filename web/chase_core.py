"""
chase_core.py - Ядро игры Chase, портированное с BASIC
Сохранена оригинальная логика игры для обеспечения корректного тестирования.
"""

import random
from typing import List, Tuple, Optional, Dict, Any

# Константы для представления клеток
EMPTY = ' '
WALL = 'X'
PLAYER = '*'
INTERCEPTOR = '+'

class ChaseGame:
    """Основной класс игры, инкапсулирующий всю логику"""
    
    def __init__(self, seed: Optional[int] = None):
        """Инициализация игры с опциональным сидом для воспроизводимости"""
        if seed is not None:
            random.seed(seed)
        
        # Инициализация игрового поля (10x20)
        self.rows = 10
        self.cols = 20
        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.original_board = None  # Для сохранения начальной конфигурации
        
        # Позиции игрока и перехватчиков
        self.player_pos = (0, 0)
        self.interceptors = []  # Список позиций перехватчиков [(row, col), ...]
        self.original_interceptors = []
        self.original_player_pos = (0, 0)
        
        # Состояние игры
        self.game_over = False
        self.game_won = False
        self.game_lost = False
        self.give_up = False
        self.jump_used = False
        
        # Счетчики
        self.move_count = 0
        self.interceptors_destroyed = 0
        
        # Инициализация игры
        self._initialize_game()
    
    def _initialize_game(self):
        """Инициализация игрового поля (соответствует строкам 190-480 BASIC)"""
        # Сначала заполняем поле случайными 'X' (строка 190-290)
        for row in range(self.rows):
            for col in range(self.cols):
                x = random.randint(0, 9)  # В BASIC: INT(10*RND(1))
                if x == 5:  # 10% вероятность стены
                    self.board[row][col] = WALL
                else:
                    self.board[row][col] = EMPTY
        
        # Края поля - всегда стены (строки 300-350)
        for row in range(self.rows):
            self.board[row][0] = WALL
            self.board[row][self.cols-1] = WALL
        
        for col in range(self.cols):
            self.board[0][col] = WALL
            self.board[self.rows-1][col] = WALL
        
        # Размещаем игрока (строки 410-420)
        while True:
            row = random.randint(1, self.rows-2)  # 2+8*RND(1) в BASIC
            col = random.randint(1, self.cols-2)  # 2+18*RND(1) в BASIC
            if self.board[row][col] == EMPTY:
                self.board[row][col] = PLAYER
                self.player_pos = (row, col)
                self.original_player_pos = (row, col)
                break
        
        # Размещаем 5 перехватчиков (строки 440-480)
        self.interceptors = []
        for _ in range(5):
            while True:
                row = random.randint(1, self.rows-2)
                col = random.randint(1, self.cols-2)
                if self.board[row][col] == EMPTY:
                    self.board[row][col] = INTERCEPTOR
                    self.interceptors.append((row, col))
                    break
        
        self.original_interceptors = self.interceptors.copy()
        
        # Сохраняем копию доски для функции "SAME SETUP"
        self.original_board = [row.copy() for row in self.board]
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Проверка, находится ли позиция в пределах поля"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def _move_interceptor(self, interceptor_idx: int, player_row: int, player_col: int) -> bool:
        """
        Движение перехватчика (соответствует подпрограмме 940-1060 BASIC)
        Возвращает True, если перехватчик уничтожил игрока
        """
        interceptor_row, interceptor_col = self.interceptors[interceptor_idx]
        
        # Проверка, не стоит ли перехватчик уже на 'X' (строка 940)
        if self.board[interceptor_row][interceptor_col] == WALL:
            return False
        
        # Сохраняем старую позицию
        old_row, old_col = interceptor_row, interceptor_col
        
        # Вычисляем движение к игроку (строки 960-970)
        # SGN(J-X) в BASIC возвращает -1, 0, 1
        delta_row = 0
        if player_row > interceptor_row:
            delta_row = 1
        elif player_row < interceptor_row:
            delta_row = -1
        
        delta_col = 0
        if player_col > interceptor_col:
            delta_col = 1
        elif player_col < interceptor_col:
            delta_col = -1
        
        new_row = interceptor_row + delta_row
        new_col = interceptor_col + delta_col
        
        # Проверка новой позиции
        if not self._is_valid_position(new_row, new_col):
            return False
        
        # Проверка, не столкнулся ли с игроком (строка 980)
        if self.board[new_row][new_col] == PLAYER:
            return True  # Игрок уничтожен
        
        # Если клетка пуста - перемещаемся (строки 990-1030)
        if self.board[new_row][new_col] == EMPTY:
            self.board[old_row][old_col] = EMPTY
            self.board[new_row][new_col] = INTERCEPTOR
            self.interceptors[interceptor_idx] = (new_row, new_col)
        # Если клетка занята стенкой - остаемся на месте (строка 1000)
        elif self.board[new_row][new_col] == WALL:
            self.board[old_row][old_col] = EMPTY
        
        return False
    
    def process_move(self, move: int) -> Dict[str, Any]:
        """
        Обработка хода игрока
        Возвращает словарь с результатом хода
        """
        result = {
            'valid_move': True,
            'message': '',
            'player_destroyed': False,
            'game_over': False,
            'game_won': False
        }
        
        # Если игра уже закончена
        if self.game_over:
            result['valid_move'] = False
            result['message'] = 'Game is already over'
            return result
        
        self.move_count += 1
        
        # Сохраняем старую позицию игрока
        old_row, old_col = self.player_pos
        
        # Обработка специальных ходов
        if move == 0:  # Случайный прыжок (строки 860-880)
            result['message'] = "$6,000,000 JUMP!!!"
            self.jump_used = True
    
            # Сохраняем позицию до прыжка
            old_row, old_col = self.player_pos
    
            # Ищем свободную клетку для прыжка
            attempts = 0
            new_pos = None
            
            while attempts < 100:
                new_row = random.randint(1, self.rows-2)
                new_col = random.randint(1, self.cols-2)
                
                if self.board[new_row][new_col] == EMPTY:
                    new_pos = (new_row, new_col)
                    break
                attempts += 1
            
            if new_pos:
                # Очищаем старую позицию
                self.board[old_row][old_col] = EMPTY
                # Перемещаем игрока
                self.board[new_pos[0]][new_pos[1]] = PLAYER
                self.player_pos = new_pos
                return result
            else:
                # Не нашли свободную клетку - остаемся на месте
                result['message'] += " (no empty space found)"
            #result['message'] = "$6,000,000 JUMP!!!"
            #self.jump_used = True
            
            # Ищем свободную клетку для прыжка
            #attempts = 0
            #while attempts < 100:  # Защита от бесконечного цикла
                #new_row = random.randint(1, self.rows-2)
                #new_col = random.randint(1, self.cols-2)
                
                #if self.board[new_row][new_col] == EMPTY:
                    # Очищаем старую позицию
                    #self.board[old_row][old_col] = EMPTY
                    # Перемещаем игрока
                    #self.board[new_row][new_col] = PLAYER
                    #self.player_pos = (new_row, new_col)
                    #break
                #attempts += 1
            
            #if attempts >= 100:
                # Не нашли свободную клетку - остаемся на месте
                #result['message'] += " (no empty space found)"
        
        elif move == -1:  # Сдаться (строка 1230)
            result['message'] = "GIVE UP, EH."
            self.give_up = True
            self.game_over = True
            result['game_over'] = True
            return result
        
        elif move == 10:  # Пропуск хода до конца игры
            result['message'] = "No move for the rest of the game"
            # Игрок остается на месте
            pass
        
        elif 1 <= move <= 9:  # Обычный ход (строки 690-890)
            # Преобразуем цифровую клавишу в смещение
            # BASIC использует ON Y9 GOTO для диспетчеризации
            move_map = {
                1: (1, -1),  7: (-1, -1),
                2: (1, 0),   8: (-1, 0),
                3: (1, 1),   9: (-1, 1),
                4: (0, -1),  6: (0, 1)
            }
            
            if move == 5:  # Нет движения (игрок остается на месте)
                delta_row, delta_col = (0, 0)
            else:
                delta_row, delta_col = move_map[move]
            
            new_row = old_row + delta_row
            new_col = old_col + delta_col
            
            # Проверка новой позиции
            if not self._is_valid_position(new_row, new_col):
                result['valid_move'] = False
                result['message'] = "Invalid move - out of bounds"
                return result
            
            # Проверка, не стена ли (строка 890)
            if self.board[new_row][new_col] == WALL:
                result['message'] = "HIGH VOLTAGE!!!!!!!!!!\n***** ZAP *****  YOU'RE DEAD!!!"
                result['player_destroyed'] = True
                self.game_over = True
                self.game_lost = True
                result['game_over'] = True
                return result
            
            # Перемещаем игрока (строки 900-910)
            self.board[old_row][old_col] = EMPTY
            self.board[new_row][new_col] = PLAYER
            self.player_pos = (new_row, new_col)
        
        else:
            result['valid_move'] = False
            result['message'] = f"Invalid move code: {move}"
            return result
        
        # Движение перехватчиков (строки 1070-1130)
        player_destroyed = False
        for i in range(len(self.interceptors)):
            if self._move_interceptor(i, self.player_pos[0], self.player_pos[1]):
                player_destroyed = True
                break
        
        # Восстанавливаем символы перехватчиков (строки 1140-1170)
        for row, col in self.interceptors:
            if self.board[row][col] == EMPTY:
                self.board[row][col] = INTERCEPTOR
        
        # Проверка, уничтожен ли игрок (строки 1240-1250)
        if player_destroyed:
            result['message'] = "*** YOU HAVE BEEN DESTROYED BY A LUCKY COMPUTER ***"
            result['player_destroyed'] = True
            self.game_over = True
            self.game_lost = True
            result['game_over'] = True
            return result
        
        # Проверка победы (все перехватчики на стенах) (строки 1180-1220)
        all_on_walls = True
        for row, col in self.interceptors:
            if self.board[row][col] != WALL:
                all_on_walls = False
                break
        
        if all_on_walls:
            result['message'] = "YOU HAVE DESTROYED ALL YOUR OPPONENTS - THE GAME IS YOURS"
            self.game_over = True
            self.game_won = True
            result['game_won'] = True
            result['game_over'] = True
        
        return result
    
    def get_board_string(self) -> str:
        """Возвращает текстовое представление игрового поля"""
        lines = []
        for row in range(self.rows):
            line = ''.join(self.board[row])
            lines.append(line)
        return '\n'.join(lines)
    
    def get_game_state(self) -> Dict[str, Any]:
        """Возвращает текущее состояние игры"""
        return {
            'board': [row.copy() for row in self.board],
            'player_pos': self.player_pos,
            'interceptors': self.interceptors.copy(),
            'game_over': self.game_over,
            'game_won': self.game_won,
            'game_lost': self.game_lost,
            'give_up': self.give_up,
            'move_count': self.move_count,
            'interceptors_destroyed': self.interceptors_destroyed
        }
    
    def reset_to_original(self):
        """Сброс игры к начальной конфигурации (для 'SAME SETUP')"""
        if self.original_board is not None:
            self.board = [row.copy() for row in self.original_board]
            self.interceptors = self.original_interceptors.copy()
            self.player_pos = self.original_player_pos
            self.game_over = False
            self.game_won = False
            self.game_lost = False
            self.give_up = False
            self.move_count = 0
            self.interceptors_destroyed = 0
    
    def get_instructions(self) -> str:
        """Возвращает инструкции игры"""
        instructions = [
            "YOU ARE WITHIN THE WALLS OF A HIGH VOLTAGE MAZE",
            "THERE ARE FIVE SECURITY MACHINES TRYING TO DESTROY YOU",
            "YOU ARE THE '*'  THE INTERCEPTORS ARE THE '+'",
            "THE AREAS MARKED 'X' ARE HIGH VOLTAGE",
            "YOUR ONLY CHANCE FOR SURVIVAL IS TO MANEUVER EACH",
            "INTERCEPTOR INTO AN 'X'.-----GOOD LUCK-----",
            "MOVES ARE   7.8.9",
            "            4.*.6",
            "            1.2.3",
            "",
            "10 = NO MOVE FOR THE REST OF THE GAME",
            "-1 = GAVE UP, SITUATION HOPELESS.",
            " 0 = A TREMENDOUS (BUT UNFORTUNATELY RANDOM) LEAP",
            ""
        ]
        return '\n'.join(instructions)


def create_game_from_log(log_data: List[str]) -> ChaseGame:
    """
    Создает игру из лога для тестирования.
    Это полезно для воспроизведения конкретных игровых ситуаций.
    """
    # Парсим начальную конфигурацию из лога
    # (Упрощенная версия - в реальности нужно парсить больше данных)
    game = ChaseGame(seed=42)  # Фиксированный seed для воспроизводимости
    return game


if __name__ == "__main__":
    # Простой тест ядра
    game = ChaseGame(seed=42)
    print("Initial board:")
    print(game.get_board_string())
    print("\nInstructions:")
    print(game.get_instructions())
    
    # Тестируем несколько ходов
    moves = [8, 6, -1]  # Вверх, вправо, сдаться
    for move in moves:
        print(f"\nMove: {move}")
        result = game.process_move(move)
        print(f"Result: {result['message']}")
        if result['game_over']:
            break