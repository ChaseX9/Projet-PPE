import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User, UserLessonProgress, Lesson, UserTrainingStats, Module
from src.utils.config import DATABASE_URL
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test_daily@capinvest.fr"
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
        full_name="Daily Test",
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
    print(f"--- Daily Completion Test for {EMAIL} ---")
    
    # login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": PASSWORD})
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Start and Finish Module 1
    session = Session()
    user = session.query(User).filter(User.email == EMAIL).first()
    stats = session.query(UserTrainingStats).filter(UserTrainingStats.user_id == user.id).first()
    m1 = session.query(Module).filter(Module.order == 1).first()
    
    # Lock in Module 1 as the day's choice
    stats.current_day_module_id = m1.id
    stats.last_activity_date = datetime.utcnow()
    
    for lesson in m1.lessons:
        progress = UserLessonProgress(user_id=user.id, lesson_id=lesson.id, status="completed", score=100)
        session.add(progress)
    session.commit()
    session.close()
    
    print("\n[STEP 1] Finished Module 1 (The day's module).")
    
    # 2. Check Module 2 status
    resp = requests.get(f"{BASE_URL}/api/training/modules", headers=headers)
    modules = resp.json()
    m2 = modules[1]
    print(f"\n[STEP 2] Module 2 ({m2['title']}) status:")
    print(f"is_locked={m2['is_locked']}, reason={m2['lock_reason']}")

    # 3. Try to access a lesson in Module 2
    m2_id = m2["id"]
    resp = requests.get(f"{BASE_URL}/api/training/modules/{m2_id}", headers=headers)
    l_m2_id = resp.json()["lessons"][0]["id"]
    
    print(f"\n[STEP 3] Trying to access Lesson {l_m2_id} in Module 2...")
    resp = requests.get(f"{BASE_URL}/api/training/lessons/{l_m2_id}", headers=headers)
    print(f"Status Code: {resp.status_code}")
    print(f"Error Detail: {resp.json().get('detail') if resp.status_code != 200 else 'SUCCESS (Failure!)'}")

if __name__ == "__main__":
    cleanup()
    setup_user()
    verify_logic()
