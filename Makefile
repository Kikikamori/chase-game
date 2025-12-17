# ============================================================================
# УНИВЕРСАЛЬНЫЙ MAKEFILE для Chase Game (Python)
# ============================================================================

PROJECT_NAME = chase-game
VERSION = 1.0.0

# Определение операционной системы
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    PYTHON := python
    PIP := pip
    MKDIR := mkdir
    RMDIR := rmdir /S /Q
    RM := del /Q
    CP := copy
    ECHO := echo.
    PATH_SEP := \\
    MAKE := make
else
    DETECTED_OS := $(shell uname -s)
    ifeq ($(DETECTED_OS),Linux)
        DETECTED_OS := Linux
    endif
    ifeq ($(DETECTED_OS),Darwin)
        DETECTED_OS := macOS
    endif
    PYTHON := python3
    PIP := pip3
    MKDIR := mkdir -p
    RMDIR := rm -rf
    RM := rm -f
    CP := cp
    ECHO := echo
    PATH_SEP := /
    MAKE := make
endif

# Пути
SRC_DIR := .
BUILD_DIR := build
DIST_DIR := dist
WEB_DIR := web
TEMPLATES_DIR := templates
VENV_DIR := venv

# Флаги
PYTEST_FLAGS := -v

# ============================================================================
# ОСНОВНЫЕ ЦЕЛИ
# ============================================================================

.PHONY: all help

all: help

help:
	@$(ECHO) "Chase Game - универсальная система сборки"
	@$(ECHO) "Обнаружена ОС: $(DETECTED_OS)"
	@$(ECHO)
	@$(ECHO) "Основные цели:"
	@$(ECHO) "  make install     - Установить зависимости"
	@$(ECHO) "  make venv        - Создать виртуальное окружение"
	@$(ECHO) "  make test        - Запустить тесты"
	@$(ECHO) "  make run         - Запустить терминальную версию"
	@$(ECHO) "  make web         - Запустить веб-версию (Flask)"
	@$(ECHO) "  make clean       - Очистить временные файлы"
	@$(ECHO)
	@$(ECHO) "Платформо-специфичные цели:"
	@$(ECHO) "  make run-windows - Оптимизировано для Windows"
	@$(ECHO) "  make run-linux   - Оптимизировано для Linux"
	@$(ECHO) "  make run-mac     - Оптимизировано для macOS"
	@$(ECHO)
	@$(ECHO) "Для запуска в Windows используйте:"
	@$(ECHO) "  mingw32-make run-windows  или  make run-windows"
	@$(ECHO)
	@$(ECHO) "Для быстрого старта в Linux/macOS:"
	@$(ECHO) "  make venv && source venv/bin/activate && make install && make run"

# ============================================================================
# УСТАНОВКА
# ============================================================================

venv:
	@$(ECHO) "Создание виртуального окружения..."
	$(PYTHON) -m venv $(VENV_DIR)
ifeq ($(DETECTED_OS),Windows)
	@$(ECHO) "Активируйте командой: $(VENV_DIR)\Scripts\activate"
else
	@$(ECHO) "Активируйте командой: source $(VENV_DIR)/bin/activate"
endif

install:
	@$(ECHO) "Установка зависимостей..."
	$(PIP) install -r requirements.txt
	$(PIP) install -r test_requirements.txt
	@$(ECHO) "Зависимости установлены."

# ============================================================================
# ЗАПУСК НА РАЗНЫХ ПЛАТФОРМАХ
# ============================================================================

run:
	@$(ECHO) "Запуск на $(DETECTED_OS)..."
	$(PYTHON) chase_terminal.py

run-windows:
	@$(ECHO) "Запуск оптимизированной версии для Windows..."
	@chcp 65001 > nul 2>&1
	$(PYTHON) chase_terminal.py

run-linux:
	@$(ECHO) "Запуск оптимизированной версии для Linux..."
	$(PYTHON) chase_terminal.py

