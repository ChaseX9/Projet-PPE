import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User, UserLessonProgress, Lesson, UserTrainingStats, Module
from src.utils.config import DATABASE_URL
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test_multi@capinvest.fr"
PASSWORD = "Admin123!"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def cleanup():
    session = Session()
    user = session.query(User).filter(User.email == EMAIL).first()
    if user:
        session.query(UserTrainingStats).filter(UserTrainingStats.user_id == user.id).delete()
        session.query(UserLessonProgress).filter(UserLessonProgress.user_id == user.id).delete()
        session.delete(user)
    session.commit()
    session.close()

def setup_user():
    from src.auth.auth import hash_password
    session = Session()
    new_user = User(
        email=EMAIL,
        full_name="Multi-Track Test",
        hashed_password=hash_password(PASSWORD),
        is_active=True,
        email_verified=True
    )
    session.add(new_user)
    session.flush()
    stats = UserTrainingStats(user_id=new_user.id, total_xp=0, completed_lessons_count=0, current_streak=0, longest_streak=0, last_activity_date=datetime.utcnow())
    session.add(stats)
    session.commit()
    session.close()

def verify_multi_track():
    print(f"--- Multi-Track logic Test for {EMAIL} ---")
    
    # login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Start Beginner Module 1
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    if resp.status_code != 200:
        print(f"Error fetching modules: {resp.status_code}")
        print(f"Response text: {resp.text}")
        return
    modules = resp.json()
    beginner_m1 = next(m for m in modules if m['level'] == 'beginner' and m['order'] == 1)
    
    print(f"\n[STEP 1] Starting Beginner Module 1 (ID: {beginner_m1['id']})...")
    # Access a lesson to lock it in
    resp = requests.get(f"{BASE_URL}/api/training/modules/{beginner_m1['id']}", headers=headers)
    lesson_id = resp.json()["lessons"][0]["id"]
    requests.get(f"{BASE_URL}/api/training/lessons/{lesson_id}", headers=headers)
    
    # 2. Start Intermediate Module 1
    intermediate_m1 = next(m for m in modules if m['level'] == 'intermediate')
    print(f"\n[STEP 2] Starting Intermediate Module 1 (ID: {intermediate_m1['id']})...")
    resp = requests.get(f"{BASE_URL}/api/training/modules/{intermediate_m1['id']}", headers=headers)
    lesson_id_int = resp.json()["lessons"][0]["id"]
    requests.get(f"{BASE_URL}/api/training/lessons/{lesson_id_int}", headers=headers)
    
    # 3. Check states
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules_after = resp.json()
    
    print("\n[STEP 3] Verifying States:")
    for m in modules_after:
        if m['level'] in ['beginner', 'intermediate'] and m['order'] <= 5: # Limit output
            status = "LOCKED" if m['is_locked'] else "UNLOCKED"
            print(f"- Module {m['id']} ({m['level']}, Order {m['order']}): {status} | Reason: {m['lock_reason']}")

if __name__ == "__main__":
    cleanup()
    setup_user()
    verify_multi_track()
