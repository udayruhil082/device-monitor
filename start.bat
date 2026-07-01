@echo off
echo Starting Device Health Monitor...
start cmd /k "cd /d C:\Users\Vanshu\OneDrive\Desktop\IIIT-D\device-monitor && venv\Scripts\activate && uvicorn backend.main:app --reload"
timeout /t 3 /nobreak
start cmd /k "cd /d C:\Users\Vanshu\OneDrive\Desktop\IIIT-D\device-monitor && venv\Scripts\activate && streamlit run dashboard/app.py"
timeout /t 3 /nobreak
start cmd /k "cd /d C:\Users\Vanshu\OneDrive\Desktop\IIIT-D\device-monitor && venv\Scripts\activate && python devices/mock_all.py"
echo All started! Opening dashboard...
start http://localhost:8501