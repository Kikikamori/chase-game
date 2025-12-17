"""
chase_terminal.py - Консольный интерфейс для игры Chase
Обеспечивает взаимодействие с пользователем через терминал
"""

import sys
import os
from typing import Optional, List
from chase_core import ChaseGame, PLAYER, INTERCEPTOR, WALL, EMPTY

class ChaseTerminal:
    """Класс для управления терминальным интерфейсом игры"""
    
    def __init__(self, seed: Optional[int] = None, log_output: bool = False):
        """
        Инициализация терминального интерфейса
        
        Args:
            seed: Seed для генератора случайных чисел (для воспроизводимости)
            log_output: Если True, вывод будет записываться в лог
        """
        self.game = ChaseGame(seed)
        self.log_output = log_output
        self.log_lines: List[str] = []
        self.input_history: List[str] = []
        
    def clear_screen(self):
        """Очистка экрана (кроссплатформенная)"""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')
    
    def print_with_log(self, text: str):
        """Вывод текста с возможностью логирования"""
        print(text)
        if self.log_output:
            self.log_lines.append(text)
    
    def show_header(self):
        """Отображение заголовка игры"""
        self.print_with_log(" " * 26 + "CHASE")
        self.print_with_log(" " * 20 + "CREATIVE COMPUTING")
        self.print_with_log(" " * 18 + "MORRISTOWN, NEW JERSEY")
        self.print_with_log("\n" * 3)
    
    def show_instructions(self):
        """Отображение инструкций игры"""
        instructions = self.game.get_instructions()
        self.print_with_log(instructions)
    
    def show_board(self):
        """Отображение игрового поля"""
        board_str = self.game.get_board_string()
        self.print_with_log(board_str)
    
    def get_player_move(self) -> Optional[int]:
        """
        Получение хода от игрока
        
        Returns:
            Код хода или None если ввод некорректен
        """
        while True:
            try:
                if self.log_output:
                    # Для тестов используем предопределенный ввод
                    if self.input_history:
                        move_input = self.input_history.pop(0)
                        self.print_with_log(f"Input (from history): {move_input}")
                    else:
                        move_input = input().strip()
                else:
                    move_input = input("YOUR MOVE? ").strip()
                
                # Логируем ввод
                if self.log_output and move_input not in self.input_history:
                    self.log_lines.append(f"Input: {move_input}")
                
                # Парсим ввод
                if not move_input:
                    continue
                    
                move = int(move_input)
                
                # Проверка допустимых значений
                valid_moves = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                if move in valid_moves:
                    return move
                else:
                    self.print_with_log(f"Invalid move: {move}. Valid moves are: {valid_moves}")
                    
            except ValueError:
                self.print_with_log("Please enter a number")
            except EOFError:
                self.print_with_log("\nGame interrupted")
                return None
            except KeyboardInterrupt:
                self.print_with_log("\nGame interrupted")
                return None
    
    def process_game_result(self, result: dict) -> bool:
        """
        Обработка результата хода
        
        Args:
            result: Результат из game.process_move()
            
        Returns:
            True если игра продолжается, False если игра закончена
        """
        if result['message']:
            self.print_with_log(result['message'])
            self.print_with_log("")  # Пустая строка для разделения
        
        if result['game_over']:
            return False
            
        return True
    
    def ask_play_again(self) -> bool:
        """Спрашивает, хочет ли игрок сыграть еще раз"""
        while True:
            try:
                if self.log_output and self.input_history:
                    response = self.input_history.pop(0).strip().upper()
                    self.print_with_log(f"ANOTHER GAME (Y/N)? {response}")
                else:
                    response = input("ANOTHER GAME (Y/N)? ").strip().upper()
                
                if response in ['Y', 'N']:
                    return response == 'Y'
                else:
                    self.print_with_log("Please enter Y or N")
                    
            except EOFError:
                return False
            except KeyboardInterrupt:
                return False
    
    def ask_same_setup(self) -> bool:
        """Спрашивает, использовать ли ту же начальную расстановку"""
        while True:
            try:
                if self.log_output and self.input_history:
                    response = self.input_history.pop(0).strip().upper()
                    self.print_with_log(f"SAME SETUP (Y/N)? {response}")
                else:
                    response = input("SAME SETUP (Y/N)? ").strip().upper()
                
                if response in ['Y', 'N']:
                    return response == 'Y'
                else:
                    self.print_with_log("Please enter Y or N")
                    
            except EOFError:
                return False
            except KeyboardInterrupt:
                return False
    
    def run_game_loop(self):
        """Основной игровой цикл"""
        game_active = True
        
        while game_active:
            # Показываем заголовок и инструкции только в начале
            self.show_header()
            self.show_instructions()
            
            # Основной цикл одной игры
            while not self.game.game_over:
                self.show_board()
                
                # Проверка условия 10 ходов без вывода (строка 610)
                # В оригинале: IF Y9 <> 10 THEN 640
                # Мы обрабатываем это в process_move
                
                move = self.get_player_move()
                if move is None:
                    self.game.game_over = True
                    break
                
                result = self.game.process_move(move)
                game_continues = self.process_game_result(result)
                
                if not game_continues:
                    break
            
            # Игра закончена, спрашиваем о повторной игре
            if not self.log_output:
                play_again = self.ask_play_again()
            else:
                # В тестовом режиме используем предопределенные ответы
                if self.input_history:
                    response = self.input_history.pop(0).strip().upper() if self.input_history else 'N'
                    play_again = response == 'Y'
                    self.print_with_log(f"ANOTHER GAME (Y/N)? {response}")
                else:
                    play_again = False
            if play_again:
                same_setup = self.ask_same_setup()
                if same_setup:
                    self.game.reset_to_original()
                else:
                    # Создаем новую игру с тем же seed если был указан
                    seed = self.game.game.seed if hasattr(self.game, 'seed') else None
                    self.game = ChaseGame(seed)
            else:
                game_active = False
    
    def run_with_inputs(self, inputs: List[str]) -> List[str]:
        """
        Запуск игры с предопределенными вводами (для тестирования)
        
        Args:
            inputs: Список строк ввода
            
        Returns:
            Список строк вывода (лог игры)
        """
        self.log_output = True
        self.input_history = inputs.copy()
        
        # Запускаем игру
        try:
            self.run_game_loop()
        except Exception as e:
            self.print_with_log(f"Error during game execution: {e}")
        
        return self.log_lines.copy()


