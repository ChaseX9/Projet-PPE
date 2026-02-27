import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from src.database.database import SessionLocal
from src.database.models import User, UserTrainingStats
from src.api.training_endpoints import get_modules, get_progress
from src.auth.auth import hash_password

def test_new_user():
    db = SessionLocal()
    email = f"new_tester_{datetime.now().timestamp()}@test.com"
    try:
        print(f"--- Testing for BRAND NEW user: {email} ---")
        new_user = User(
            email=email,
            full_name="New Tester",
            hashed_password=hash_password("Admin123!"),
            is_active=True,
            email_verified=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Test get_modules with NO STATS
        print("\n[TEST] get_modules (stats=None)")
        try:
            modules = get_modules(current_user=new_user, db=db)
            print(f"Successfully fetched {len(modules)} modules.")
        except Exception as e:
            print(f"FAILED get_modules: {e}")
            import traceback
            traceback.print_exc()

        # Test get_progress with NO STATS
        print("\n[TEST] get_progress (stats=None)")
        try:
            progress = get_progress(current_user=new_user, db=db)
            print("Successfully fetched progress.")
        except Exception as e:
            print(f"FAILED get_progress: {e}")
            import traceback
            traceback.print_exc()
            
    finally:
        db.query(User).filter(User.email == email).delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    test_new_user()
