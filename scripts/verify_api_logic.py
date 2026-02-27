import requests
import json

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test@capinvest.fr"
PASSWORD = "Admin123!"

def verify_api_logic():
    print(f"--- Testing logic for {EMAIL} ---")
    
    # 1. Login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Check initial modules (Sequential Locking)
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules = resp.json()
    print("\nInitial State (Sequential Locking):")
    for m in modules[:3]:
        print(f"Module {m['order']} ({m['title']}): is_locked={m['is_locked']}, reason={m['lock_reason']}")
    
    # 3. Simulate starting a lesson in Module 1
    # First, get Module 1 lessons
    m1_id = modules[0]["id"]
    resp = requests.get(f"{BASE_URL}/api/training/modules/{m1_id}", headers=headers)
    lessons = resp.json()["lessons"]
    l1_id = lessons[0]["id"]
    
    print(f"\nAccessing Lesson 1 (ID: {l1_id}) to lock in the day...")
    resp = requests.get(f"{BASE_URL}/api/training/lessons/{l1_id}", headers=headers)
    
    # 4. Check modules again (Daily Locking)
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules = resp.json()
    print("\nState after starting Lesson 1 (Daily Locking):")
    for m in modules[:3]:
        print(f"Module {m['order']} ({m['title']}): is_locked={m['is_locked']}, reason={m['lock_reason']}")

if __name__ == "__main__":
    verify_api_logic()
