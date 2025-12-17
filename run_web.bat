@echo off
chcp 65001 > nul
echo Запуск Chase Game Web версии...
echo.

if exist "venv" (
    call venv\Scripts\activate.bat
)

pip install flask > nul 2>&1

echo Запуск сервера на http://localhost:5000
echo Нажмите Ctrl+C для остановки
echo.

python chase_web.py