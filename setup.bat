@echo off
python3 -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    python -m pip install -r requirements.txt
)