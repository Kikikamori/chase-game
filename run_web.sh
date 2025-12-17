#!/bin/bash

echo "Запуск Chase Game Web версии..."
echo

# Активация виртуального окружения
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Установка Flask если нужно
pip install flask gunicorn > /dev/null 2>&1

echo "Запуск сервера на http://localhost:5000"
echo "Нажмите Ctrl+C для остановки"
echo

python chase_web.py