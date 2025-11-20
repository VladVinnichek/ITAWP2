@echo off
chcp 65001 >nul
title Публичный доступ Django - Переводчик

echo ===============================================
echo    ЗАПУСК ПУБЛИЧНОГО ДОСТУПА
echo ===============================================

set "SCRIPT_DIR=%~dp0"

cd /d "%SCRIPT_DIR%"

echo Проверка cloudflared...
if exist "cloudflared.exe" (
    echo cloudflared найден в папке.
) else (
    echo Установка cloudflared...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"
    echo cloudflared установлен успешно!
)

echo.
echo Проверка запущенного Django сервера...
timeout /t 2 /nobreak >nul

echo.
echo ===============================================
echo    ЗАПУСК CLOUDFLARE TUNNEL
echo ===============================================
echo.
echo    Ожидайте получение публичного URL...
echo    Это может занять несколько секунд...
echo.
echo    Сервер должен быть запущен через Run.bat
echo    Локальный URL: http://127.0.0.1:8000/
echo.
echo ===============================================
echo.

cloudflared.exe tunnel --url http://127.0.0.1:8000

pause