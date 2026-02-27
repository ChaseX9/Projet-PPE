import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User, UserLessonProgress, Lesson, UserTrainingStats, Module
from src.utils.config import DATABASE_URL
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test_logic@capinvest.fr"
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
        full_name="Logic Test",
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

def verify_logic():
    print(f"--- Comprehensive Logic Test for {EMAIL} ---")
    
    # login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Sequential Proof
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules = resp.json()
    print("\n[STEP 1] Initial (Sequential) State:")
    for m in modules[:2]:
        print(f"Module {m['order']}: is_locked={m['is_locked']}, reason={m['lock_reason']}")

    # 2. Unlock Module 2 by finishing Module 1
    session = Session()
    user = session.query(User).filter(User.email == EMAIL).first()
    m1 = session.query(Module).filter(Module.order == 1).first()
    for lesson in m1.lessons:
        progress = UserLessonProgress(user_id=user.id, lesson_id=lesson.id, status="completed", score=100)
        session.add(progress)
    session.commit()
    session.close()
    
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules = resp.json()
    print("\n[STEP 2] After finishing Module 1:")
    for m in modules[:2]:
        print(f"Module {m['order']}: is_locked={m['is_locked']}, reason={m['lock_reason']}")

    # 3. Daily Lock Proof: Start Module 2
    m2_id = modules[1]["id"]
    resp = requests.get(f"{BASE_URL}/api/training/modules/{m2_id}", headers=headers)
    l_m2_id = resp.json()["lessons"][0]["id"]
    
    print(f"\n[STEP 3] Starting Module 2 (Lesson ID: {l_m2_id})...")
    requests.get(f"{BASE_URL}/api/training/lessons/{l_m2_id}", headers=headers)
    
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules = resp.json()
    print("\n[STEP 4] State after starting Module 2 (Daily Lock Check):")
    for m in [modules[1], modules[2]]: # Module 2 and Module 3
        print(f"Module {m['order']}: is_locked={m['is_locked']}, reason={m['lock_reason']}")

if __name__ == "__main__":
    cleanup()
    setup_user()
    verify_logic()
