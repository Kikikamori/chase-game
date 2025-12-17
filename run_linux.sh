#!/bin/bash

echo "Запуск Chase Game для Linux..."
echo

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не найден!"
    echo "Установите Python3: sudo apt install python3 python3-pip"
    exit 1
fi

# Создание виртуального окружения если нужно
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
echo "Установка зависимостей..."
pip install -r requirements.txt > /dev/null 2>&1

# Запуск игры
echo
echo "==============================="
echo "CHASE GAME - LINUX VERSION"
echo "==============================="
echo
python3 chase_terminal.py