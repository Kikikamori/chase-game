@echo off
REM Скрипт для запуска тестов на Windows

echo Running Chase Game tests...
echo ============================

REM Создаем виртуальное окружение если его нет
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Активируем виртуальное окружение
call venv\Scripts\activate.bat

REM Устанавливаем зависимости
echo Installing dependencies...
pip install -r test_requirements.txt > nul 2>&1

REM Запускаем тесты
echo.
echo Running unit tests...
python -m pytest test_chase.py -v --cov=chase_core --cov=chase_terminal --cov-report=term-missing

echo.
echo Running coverage report...
python -m coverage html
echo Coverage report generated in htmlcov\

REM Деактивируем виртуальное окружение
deactivate

echo.
echo Tests completed!
pause