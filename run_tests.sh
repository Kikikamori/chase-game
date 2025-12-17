#!/bin/bash
# Скрипт для запуска всех тестов

echo "Running Chase Game tests..."
echo "============================"

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
echo "Installing dependencies..."
pip install -r test_requirements.txt > /dev/null 2>&1

# Запускаем тесты
echo ""
echo "Running unit tests..."
python -m pytest test_chase.py -v --cov=chase_core --cov=chase_terminal --cov-report=term-missing

echo ""
echo "Running coverage report..."
python -m coverage html
echo "Coverage report generated in htmlcov/"

# Деактивируем виртуальное окружение
deactivate

echo ""
echo "Tests completed!"