def print_help():
    """Вывод справки по использованию"""
    help_text = """
Chase Game - Terminal Version

Usage:
    python chase_terminal.py [options]

Options:
    --seed=NUMBER      Set random seed for reproducible games
    --test             Run in test mode (no interactive input)
    --help, -h         Show this help message
    --version          Show version information

Game Controls:
    7 8 9      Up-Left, Up, Up-Right
    4   6      Left, Right
    1 2 3      Down-Left, Down, Down-Right
    
    0         Random jump
    10        No move for rest of game
    -1        Give up

Examples:
    python chase_terminal.py
    python chase_terminal.py --seed=42
    """
    print(help_text)


def main():
    """Основная функция запуска"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Chase Game - Terminal Version',
        add_help=False
    )
    
    parser.add_argument('--seed', type=int, help='Random seed for reproducible games')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--help', '-h', action='store_true', help='Show help message')
    parser.add_argument('--version', action='store_true', help='Show version information')
    
    args = parser.parse_args()
    
    if args.help:
        print_help()
        return
    
    if args.version:
        print("Chase Game v1.0 - Python Port")
        print("Based on original BASIC version from Creative Computing")
        return
    
    if args.test:
        # Режим тестирования - запускаем с предопределенными вводами
        print("Running in test mode...")
        test_inputs = ["8", "6", "-1", "N"]  # Пример тестового ввода
        terminal = ChaseTerminal(seed=args.seed, log_output=True)
        log = terminal.run_with_inputs(test_inputs)
        
        print("\n" + "="*50)
        print("Game Log:")
        print("="*50)
        for line in log:
            print(line)
        return
    
    # Интерактивный режим
    try:
        terminal = ChaseTerminal(seed=args.seed, log_output=False)
        terminal.run_game_loop()
        
        print("\nThanks for playing Chase!")
        print("Based on original BASIC version from Creative Computing")
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()