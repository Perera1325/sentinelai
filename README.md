\# SentinelAI – AI Powered API Security Platform



SentinelAI is an AI-powered API gateway security platform that detects abnormal API behavior using rule-based detection, machine learning, and GenAI-style explanations.



The system monitors API traffic in real time, identifies suspicious request patterns, classifies attacks using ML, and explains incidents in natural language.



Built with FastAPI, Python, SQLite, scikit-learn, and Docker.



---



\## 🚀 Features



\- API Gateway using FastAPI

\- Real-time traffic logging

\- SQLite-based request storage

\- Rule-based attack detection

\- Machine Learning classifier for abnormal behavior

\- GenAI-style natural language explanations

\- Alert generation

\- Dockerized deployment

\- Swagger UI for API testing



---



\## 🧠 Architecture



Client  

↓  

FastAPI Gateway  

↓  

Traffic Logger Middleware  

↓  

SQLite Database  

↓  

Rule Engine + ML Classifier  

↓  

GenAI Explanation Layer  

↓  

Alerts \& REST APIs  



---



\## 📦 Tech Stack



\- Python

\- FastAPI

\- SQLite

\- Pandas

\- Scikit-learn

\- Docker / Docker Compose



---



\## ▶ Run Locally



```bash

python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt

uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/docs

🐳 Run with Docker
docker compose build
docker compose up


Open:

http://127.0.0.1:8001/docs

🔍 Main Endpoints

/logs – View traffic logs

/detect – Rule-based detection

/ml-detect – ML classification

/explain – GenAI-style explanations

/alerts – Security alerts

🎯 Use Case

Detect API abuse

Identify bot traffic

Monitor suspicious request rates

Explain security incidents in plain English

📈 Future Improvements

Real LLM integration (OpenAI / Ollama)

JWT authentication

Dashboard UI

Kubernetes deployment

Redis caching

Cloud deployment (AWS)

👤 Author

Vinod Perera
GitHub: https://github.com/Perera1325


Save.

---

# ✅ STEP 2 — Commit Day 07

```bash
git add .
git commit -m "Day 07: Final README, architecture, and project polish"
git push


🎤 Demo Script (use this when showing project)

Say this:

SentinelAI is an AI-powered API security platform.
It logs API traffic, detects abnormal behavior using both rule-based logic and machine learning, and explains attacks in natural language.
The system is containerized with Docker and exposes REST endpoints via FastAPI.
This simulates how modern API gateways can integrate AI for threat detection.








