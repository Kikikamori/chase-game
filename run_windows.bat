@echo off
chcp 65001 > nul
echo Запуск Chase Game для Windows...
echo.

REM Проверка Python
python --version > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не найден!
    echo Установите Python 3.8+ с python.org
    pause
    exit /b 1
)

REM Создание виртуального окружения если нужно
if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
)

REM Активация виртуального окружения
call venv\Scripts\activate.bat

REM Установка зависимостей
echo Установка зависимостей...
pip install -r requirements.txt > nul 2>&1
if errorlevel 1 (
    echo Ошибка установки зависимостей
    pause
    exit /b 1
)

REM Запуск игры
echo.
echo ===============================
echo CHASE GAME - WINDOWS VERSION
echo ===============================
echo.
python chase_terminal.py

pause