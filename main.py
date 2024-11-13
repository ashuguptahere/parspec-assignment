import os
import sys
import time
import threading
import subprocess
import http.client
from urllib.parse import urlparse

curr = os.getcwd()

backend_dir = os.path.join(curr, "backend")
frontend_dir = os.path.join(curr, "frontend")

npm_path = "/usr/bin/npm"
python_path = sys.executable


def install_frontend_dependencies():
    print("Installing frontend dependencies...")
    subprocess.run([npm_path, "install"], cwd=frontend_dir)


def start_frontend():
    print("Starting frontend...")
    frontend_process = subprocess.Popen([npm_path, "run", "dev"], cwd=frontend_dir)
    return frontend_process


def start_backend():
    print("Starting backend...")
    backend_process = subprocess.Popen(
        [python_path, "main.py"], cwd=backend_dir
    )
    return backend_process


def wait_for_process(proc, name):
    try:
        proc.wait()
    except KeyboardInterrupt:
        print(f"Terminating {name} process...")
        proc.terminate()
        proc.wait()


def is_backend_ready(url="http://localhost:5000"):
    parsed_url = urlparse(url)
    connection = http.client.HTTPConnection(parsed_url.hostname, parsed_url.port)

    try:
        connection.request("GET", parsed_url.path)
        response = connection.getresponse()
        return response.status == 200
    except (http.client.HTTPException, ConnectionRefusedError):
        return False
    finally:
        connection.close()


if __name__ == "__main__":
    install_frontend_dependencies()
    backend_process = start_backend()

    backend_ready = False
    while not backend_ready:
        print("Model is too big to load, please wait for a while...")
        time.sleep(30)
        backend_ready = is_backend_ready()

    frontend_process = start_frontend()

    backend_thread = threading.Thread(
        target=wait_for_process, args=(backend_process, "backend")
    )
    frontend_thread = threading.Thread(
        target=wait_for_process, args=(frontend_process, "frontend")
    )

    backend_thread.start()
    frontend_thread.start()

    backend_thread.join()
    frontend_thread.join()

    print("Both processes terminated.")
