@echo on

docker start my-mysql

timeout /t 5 /nobreak > nul

call .\venv\Scripts\Activate.bat

cd my-app

echo Server for Api: http://127.0.0.1:8000/docs
python -m uvicorn main:app --reload

pause