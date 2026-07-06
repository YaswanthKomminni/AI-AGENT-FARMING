# 🌾 FarmWise AI — Smart Farming Advisor powered by IBM Granite + RAG

> An intelligent AI-powered agricultural assistant that empowers small and marginal farmers with accurate, real-time, localized, and multilingual farming guidance.

---

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     React.js Frontend                        │
│        Voice Input → Chat UI → Multilingual Display         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP / WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ RAG Pipeline│  │ Agent Router  │  │  Voice/TTS/STT    │  │
│  └──────┬──────┘  └──────┬───────┘  └───────────────────┘  │
│         │                │                                   │
│  ┌──────▼──────┐  ┌──────▼───────────────────────────────┐  │
│  │ ChromaDB    │  │   Feature Modules                     │  │
│  │ Vector DB   │  │  Crops │ Weather │ Pest │ Market      │  │
│  └─────────────┘  │  Irrigation │ Fertilizer │ Schemes   │  │
│                   └──────────────────────────────────────┘  │
│                          │                                   │
│                   ┌──────▼──────────┐                        │
│                   │ IBM Watsonx.ai  │                        │
│                   │ Granite LLM     │                        │
│                   └─────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
┌────────▼────────┐  ┌────────▼──────┐  ┌─────────▼────────┐
│  Weather API    │  │ Mandi Price   │  │ Govt Schemes DB  │
│  (OpenMeteo)    │  │ API           │  │                  │
└─────────────────┘  └───────────────┘  └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- IBM Watsonx.ai account (Cloud Lite)

### 1. Clone & Setup Environment

```bash
git clone <repo>
cd farming-ibm

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and fill environment variables
cp .env.example .env

# Frontend
cd ../frontend
npm install
```

### 2. Configure IBM Watsonx Credentials

Edit `backend/.env`:
```
IBM_WATSONX_API_KEY=your_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### 3. Ingest Knowledge Base

```bash
cd backend
python scripts/ingest_knowledge.py
```

### 4. Run the Application

```bash
# Terminal 1 — Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
```

Open http://localhost:3000

---

## 📦 Project Structure

```
farming-ibm/
├── backend/
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Configuration & env vars
│   ├── requirements.txt
│   ├── .env.example
│   ├── agents/
│   │   ├── farming_agent.py       # Main LangChain agent
│   │   └── tools.py               # Agent tools registry
│   ├── rag/
│   │   ├── pipeline.py            # RAG pipeline
│   │   ├── embeddings.py          # Embedding model
│   │   └── vectorstore.py         # ChromaDB integration
│   ├── modules/
│   │   ├── crops.py               # Crop recommendations
│   │   ├── weather.py             # Weather insights
│   │   ├── pest.py                # Pest & disease diagnosis
│   │   ├── irrigation.py          # Irrigation guidance
│   │   ├── market.py              # Mandi prices
│   │   ├── fertilizer.py          # Fertilizer advice
│   │   └── schemes.py             # Government schemes
│   ├── voice/
│   │   ├── stt.py                 # Speech-to-Text
│   │   └── tts.py                 # Text-to-Speech
│   ├── translation/
│   │   └── translator.py          # Multilingual support
│   ├── knowledge_base/
│   │   ├── crops.txt
│   │   ├── pest_diseases.txt
│   │   ├── fertilizers.txt
│   │   ├── irrigation.txt
│   │   ├── government_schemes.txt
│   │   └── farming_practices.txt
│   └── scripts/
│       └── ingest_knowledge.py    # Knowledge ingestion script
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── public/
    └── src/
        ├── app/
        │   ├── layout.tsx
        │   ├── page.tsx
        │   └── globals.css
        ├── components/
        │   ├── ChatInterface.tsx
        │   ├── VoiceInput.tsx
        │   ├── WeatherWidget.tsx
        │   ├── MarketPrices.tsx
        │   ├── LanguageSelector.tsx
        │   └── FarmingCards.tsx
        └── lib/
            └── api.ts
```

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🌾 Crop Advisor | Soil+Season+Climate based crop recommendations |
| 🌦 Weather | Real-time forecasts via OpenMeteo API |
| 🪲 Pest Diagnosis | Symptom-based identification + treatment |
| 💧 Irrigation | Water scheduling & conservation tips |
| 💰 Mandi Prices | Live market prices comparison |
| 🌱 Fertilizer | Nutrient analysis + organic alternatives |
| 📢 Govt Schemes | Subsidies, insurance, loan eligibility |
| 🎙 Voice | STT + TTS in regional Indian languages |
| 🌐 Multilingual | Hindi, Tamil, Telugu, Kannada, Bengali + more |

## 📄 License

MIT License — See LICENSE file.
