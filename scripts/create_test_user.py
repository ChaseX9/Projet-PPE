from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User, UserTrainingStats, UserLessonProgress
from src.auth.auth import hash_password
from src.utils.config import DATABASE_URL
from datetime import datetime

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_test_user():
    session = Session()
    email = "test@capinvest.fr"
    
    # Remove existing test user
    user = session.query(User).filter(User.email == email).first()
    if user:
        session.query(UserTrainingStats).filter(UserTrainingStats.user_id == user.id).delete()
        session.query(UserLessonProgress).filter(UserLessonProgress.user_id == user.id).delete()
        session.delete(user)
        session.commit()
        print(f"Deleted existing test user {email}")

    # Create new user
    new_user = User(
        email=email,
        full_name="Compte Test",
        hashed_password=hash_password("Admin123!"),
        is_active=True,
        email_verified=True
    )
    session.add(new_user)
    session.flush()

    # Create stats
    stats = UserTrainingStats(
        user_id=new_user.id,
        total_xp=0,
        completed_lessons_count=0,
        current_streak=0,
        longest_streak=0,
        last_activity_date=datetime.utcnow()
    )
    session.add(stats)
    session.commit()
    print(f"✅ Test user {email} created successfully.")
    session.close()

if __name__ == "__main__":
    create_test_user()
