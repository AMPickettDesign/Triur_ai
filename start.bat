@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Triur_ai - Three AI Companions
echo ========================================
echo.

:: Check if Python is installed
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo   ERROR: Python is not installed.
    echo   Please install Python 3.14+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

:: Check Python version (need 3.14+)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)
if !PYMAJOR! LSS 3 (
    echo.
    echo   ERROR: Python version !PYVER! is too old.
    echo   Please upgrade to Python 3.14+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)
if !PYMAJOR! EQU 3 if !PYMINOR! LSS 14 (
    echo.
    echo   WARNING: Python !PYVER! detected. Version 3.14+ recommended.
    echo   Triur_ai may not work correctly with older versions.
    echo.
)

:: Check if Ollama is installed
echo [2/5] Checking Ollama...
where ollama >nul 2>&1
if errorlevel 1 (
    echo.
    echo   ERROR: Ollama is not installed.
    echo   Please install Ollama from https://ollama.com/
    echo.
    pause
    exit /b 1
)

:: Check if Ollama is running, start it if not
echo [3/5] Checking Ollama status...
tasklist /fi "imagename eq ollama.exe" 2>nul | find "ollama.exe" >nul
if errorlevel 1 (
    echo   Starting Ollama...
    start "" "C:\Users\Zombi\AppData\Local\Programs\Ollama\ollama.exe" serve
    timeout /t 5 /noq >nul
) else (
    echo   Ollama is already running.
)

:: Check if the model is pulled
echo [4/5] Checking AI model...
ollama list 2>nul | find "dolphin-llama3:8b" >nul
if errorlevel 1 (
    echo.
    echo   INFO: AI model not found. Pulling it now...
    echo   This may take a few minutes...
    echo.
    ollama pull dolphin-llama3:8b
    if errorlevel 1 (
        echo.
        echo   ERROR: Failed to pull AI model.
        echo   Please run: ollama pull dolphin-llama3:8b
        echo.
        pause
        exit /b 1
    )
)
echo   AI model ready.

:: Install Python dependencies if needed
echo [5/5] Checking Python dependencies...
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo   Creating virtual environment...
    python -m venv venv
)
echo   Installing Flask and dependencies...
call venv\Scripts\python.exe -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo.
    echo   ERROR: Failed to install Python dependencies.
    echo   Please run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:: Start Triur_ai
echo.
echo ========================================
echo   Starting Triur_ai...
echo ========================================
echo.

:: Start the brain server
start "" /min cmd /c "cd /d "%~dp0" && venv\Scripts\python.exe src\server.py"
timeout /t 3 /noq >nul

:: Start the Electron app
cd /d "%~dp0\app"
start "" npx electron .

echo   Triur_ai is running!
echo.
pause
