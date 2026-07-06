#!/bin/bash
# FarmWise AI — Linux/Mac Quick Start

set -e

echo ""
echo "===================================================="
echo "  FarmWise AI — Quick Start"
echo "===================================================="
echo ""

# Backend
echo "[1/4] Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "[2/4] Installing backend dependencies..."
pip install -r requirements.txt

echo "[3/4] Ingesting knowledge base..."
[ ! -f .env ] && cp .env.example .env && echo "Created .env — fill in your IBM Watsonx credentials."
python scripts/ingest_knowledge.py

echo "[4/4] Starting FastAPI backend..."
uvicorn main:app --reload --port 8000 &

cd ../frontend

echo "Installing frontend dependencies..."
npm install

echo "Starting Next.js frontend..."
npm run dev &

echo ""
echo "===================================================="
echo "  FarmWise AI is running!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
echo "===================================================="
