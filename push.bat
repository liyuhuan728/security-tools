@echo off
REM ============================================
REM  push.bat - One-click upload to GitHub
REM  Double-click this file, type a short note, done.
REM ============================================

cd /d "%~dp0"

echo.
echo   === Upload to GitHub ===
echo.

set /p MSG=What did you change? (press Enter to use date):

if "%MSG%"=="" set MSG=update %date% %time%

echo.
echo [1/3] Staging files...
git add -A

echo [2/3] Committing: %MSG%
git commit -m "%MSG%"

echo [3/3] Pushing to GitHub...
git push

echo.
echo   === Done! Check github.com/liyuhuan728/security-tools ===
echo.
pause
