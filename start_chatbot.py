#!/usr/bin/env python3
"""
ABS Chatbot Startup Script
Starts both the FastAPI backend and Streamlit frontend
"""

import subprocess
import time
import sys
import requests
import os
import signal
from threading import Thread

def check_api_health(max_retries=10, delay=2):
    """Check if API is responding"""
    for attempt in range(max_retries):
        try:
            response = requests.get("http://localhost:8001/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy and ready!")
                return True
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                print(f"⏳ Waiting for API... (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            else:
                print("❌ API failed to start properly")
                return False
    return False

def start_api_server():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        # Start the API server
        api_process = subprocess.Popen([
            sys.executable, "backend_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if api_process.poll() is None:
            print("✅ API server started successfully on http://localhost:8001")
            return api_process
        else:
            print("❌ Failed to start API server")
            stdout, stderr = api_process.communicate()
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def start_streamlit_app():
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    try:
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "chatbot_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        
        print("✅ Streamlit app started successfully on http://localhost:8501")
        return streamlit_process
        
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        return None

def cleanup_processes(api_process, streamlit_process):
    """Clean up running processes"""
    print("\n🛑 Shutting down services...")
    
    if streamlit_process and streamlit_process.poll() is None:
        print("Stopping Streamlit...")
        streamlit_process.terminate()
        try:
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            streamlit_process.kill()
    
    if api_process and api_process.poll() is None:
        print("Stopping API server...")
        api_process.terminate()
        try:
            api_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
    
    print("✅ All services stopped")

def check_requirements():
    """Check if required files exist"""
    required_files = ["backend_api.py", "chatbot_app.py", "requirements.txt"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found. Make sure to set GOOGLE_API_KEY")
    
    return True

def main():
    """Main function to orchestrate the startup"""
    print("🤖 ABS Chatbot Startup Script")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please ensure all required files are present")
        return 1
    
    # Check if ports are available
    try:
        import socket
        
        # Check API port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8001))
        sock.close()
        
        if result == 0:
            print("❌ Port 8001 is already in use. Please stop any existing API server.")
            return 1
            
    except Exception as e:
        print(f"⚠️  Could not check port availability: {e}")
    
    api_process = None
    streamlit_process = None
    
    try:
        # Start API server
        api_process = start_api_server()
        if not api_process:
            return 1
        
        # Wait for API to be ready
        if not check_api_health():
            print("❌ API server is not responding properly")
            cleanup_processes(api_process, None)
            return 1
        
        # Start Streamlit app
        streamlit_process = start_streamlit_app()
        if not streamlit_process:
            cleanup_processes(api_process, None)
            return 1
        
        print("\n" + "=" * 50)
        print("🎉 ABS Chatbot is now running!")
        print("📱 Frontend: http://localhost:8501")
        print("🔧 API: http://localhost:8001")
        print("📖 API Docs: http://localhost:8001/docs")
        print("=" * 50)
        print("\n💡 Tips:")
        print("   • Make sure you've processed documents using main.py first")
        print("   • Check the sidebar for connection status")
        print("   • Use Ctrl+C to stop all services")
        print("\nPress Ctrl+C to stop all services...")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if api_process.poll() is not None:
                    print("❌ API server stopped unexpectedly")
                    break
                    
                if streamlit_process.poll() is not None:
                    print("❌ Streamlit app stopped unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Received shutdown signal...")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        cleanup_processes(api_process, streamlit_process)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)