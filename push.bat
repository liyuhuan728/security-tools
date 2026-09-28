@echo off
REM ============================================
REM  push.bat - One-click upload to GitHub
REM  Double-click this file, type a short note, done.
REM ============================================

cd /d "%~dp0"

REM Portable git is not in system PATH, add it manually
set "PATH=C:\Users\28638\.workbuddy\binaries\PortableGit\versions\1.2.0\cmd;%PATH%"

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
echo   (this may take a few seconds)
git push

echo.
if errorlevel 1 (
  echo   === FAILED ===
  echo   Something went wrong. Screenshot the red text above and send it over.
) else (
  echo   === Done! Check github.com/liyuhuan728/security-tools ===
)
echo.
echo   Note: a line saying "hostfile_replace_entries" or "update_known_hosts"
echo   is a harmless Windows warning - if you see "Done!" you are fine.
echo.
pause
