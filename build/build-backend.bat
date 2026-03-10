@echo off
echo [Triur.ai] Building Python backend with PyInstaller...

cd /d "%~dp0"

REM Install PyInstaller if not present
pip install pyinstaller --quiet

REM Clean previous build
if exist "..\dist\triur-brain" rmdir /s /q "..\dist\triur-brain"
if exist "..\build\__pycache__" rmdir /s /q "..\build\__pycache__"

REM Build
pyinstaller triur.spec --distpath ../dist --workpath ../build/pyinstaller-work --clean

if %ERRORLEVEL% EQU 0 (
    echo [Triur.ai] Backend built successfully.
    echo [Triur.ai] Output: dist/triur-brain.exe
) else (
    echo [Triur.ai] Build failed. Check errors above.
    pause
)
