"""
Simple server to test the Ratoncito Pérez frontend
"""
import http.server
import socketserver
import webbrowser
import os
from threading import Thread
import time

def start_api_server():
    """Start the FastAPI server in a separate thread"""
    import subprocess
    import sys

    # Prefer a project virtualenv if present, otherwise use the current Python executable
    venv_python = os.path.join(os.getcwd(), '.venv', 'bin', 'python')
    if os.path.exists(venv_python):
        python_exe = venv_python
    else:
        python_exe = sys.executable

    # Start the API server using uvicorn module
    cmd = [python_exe, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    subprocess.Popen(cmd, cwd="backend")

def start_frontend_server():
    """Start a simple HTTP server for the frontend"""
    # Try to start the frontend using npm start for CRA (better dev experience)
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    if os.path.exists(frontend_dir):
        try:
            # Start 'npm start' in the frontend directory
            subprocess.Popen(["npm", "start"], cwd=frontend_dir)
            print("Frontend 'npm start' launched (create-react-app).")
            webbrowser.open("http://localhost:3000")
            print("Open http://localhost:3000 to use the Ratoncito Pérez app!")
            return
        except Exception:
            # Fallback to simple HTTP server
            os.chdir(frontend_dir)

    PORT = 3000
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Frontend static server running at http://localhost:{PORT}")
        print("API server should be running at http://localhost:8000")
        print("Press Ctrl+C to stop")

        # Auto-open browser
        webbrowser.open(f"http://localhost:{PORT}")

        httpd.serve_forever()

if __name__ == "__main__":
    print("🐭 Starting Ratoncito Pérez servers...")

    # Start API server in background
    print("Starting API server...")
    start_api_server()

    # Wait a moment for API to start
    time.sleep(3)

    # Start frontend server (blocking)
    print("Starting frontend server...")
    start_frontend_server()
