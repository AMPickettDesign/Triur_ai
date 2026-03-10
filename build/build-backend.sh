#!/bin/bash
echo "[Triur.ai] Building Python backend with PyInstaller..."

cd "$(dirname "$0")"

# Install PyInstaller if not present
pip install pyinstaller --quiet

# Clean previous build
rm -rf ../dist/triur-brain
rm -rf ../build/pyinstaller-work

# Build
pyinstaller triur.spec --distpath ../dist --workpath ../build/pyinstaller-work --clean

if [ $? -eq 0 ]; then
    echo "[Triur.ai] Backend built successfully."
    echo "[Triur.ai] Output: dist/triur-brain"
else
    echo "[Triur.ai] Build failed. Check errors above."
fi
