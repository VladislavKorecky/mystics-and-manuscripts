@echo off
python3 -m mystics_and_manuscripts.main

if %errorlevel% neq 0 (
    python -m mystics_and_manuscripts.main
)