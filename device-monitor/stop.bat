@echo off
echo Stopping all services...
taskkill /f /im python.exe
taskkill /f /im uvicorn.exe
echo Done! All stopped.
pause