import subprocess
import os

def start_streamlit():
    streamlit_dir = os.path.join(os.getcwd(), "Streamlit_Frontend")
    subprocess.run(["streamlit", "run", "frontend.py", "--server.port", "3030"], cwd=streamlit_dir)

def start_fastapi():
    fastapi_dir = os.path.join(os.getcwd(), "FastAPI_Backend")
    subprocess.run(["uvicorn", "main:app", "--port", "8080", "--reload"], cwd=fastapi_dir)

if __name__ == "__main__":
    import threading
    t1 = threading.Thread(target=start_streamlit)
    t2 = threading.Thread(target=start_fastapi)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
