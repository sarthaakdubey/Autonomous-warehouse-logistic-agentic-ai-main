# Use Python 3.11 (important)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Start both backend & frontend
CMD ["sh", "-c", "uvicorn backend.api:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]