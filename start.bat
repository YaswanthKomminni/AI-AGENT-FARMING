@echo off
echo.
echo ====================================================
echo   FarmWise AI — Windows Quick Start
echo ====================================================
echo.

:: Backend setup
echo [1/4] Setting up Python virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate

echo [2/4] Installing backend dependencies...
pip install -r requirements.txt

echo [3/4] Ingesting knowledge base into ChromaDB...
if not exist .env (
    copy .env.example .env
    echo Created .env — please fill in your IBM Watsonx credentials.
)
python scripts/ingest_knowledge.py

echo [4/4] Starting FastAPI backend on port 8000...
start "FarmWise-Backend" cmd /k "call venv\Scripts\activate && uvicorn main:app --reload --port 8000"

cd ..\frontend

echo Installing frontend dependencies...
npm install

echo Starting Next.js frontend on port 3000...
start "FarmWise-Frontend" cmd /k "npm run dev"

echo.
echo ====================================================
echo   FarmWise AI is starting up!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo ====================================================
echo.
pause
