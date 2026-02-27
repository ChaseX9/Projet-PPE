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

def debug_endpoints():
    db = SessionLocal()
    try:
        # Get a test user (the one created by subagent)
        user = db.query(User).filter(User.email == "test_prog_999@test.com").first()
        if not user:
            print("User test_prog_999@test.com not found. Trying maelvaudin@gmail.com")
            user = db.query(User).filter(User.email == "maelvaudin@gmail.com").first()
        
        if not user:
            print("No suitable user found.")
            return

        print(f"--- Debugging endpoints for user: {user.email} ---")
        
        # Test get_modules
        print("\n[TEST] get_modules")
        try:
            modules = get_modules(current_user=user, db=db)
            print(f"Successfully fetched {len(modules)} modules.")
        except Exception as e:
            print(f"FAILED get_modules: {e}")
            import traceback
            traceback.print_exc()

        # Test get_progress
        print("\n[TEST] get_progress")
        try:
            progress = get_progress(current_user=user, db=db)
            print("Successfully fetched progress.")
            print(f"Daily modules: {progress.daily_modules}")
        except Exception as e:
            print(f"FAILED get_progress: {e}")
            import traceback
            traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    debug_endpoints()
