@echo off
title RAMNOTE
echo.
echo Index Path: http://127.0.0.1:5000/static/index.html
echo.
cd server
rem set FLASK_ENV=development
start http://127.0.0.1:5000/static/index.html
venv\Scripts\flask run
cd ..\