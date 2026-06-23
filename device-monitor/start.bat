@echo off
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn backend.main:app --reload"
timeout /t 3
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run dashboard/app.py"
echo Started! Open http://localhost:8501