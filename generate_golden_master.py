#!/usr/bin/env python3
"""
Генератор эталонных логов для игры Chase
Генерирует логи, соответствующие оригинальной BASIC версии
"""

import os
import sys
import random
from pathlib import Path
from typing import List, Dict, Any

# Добавляем путь к модулям игры
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chase_core import ChaseGame
from chase_terminal import ChaseTerminal


class GoldenMasterGenerator:
    """Генератор эталонных логов"""
    
    def __init__(self, output_dir: str = "test_data/golden_master"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Тестовые сценарии
        self.scenarios = [
            {
                "name": "immediate_surrender",
                "description": "Игрок сдается на первом ходу",
                "inputs": ["-1", "N"],
                "seed": 42,
                "expected_lines": ["GIVE UP, EH."]
            },
            {
                "name": "random_jump_surrender",
                "description": "Случайный прыжок и сдача",
                "inputs": ["0", "-1", "N"],
                "seed": 42,
                "expected_lines": ["$6,000,000 JUMP!!!", "GIVE UP, EH."]
            },
            {
                "name": "no_move_surrender",
                "description": "Пропуск ходов и сдача",
                "inputs": ["10", "-1", "N"],
                "seed": 42,
                "expected_lines": ["GIVE UP, EH."]
            },
            {
                "name": "wall_collision",
                "description": "Столкновение со стеной",
                "inputs": ["8", "8", "8", "8", "N"],
                "seed": 123,
                "expected_lines": ["HIGH VOLTAGE", "ZAP", "YOU'RE DEAD"]
            },
            {
                "name": "interceptor_capture",
                "description": "Захват перехватчиком",
                "inputs": ["5", "5", "5", "5", "5", "5", "N"],
                "seed": 456,
                "expected_lines": ["DESTROYED BY A LUCKY COMPUTER"]
            },
            {
                "name": "multiple_moves",
                "description": "Несколько ходов в разных направлениях",
                "inputs": ["8", "6", "4", "2", "7", "9", "1", "3", "-1", "N"],
                "seed": 789,
                "expected_lines": ["GIVE UP, EH."]
            },
            {
                "name": "same_setup_restart",
                "description": "Перезапуск с той же расстановкой",
                "inputs": ["-1", "Y", "Y", "-1", "N"],
                "seed": 42,
                "expected_lines": ["GIVE UP, EH.", "SAME SETUP"]
            },
            {
                "name": "new_game_restart",
                "description": "Перезапуск с новой расстановкой",
                "inputs": ["-1", "Y", "N", "-1", "N"],
                "seed": 42,
                "expected_lines": ["GIVE UP, EH.", "ANOTHER GAME"]
            }
        ]
    
    def normalize_log(self, log_lines: List[str]) -> List[str]:
        """
        Нормализация лога для сравнения
        - Удаление лишних пробелов
        - Стандартизация переносов строк
        """
        normalized = []
        for line in log_lines:
            # Убираем пробелы в конце строки
            line = line.rstrip()
            # Заменяем множественные пробелы на один
            line = ' '.join(line.split())
            # Пропускаем полностью пустые строки (но сохраняем структуру)
            if line or len(normalized) == 0 or normalized[-1] != "":
                normalized.append(line)
        return normalized
    
    def generate_scenario(self, scenario: Dict[str, Any]) -> bool:
        """Генерация лога для одного сценария"""
        print(f"\nГенерация сценария: {scenario['name']}")
        print(f"Описание: {scenario['description']}")
        print(f"Входные данные: {scenario['inputs']}")
        
        try:
            # Создаем терминал с фиксированным seed
            terminal = ChaseTerminal(seed=scenario['seed'], log_output=True)
            
            # Запускаем игру с заданными вводами
            log_lines = terminal.run_with_inputs(scenario['inputs'])
            
            # Нормализуем лог
            normalized_log = self.normalize_log(log_lines)
            
            # Сохраняем лог
            output_file = self.output_dir / f"{scenario['name']}.log"
            with open(output_file, 'w', encoding='utf-8') as f:
                for line in normalized_log:
                    f.write(line + '\n')
            
            # Проверяем ожидаемые строки
            log_text = '\n'.join(normalized_log)
            all_found = True
            for expected in scenario['expected_lines']:
                if expected not in log_text:
                    print(f"  ВНИМАНИЕ: Ожидаемая строка не найдена: '{expected}'")
                    all_found = False
            
            print(f"  Успешно сохранен: {output_file}")
            print(f"  Количество строк: {len(normalized_log)}")
            
            return all_found
            
        except Exception as e:
            print(f"  ОШИБКА: {e}")
            return False
    
    def generate_all(self) -> Dict[str, bool]:
        """Генерация всех сценариев"""
        print("=" * 60)
        print("Генерация эталонных логов Golden Master")
        print("=" * 60)
        
        results = {}
        successful = 0
        
        for scenario in self.scenarios:
            success = self.generate_scenario(scenario)
            results[scenario['name']] = success
            if success:
                successful += 1
        
        # Сводка
        print("\n" + "=" * 60)
        print("Сводка генерации:")
        print("=" * 60)
        print(f"Всего сценариев: {len(self.scenarios)}")
        print(f"Успешно: {successful}")
        print(f"С ошибками: {len(self.scenarios) - successful}")
        
        for name, success in results.items():
            status = "✓ УСПЕХ" if success else "✗ ОШИБКА"
            print(f"  {name}: {status}")
        
        return results
    
    def create_verification_script(self):
        """Создание скрипта для верификации логов"""
        script_content = '''#!/usr/bin/env python3
"""
Скрипт верификации эталонных логов
Сравнивает сгенерированные логи с сохраненными эталонами
"""

import os
import sys
from pathlib import Path

def compare_logs(file1, file2, tolerance=0):
    """Сравнение двух логов с допустимой погрешностью"""
    with open(file1, 'r', encoding='utf-8') as f1:
        lines1 = [line.rstrip() for line in f1]
    
    with open(file2, 'r', encoding='utf-8') as f2:
        lines2 = [line.rstrip() for line in f2]
    
    # Проверяем длину
    if abs(len(lines1) - len(lines2)) > tolerance:
        return False, f"Разная длина: {len(lines1)} vs {len(lines2)}"
    
    # Сравниваем строки
    min_len = min(len(lines1), len(lines2))
    for i in range(min_len):
        if lines1[i] != lines2[i]:
            return False, f"Различие в строке {i+1}:\\n  Файл1: {lines1[i]}\\n  Файл2: {lines2[i]}"
    
    return True, "Логи идентичны"

def main():
    golden_dir = Path("test_data/golden_master")
    generated_dir = Path("test_data/generated")
    
    if not golden_dir.exists():
        print("Ошибка: Директория golden_master не найдена")
        return 1
    
    if not generated_dir.exists():
        print("Ошибка: Директория generated не найдена")
        return 1
    
    # Ищем все логи
    golden_files = list(golden_dir.glob("*.log"))
    generated_files = list(generated_dir.glob("*.log"))
    
    print("Верификация эталонных логов")
    print("=" * 60)
    
    all_passed = True
    
    for golden_file in golden_files:
        generated_file = generated_dir / golden_file.name
        
        if generated_file.exists():
            print(f"\\nПроверка: {golden_file.name}")
            passed, message = compare_logs(golden_file, generated_file, tolerance=5)
            
            if passed:
                print(f"  ✓ УСПЕХ: {message}")
            else:
                print(f"  ✗ ОШИБКА: {message}")
                all_passed = False
        else:
            print(f"  ✗ ОШИБКА: Соответствующий файл не найден: {generated_file.name}")
            all_passed = False
    
    print("\\n" + "=" * 60)
    if all_passed:
        print("Все тесты пройдены успешно!")
        return 0
    else:
        print("Обнаружены различия в логах")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
        
        script_file = self.output_dir.parent / "verify_logs.py"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Делаем скрипт исполняемым (Unix)
        if os.name != 'nt':
            os.chmod(script_file, 0o755)
        
        print(f"\nСкрипт верификации создан: {script_file}")
    
    def create_test_inputs(self):
        """Создание файлов с входными данными для тестов"""
        inputs_dir = self.output_dir.parent / "inputs"
        inputs_dir.mkdir(exist_ok=True)
        
        for scenario in self.scenarios:
            input_file = inputs_dir / f"{scenario['name']}.txt"
            with open(input_file, 'w', encoding='utf-8') as f:
                for inp in scenario['inputs']:
                    f.write(inp + '\n')
            
            print(f"Файл входных данных создан: {input_file}")


def main():
    """Основная функция"""
    generator = GoldenMasterGenerator()
    
    # Генерируем все логи
    results = generator.generate_all()
    
    # Создаем дополнительные файлы
    generator.create_verification_script()
    generator.create_test_inputs()
    
    # Создаем README для тестовых данных
    readme_content = """# Тестовые данные для игры Chase

## Структура каталогов

- `golden_master/` - Эталонные логи из оригинальной BASIC версии
- `generated/` - Логи, сгенерированные портированной версией
- `inputs/` - Входные данные для тестовых сценариев
- `comparison_results/` - Результаты сравнения логов

## Тестовые сценарии

1. **immediate_surrender** - Игрок сдается на первом ходу
2. **random_jump_surrender** - Случайный прыжок и сдача
3. **no_move_surrender** - Пропуск ходов и сдача
4. **wall_collision** - Столкновение со стеной
5. **interceptor_capture** - Захват перехватчиком
6. **multiple_moves** - Несколько ходов в разных направлениях
7. **same_setup_restart** - Перезапуск с той же расстановкой
8. **new_game_restart** - Перезапуск с новой расстановкой

## Использование

1. Генерация эталонных логов:
   ```bash
   python generate_golden_master.py