# 🚀 Autonomous Warehouse Logistics AI Agent

An **AI-powered multi-agent system** designed to analyze, optimize, and improve warehouse logistics operations.
This project leverages **CrewAI, RAG (ChromaDB), and LLMs** to provide intelligent insights, detect delays, and recommend actionable improvements.

---

## 🧠 Key Features

### 🤖 Multi-Agent AI System (CrewAI)

* **Data Analyst Agent** → Extracts insights from structured data
* **Research Agent** → Performs external knowledge lookup
* **Manager Agent** → Coordinates agents and generates final responses

---

### 🔍 Retrieval-Augmented Generation (RAG)

* Context-aware responses using **ChromaDB**
* Improves accuracy by grounding responses in data

---

### 📊 Intelligent Query Handling

* **Dataset Queries** → Direct answers from structured data
* **Research Queries** → AI-generated insights using LLMs

---

### 🌐 Interactive Frontend

* Built using **Streamlit**
* Simple UI for querying warehouse data and insights

---

### ⚡ FastAPI Backend

* REST APIs for handling queries and agent orchestration
* High-performance asynchronous architecture

---

### 🐳 Containerization

* Fully containerized using **Docker**
* Ensures portability and consistent deployment

---

### 🔄 CI/CD Pipeline

* Implemented using **GitHub Actions**
* Automated:

  * Dependency installation
  * Build validation
  * Docker image creation

---

## 🏗️ Project Architecture

```
User (Browser)
      ↓
Frontend (Streamlit)
      ↓
Backend (FastAPI APIs)
      ↓
Multi-Agent System (CrewAI)
      ↓
RAG Layer (ChromaDB + Knowledge Base)
      ↓
LLM (Groq - LLaMA 3) + Tavily Search
```

---

## 🗂️ Project Structure

```
.
├── backend/
│   ├── api.py
│   ├── services/
│   ├── crew/
│   ├── rag/
│   ├── memory/
│   └── tools/
├── frontend/
│   └── app.py
├── vector_db/
├── knowledge_base/
├── requirements.txt
├── Dockerfile
└── .github/workflows/ci-cd.yml
```

---

## ⚙️ Tech Stack

| Category     | Technology             |
| ------------ | ---------------------- |
| Backend      | FastAPI                |
| Frontend     | Streamlit              |
| AI Framework | CrewAI                 |
| LLM          | Groq (LLaMA 3)         |
| Vector DB    | ChromaDB               |
| Search API   | Tavily                 |
| DevOps       | Docker, GitHub Actions |
| Cloud        | AWS EC2                |

---

## 🚀 Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/sarthaakdubey/Autonomous-warehouse-logistic-agentic-ai-main
cd Autonomous-warehouse-logistic-agentic-ai-main
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

---

### ▶️ Run Application

#### Backend

```bash
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend

```bash
streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
```

---

## 🐳 Docker Setup

### Build Image

```bash
docker build -t warehouse-ai .
```

### Run Container

```bash
docker run -d -p 8000:8000 -p 8501:8501 warehouse-ai
```

---

## ☁️ AWS Deployment (EC2)

1. Launch EC2 instance (Ubuntu)
2. Configure security groups (ports 22, 8000, 8501)
3. Install Docker & Git
4. Clone repository
5. Build and run Docker container

Access:

* Backend → `http://<public-ip>:8000/docs`
* Frontend → `http://<public-ip>:8501`

---

## 🧪 Example Queries

### 📊 Dataset Queries

* `order 1003 details`
* `which warehouse has most delays`

### 🔍 Research Queries

* `why orders delayed`
* `how to improve warehouse operations`
* `latest warehouse automation technologies`

---

## 💼 Resume Description

> Designed and deployed an AI-powered warehouse logistics system using a multi-agent architecture (CrewAI) with RAG-based intelligence (ChromaDB). Built scalable APIs using FastAPI and an interactive frontend using Streamlit. Containerized the application using Docker and deployed it on AWS EC2 with configured security groups and public access.

---

## 🔮 Future Enhancements

* AWS ECS / Kubernetes deployment
* Real-time data streaming integration
* Advanced analytics dashboard
* Role-based access control (RBAC)
* Monitoring & logging (Prometheus + Grafana)

---

## 👨‍💻 Author

**Sarthak Dubey**
B.Tech CSE | AI & Full Stack Developer

---

## ⭐ Key Highlights

* Multi-Agent AI System
* RAG-based intelligent responses
* Full-stack development
* Cloud deployment (AWS EC2)
* Production-ready architecture

---

## 📌 License

This project is open-source and available under the MIT License.
