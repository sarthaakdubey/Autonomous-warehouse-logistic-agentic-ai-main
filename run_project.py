import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")

backend = None
frontend = None

def start_backend():
    print("Starting FastAPI backend...")
    return subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "backend.api:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BASE_DIR
    )

def start_frontend():
    print("Starting Streamlit frontend...")
    return subprocess.Popen(
        [PYTHON, "-m", "streamlit", "run", "frontend/app.py"],
        cwd=BASE_DIR
    )

if __name__ == "__main__":
    try:
        backend = start_backend()

        # wait until backend actually starts
        print("Waiting for backend to boot...")
        time.sleep(5)

        frontend = start_frontend()

        print("\nProject is running!")
        print("Backend: http://127.0.0.1:8000/docs")
        print("Frontend: http://localhost:8501")
        print("Press CTRL+C to stop everything\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping servers...")

        if backend:
            backend.terminate()
        if frontend:
            frontend.terminate()

        sys.exit()
