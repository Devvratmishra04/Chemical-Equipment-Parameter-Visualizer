import requests
import os

BASE_URL = "http://127.0.0.1:8000/api"
FILE_PATH = "sample_equipment_data.csv"

def test_upload():
    print("Testing File Upload...")
    if not os.path.exists(FILE_PATH):
        print(f"File {FILE_PATH} not found.")
        return

    with open(FILE_PATH, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/upload/", files=files)
        
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_history():
    print("\nTesting History...")
    response = requests.get(f"{BASE_URL}/history/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_upload()
    test_history()
