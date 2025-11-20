@echo off
chcp 65001 >nul
title Запуск Django сервера - Product Catalog

echo ===============================================
echo    ЗАПУСК ПРОЕКТА DJANGO - PRODUCT CATALOG
echo ===============================================

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%myvenv"
set "PROJECT_DIR=%SCRIPT_DIR%product_catalog_project"

echo Проверка виртуального окружения...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено!
    echo Проект не установлен!
    pause
    exit /b 1
)

echo Активация виртуального окружения...
call "%VENV_DIR%\Scripts\activate.bat"

echo Установка/проверка Django...
pip install django

echo Переход в папку проекта...
cd /d "%PROJECT_DIR%"

echo Проверка миграций...
python manage.py makemigrations
python manage.py migrate

echo Запуск сервера разработки...
echo.
echo ===============================================
echo    СЕРВЕР ЗАПУЩЕН
echo    Локальный URL: http://127.0.0.1:8000/
echo    Админ-панель: http://127.0.0.1:8000/admin/
echo.
echo    Для публичного доступа запустите Public.bat
echo    в отдельном окне командной строки
echo ===============================================
echo.

start http://127.0.0.1:8000/
python manage.py runserver

pause