@echo off
cd /d C:\Business_Software
call venv\Scripts\activate
cd core

:: Start Django server in a new command window
start cmd /k "python manage.py runserver 127.0.0.1:8000"

:: Wait a few seconds to allow server to start
timeout /t 5 >nul

:: Open browser
start http://127.0.0.1:8000
