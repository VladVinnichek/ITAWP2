@echo off
chcp 65001 >nul
title Установка Django проекта - Переводчик

echo ===============================================
echo         УСТАНОВКА DJANGO ПРОЕКТА - ПЕРЕВОДЧИК
echo ===============================================

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%myvenv"
set "PROJECT_DIR=%SCRIPT_DIR%translator_project"

echo Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не установлен или не добавлен в PATH!
    echo Установите Python с официального сайта:
    echo https://www.python.org/downloads/
    echo.
    echo Нажмите Enter для закрытия...
    pause >nul
    exit /b 1
)

echo Проверка виртуального окружения...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено!
    echo Создание виртуального окружения...
    cd /d "%SCRIPT_DIR%"
    python -m venv myvenv
    if errorlevel 1 (
        echo Ошибка при создании виртуального окружения!
        echo Проверьте установку Python.
        echo.
        echo Нажмите Enter для закрытия...
        pause >nul
        exit /b 1
    )
    echo Виртуальное окружение создано успешно!
) else (
    echo Виртуальное окружение уже существует.
)

echo Активация виртуального окружения...
cd /d "%SCRIPT_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Установка Django...
pip install django
if errorlevel 1 (
    echo Ошибка при установке Django!
    echo.
    echo Нажмите Enter для закрытия...
    pause >nul
    exit /b 1
)
echo Django установлен успешно!

echo Установка дополнительных пакетов для переводчика...
pip install requests googletrans==3.1.0a0
if errorlevel 1 (
    echo Внимание: Не удалось установить пакеты для перевода!
    echo Базовый функционал Django будет работать.
) else (
    echo Пакеты для перевода установлены успешно!
)

echo Проверка существования проекта...
if not exist "%PROJECT_DIR%" (
    echo Проект не найден в ожидаемой папке.
    echo Убедитесь, что проект находится в: %PROJECT_DIR%
    echo.
    echo Нажмите Enter для закрытия...
    pause >nul
    exit /b 1
) else (
    echo Проект найден: %PROJECT_DIR%
)

echo Проверка приложения translator...
if not exist "%PROJECT_DIR%\translator" (
    echo Приложение translator не найдено!
    echo.
    echo Нажмите Enter для закрытия...
    pause >nul
    exit /b 1
) else (
    echo Приложение translator найдено.
)

echo Настройка проекта...
cd /d "%PROJECT_DIR%"

echo Создание базовых миграций...
python manage.py makemigrations
python manage.py migrate

echo.
echo ===============================================
echo    УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!
echo ===============================================
echo.
echo Созданные файлы и папки:
echo - myvenv\ (виртуальное окружение)
echo - translator_project\ (проект Django)
echo   - translator\ (приложение переводчика)
echo.
echo Для запуска проекта используйте Run.bat
echo Для создания администратора - Admin.bat
echo Для настройки публичного доступа - Public.bat
echo.
echo Нажмите Enter для закрытия...
pause >nul