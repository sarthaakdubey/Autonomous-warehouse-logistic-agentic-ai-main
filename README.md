# 🚀 Autonomous Warehouse Logistics AI Agent

An AI-powered multi-agent system for intelligent warehouse analysis and optimization.. 
This project uses FastAPI, Streamlit, CrewAI, and RAG (ChromaDB) to provide insights, detect delays, and recommend improvements in logistics operations.

----

## 🧠 Features

- 🤖 Multi-Agent AI System (CrewAI)
  - Data Analyst Agent  
  - Research Agent  
  - Manager Agent  

- 📊 Smart Query Handling
  - Dataset lookup (exact answers)  
  - Research mode (AI-generated insights)  

- 🔍 RAG (Retrieval-Augmented Generation)
  - Context-aware responses using ChromaDB  

- 🌐 Interactive UI (Streamlit)

- ⚡ FastAPI Backend

- 🐳 Docker Support (Containerized Backend)

- 🔄 CI/CD Pipeline (GitHub Actions)
  - Automated dependency install  
  - Automated Docker build  

---

## 🏗️ Project Structure
.
├── backend/
│ ├── api.py
│ ├── services/
│ ├── crew/
│ ├── rag/
│ ├── memory/
│ └── tools/
│
├── frontend/
│ └── app.py
│
├── vector_db/
├── knowledge_base/
├── requirements.txt
├── Dockerfile
└── .github/workflows/ci-cd.yml

---

## ⚙️ Tech Stack

- Backend: FastAPI  
- Frontend: Streamlit  
- AI: CrewAI  
- Vector DB: ChromaDB  
- LLM: Groq (LLaMA 3)  
- Search: Tavily API  
- DevOps: Docker, GitHub Actions  

---

## 🚀 Setup Instructions

### 1. Clone Repository
git clone https://github.com/sarthaakdubey/Autonomous-warehouse-logistic-agentic-ai-main
cd Autonomous-warehouse-logistic-agentic-ai-main

---

### 2. Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate

---

### 3. Install Dependencies
pip install -r requirements.txt

---

### 4. Add Environment Variables

Create a `.env` file:
GROQ_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key

---

## ▶️ Run Application

### Run Backend
python -m uvicorn backend.api:app --reload

👉 Open:
http://127.0.0.1:8000/docs

---

### Run Frontend
streamlit run frontend/app.py

---

## 🐳 Docker Usage

### Build Image
docker build -t warehouse-ai .

---

## 🔄 CI/CD Pipeline

Implemented using GitHub Actions:

- Runs on every push  
- Installs dependencies  
- Validates application  
- Builds Docker image  

---

## 🧪 Example Queries

### Dataset Queries
- order 1003 details  
- which warehouse has most delays  

### Research Queries
- why orders delayed  
- how to improve warehouse operations  
- latest warehouse automation technologies  

---

## 💼 Resume Description

Designed and implemented an AI-powered warehouse logistics system using FastAPI and Streamlit, integrating multi-agent architecture (CrewAI) with RAG-based intelligence. Containerized the application using Docker and implemented a CI/CD pipeline using GitHub Actions to automate testing and deployment.

---

## 👨‍💻 Author

Sarthak Dubey  
B.Tech CSE | AI & Full Stack Developer  

---

## ⭐ Future Improvements

- AWS Deployment  
- Kubernetes Integration  
- Real-time Data Integration  
- Advanced Analytics Dashboard  

---

## 📌 Summary

This project demonstrates:
- AI system design  
- Full-stack development  
- DevOps (Docker + CI/CD)  
- Production-ready architecture  
