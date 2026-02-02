import requests
import os

class APIClient:
    BASE_URL = "http://127.0.0.1:8000/api"

    @staticmethod
    def upload_file(file_path):
        url = f"{APIClient.BASE_URL}/upload/"
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files)
                return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    @staticmethod
    def get_history():
        url = f"{APIClient.BASE_URL}/history/"
        try:
            response = requests.get(url)
            return response.json()
        except requests.RequestException as e:
            return [{"error": str(e)}]
