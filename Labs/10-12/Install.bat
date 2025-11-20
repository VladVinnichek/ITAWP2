@echo off
chcp 65001 >nul
title Установка Django проекта - Product Catalog

echo ===============================================
echo         УСТАНОВКА DJANGO ПРОЕКТА
echo ===============================================

set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%myvenv"
set "PROJECT_DIR=%SCRIPT_DIR%product_catalog_project"

echo Проверка виртуального окружения...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Виртуальное окружение не найдено!
    echo Создание виртуального окружения...
    cd /d "%SCRIPT_DIR%"
    python -m venv myvenv
    echo Виртуальное окружение создано успешно!
) else (
    echo Виртуальное окружение уже существует.
)

echo Активация виртуального окружения...
cd /d "%SCRIPT_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

echo Установка Django...
pip install django
echo Django установлен успешно!

echo Установка ngrok...
pip install pyngrok

echo Создание проекта...
if not exist "%PROJECT_DIR%" (
    django-admin startproject product_catalog_project
    echo Проект создан успешно!
) else (
    echo Проект уже существует.
)

echo Создание приложения...
cd /d "%PROJECT_DIR%"
if not exist "%PROJECT_DIR%\product_catalog" (
    python manage.py startapp product_catalog
    echo Приложение создано успешно!
) else (
    echo Приложение уже существует.
)

echo.
echo ===============================================
echo    УСТАНОВКА ЗАВЕРШЕНА УСПЕШНО!
echo ===============================================
echo.
echo Нажмите Enter для закрытия...
pause >nul