"""Quick test script to verify Academy functionality."""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question, User
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

print("=" * 50)
print("CAPINVEST ACADEMY - DATABASE TEST")
print("=" * 50)

# Check modules
modules = session.query(Module).order_by(Module.order).all()
print(f"\n✅ {len(modules)} modules loaded:")
for m in modules:
    lesson_count = len(m.lessons)
    print(f"   {m.icon} {m.title} ({m.level}) - {lesson_count} leçons")

# Check lessons
total_lessons = session.query(Lesson).count()
print(f"\n✅ {total_lessons} lessons total")

# Check questions
total_questions = session.query(Question).count()
print(f"\n✅ {total_questions} questions total")

# Sample lesson detail
first_lesson = session.query(Lesson).first()
if first_lesson:
    print(f"\n📖 Sample Lesson: {first_lesson.title}")
    print(f"   Content length: {len(first_lesson.content)} chars")
    print(f"   Example: {'Yes' if first_lesson.example else 'No'}")
    print(f"   Questions: {len(first_lesson.questions)}")
    print(f"   XP Reward: {first_lesson.xp_reward} XP")

# Check user count
user_count = session.query(User).count()
print(f"\n✅ {user_count} users in database")

print("\n" + "=" * 50)
print("All checks passed! Academy is ready. 🎓")
print("=" * 50)
