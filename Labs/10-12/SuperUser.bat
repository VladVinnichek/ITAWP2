@echo off
chcp 65001 >nul
title Создание администратора - Product Catalog

echo ===============================================
echo        СОЗДАНИЕ АДМИНИСТРАТОРА
echo ===============================================

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%myvenv"
set "PROJECT_DIR=%SCRIPT_DIR%product_catalog_project"

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

:create_superuser
echo Создание суперпользователя...
python manage.py createsuperuser

if %errorlevel% equ 0 (
    echo Суперпользователь создан успешно!
) else (
    echo Ошибка при создании суперпользователя!
)

echo.
choice /C YN /M "Хотите добавить ещё одного администратора"
if %errorlevel% equ 1 (
    goto create_superuser
) else (
    echo.
    echo Нажмите Enter для закрытия...
    pause >nul
)