import requests
import sys
import time
import subprocess
import os
import signal

def test_backend():
    print("🚀 Starting backend server for testing...")
    # Start the backend server
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=os.path.join(os.getcwd(), "backend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        base_url = "http://localhost:8000/api"
        
        # Test 1: Health Check
        print("\nTesting /health endpoint...")
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed!")
                print(response.json())
            else:
                print(f"❌ Health check failed with status {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Health check failed with error: {e}")

        # Test 2: Models Endpoint
        print("\nTesting /models endpoint...")
        try:
            response = requests.get(f"{base_url}/models")
            if response.status_code == 200:
                print("✅ Models endpoint passed!")
                print(f"Available models: {len(response.json()['models'])}")
            else:
                print(f"❌ Models endpoint failed with status {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Models endpoint failed with error: {e}")
            
    finally:
        # Cleanup
        print("\n🛑 Stopping backend server...")
        process.terminate()
        try:
            outs, errs = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            outs, errs = process.communicate()
            
        if process.returncode != 0 and process.returncode != -15: # -15 is SIGTERM
            print("Server output:")
            print(outs)
            print("Server errors:")
            print(errs)

if __name__ == "__main__":
    test_backend()
