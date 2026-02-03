
import requests
import sys
import random
import string

BASE_URL = "http://127.0.0.1:8000/api"

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_registration():
    print("\nTesting User Registration...")
    username = f"user_{get_random_string(5)}"
    password = "testpassword123"
    
    try:
        payload = {
            "username": username,
            "password": password
        }
        r = requests.post(f"{BASE_URL}/register/", data=payload)
        
        if r.status_code == 201:
            print(f"PASS: Registration successful for user '{username}'.")
            return username, password
        else:
            print(f"FAIL: Registration failed. Status: {r.status_code}")
            print(r.text)
            return None, None
    except Exception as e:
        print(f"ERROR: {e}")
        return None, None

def test_auth(username, password):
    print(f"\nTesting Authentication for '{username}'...")
    
    # Authenticated request (should succeed)
    try:
        r = requests.get(f"{BASE_URL}/history/", auth=(username, password))
        if r.status_code == 200:
            print("PASS: Authenticated access allowed.")
        else:
            print(f"FAIL: Authenticated access failed. Status: {r.status_code}")
            print(r.text)
    except Exception as e:
        print(f"ERROR: {e}")

def test_pdf():
    print("\nTesting PDF Generation (using admin)...")
    # Using admin for consistent data access if new user has no data
    try:
        r = requests.get(f"{BASE_URL}/history/", auth=('admin', 'adminpassword'))
        data = r.json()
        
        if not data:
            print("SKIP: No documents found to test PDF generation. Please upload a file first.")
            return

        doc_id = data[0]['id']
        print(f"Testing PDF for Document ID: {doc_id}")
        
        pdf_url = f"{BASE_URL}/history/{doc_id}/pdf/"
        r_pdf = requests.get(pdf_url, auth=('admin', 'adminpassword'))
        
        if r_pdf.status_code == 200:
            if r_pdf.headers.get('Content-Type') == 'application/pdf':
                if r_pdf.content.startswith(b'%PDF'):
                    print("PASS: PDF generated successfully.")
                else:
                    print("FAIL: Content does not look like a PDF.")
            else:
                 print(f"FAIL: unexpected Content-Type: {r_pdf.headers.get('Content-Type')}")
        else:
            print(f"FAIL: PDF generation failed. Status: {r_pdf.status_code}")
            print(r_pdf.text)

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    new_user, new_pass = test_registration()
    if new_user:
        test_auth(new_user, new_pass)
    
    test_pdf()
