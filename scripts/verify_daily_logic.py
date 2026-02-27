from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User, UserTrainingStats, Module, Lesson, UserLessonProgress
from src.utils.config import DATABASE_URL
from datetime import datetime, timedelta

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def verify_logic():
    session = Session()
    # Find a user
    user = session.query(User).first()
    if not user:
        print("No user found.")
        return

    # Check stats for this user
    stats = session.query(UserTrainingStats).filter(UserTrainingStats.user_id == user.id).first()
    if not stats:
        print("No stats found for user.")
        return

    print(f"User: {user.email}")
    print(f"Current Day Module ID: {stats.current_day_module_id}")
    print(f"Last Activity Date: {stats.last_activity_date}")
    
    # Simulate a module start?
    # Actually, let's just check if our new lessons are there.
    m7 = session.query(Module).filter(Module.order == 7).first()
    lessons = session.query(Lesson).filter(Lesson.module_id == m7.id).all()
    print(f"Module 7 lessons count: {len(lessons)}")
    for l in lessons:
        print(f" - Lesson {l.order}: {l.title}")

    session.close()

if __name__ == "__main__":
    verify_logic()
