@echo off
chcp 65001 >nul
title Миграции базы данных - Переводчик

echo ===============================================
echo        МИГРАЦИИ БАЗЫ ДАННЫХ
echo ===============================================

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%myvenv"
set "PROJECT_DIR=%SCRIPT_DIR%translator_project"

echo Проверка виртуального окружения...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Ошибка: Виртуальное окружение не найдено!
    echo Проект не установлен!
    echo.
    echo Нажмите Enter для закрытия...
    pause >nul
    exit /b 1
)

echo Активация виртуального окружения...
cd /d "%SCRIPT_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Переход в папку проекта...
cd /d "%PROJECT_DIR%"

echo Создание миграций...
python manage.py makemigrations

echo Применение миграций...
python manage.py migrate

echo.
echo ===============================================
echo    МИГРАЦИИ ВЫПОЛНЕНЫ УСПЕШНО!
echo ===============================================
echo.
echo Нажмите Enter для закрытия...
pause >nul