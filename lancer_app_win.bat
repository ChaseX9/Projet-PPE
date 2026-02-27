@echo off
setlocal
title CapInvest Academy - Windows Launcher

echo.
echo  🚀 CapInvest Academy - Chargement...
echo  ====================================
echo.

:: Check if port 8000 is in use and kill the process
echo [*] Verification du port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo [!] Liberation du port 8000 (PID %%a)...
    taskkill /f /pid %%a >nul 2>&1
)

:: Set PYTHONPATH to project root
set PYTHONPATH=%CD%

:: Ch:: Check for venv
if exist venv (
    echo [v] Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
) else (
    echo [!] Erreur : Dossier 'venv' introuvable. Veuillez le creer (voir README.md).
    pause
    exit /b
)

:: Add current directory to PYTHONPATH
set PYTHONPATH=%PYTHONPATH%;.

:: Check for port 8000
echo [*] Verification du port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo [!] Le port 8000 est occupe par le PID %%a. Fermeture...
    taskkill /F /PID %%a
)

echo [*] Lancement du serveur Uvicorn...
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload

pause
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Une erreur est survenue lors du lancement.
    echo [!] Verifiez que Python est bien installe et que les dependances sont a jour.
    pause
)
