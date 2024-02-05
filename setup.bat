@echo off
pip install -r requirements.txt

if %errorlevel% neq 0 (
    pip3 install -r requirements.txt
)