run-mac:
	@$(ECHO) "Запуск оптимизированной версии для macOS..."
	$(PYTHON) chase_terminal.py

# ============================================================================
# ВЕБ-ВЕРСИЯ
# ============================================================================

web-install:
	@$(ECHO) "Установка веб-зависимостей..."
	$(PIP) install flask gunicorn
	@$(ECHO) "Веб-зависимости установлены."

web-run:
	@$(ECHO) "Запуск веб-версии на http://localhost:5000"
	@$(ECHO) "Нажмите Ctrl+C для остановки"
	$(PYTHON) chase_web.py

web-run-linux:
	@$(ECHO) "Запуск веб-версии для Linux (с gunicorn)..."
	cd web && gunicorn -w 4 -b 0.0.0.0:5000 chase_web:app

# ============================================================================
# ТЕСТИРОВАНИЕ
# ============================================================================

test:
	@$(ECHO) "Запуск тестов..."
	$(PYTHON) -m pytest test_chase.py $(PYTEST_FLAGS)

test-windows:
	@$(ECHO) "Запуск тестов в Windows..."
	@chcp 65001 > nul 2>&1
	$(PYTHON) -m pytest test_chase.py $(PYTEST_FLAGS)

# ============================================================================
# СБОРКА И ДИСТРИБУЦИЯ
# ============================================================================

build-web:
	@$(ECHO) "Подготовка веб-версии..."
	$(MKDIR) $(WEB_DIR)$(PATH_SEP)$(TEMPLATES_DIR)
	$(CP) chase_web.py $(WEB_DIR)$(PATH_SEP)
	$(CP) chase_core.py $(WEB_DIR)$(PATH_SEP)
	$(CP) templates$(PATH_SEP)* $(WEB_DIR)$(PATH_SEP)$(TEMPLATES_DIR)$(PATH_SEP)
	@$(ECHO) "Веб-версия подготовлена в папке $(WEB_DIR)/"

# ============================================================================
# ОЧИСТКА
# ============================================================================

clean:
	@$(ECHO) "Очистка временных файлов..."
	-$(RMDIR) $(BUILD_DIR)
	-$(RMDIR) $(DIST_DIR)
	-$(RMDIR) $(WEB_DIR)
	-$(RMDIR) $(VENV_DIR)
	-$(RMDIR) __pycache__
	-$(RMDIR) *.pyc 2>/dev/null || true
	-$(RM) *.spec 2>/dev/null || true
	@$(ECHO) "Очистка завершена."

# ============================================================================
# ПРОВЕРКА ОКРУЖЕНИЯ
# ============================================================================

check:
	@$(ECHO) "Проверка окружения:"
	@$(ECHO) "ОС: $(DETECTED_OS)"
	@$(ECHO) "Python: $(shell $(PYTHON) --version 2>&1)"
	@$(ECHO) "Pip: $(shell $(PIP) --version 2>&1)"

# ============================================================================
# БЫСТРЫЙ СТАРТ
# ============================================================================

quick-start:
	@$(ECHO) "Быстрый старт Chase Game:"
	@$(ECHO) "1. Создать виртуальное окружение: make venv"
	@$(ECHO) "2. Активировать его:"
ifeq ($(DETECTED_OS),Windows)
	@$(ECHO) "   $(VENV_DIR)\Scripts\activate"
else
	@$(ECHO) "   source $(VENV_DIR)/bin/activate"
endif
	@$(ECHO) "3. Установить зависимости: make install"
	@$(ECHO) "4. Запустить игру: make run"
	@$(ECHO)
	@$(ECHO) "Для веб-версии:"
	@$(ECHO) "   make web-install"
	@$(ECHO) "   make web-run"

# ============================================================================
# ДЛЯ WINDOWS СОВМЕСТИМОСТЬ
# ============================================================================

# Псевдонимы для Windows (чтобы работало с mingw32-make)
windows-run: run-windows
windows-test: test-windows
web: web-run