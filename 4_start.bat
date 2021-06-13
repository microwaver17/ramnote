@echo off
echo Index Path: http://127.0.0.1:5000/static/index.html
title RAMNOTE
cd server
rem set FLASK_ENV=development
venv\Scripts\flask run
cd ..\
