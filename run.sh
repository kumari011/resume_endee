#!/bin/bash
echo "============================================"
echo "  AI Resume Analyzer - One-Click Setup"
echo "============================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed."
    echo "Install it: sudo apt install python3 python3-pip"
    exit 1
fi

# Install dependencies
echo "[1/2] Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet

echo "[2/2] Starting server..."
echo
echo "============================================"
echo "  Open http://127.0.0.1:8000 in browser"
echo "  Press Ctrl+C to stop"
echo "============================================"
echo

# Open browser (works on Linux & macOS)
(sleep 3 && (xdg-open http://127.0.0.1:8000 2>/dev/null || open http://127.0.0.1:8000 2>/dev/null)) &

# Run the app
python3 app.py
