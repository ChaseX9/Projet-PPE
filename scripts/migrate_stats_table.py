from sqlalchemy import create_engine, text
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Migrating UserTrainingStats table...")
    # Drop old column if it exists
    try:
        conn.execute(text("ALTER TABLE user_training_stats DROP COLUMN current_day_module_id"))
        print("Dropped current_day_module_id column.")
    except Exception as e:
        print(f"Skipped dropping current_day_module_id: {e}")
    
    # Add new column if it doesn't exist
    try:
        conn.execute(text("ALTER TABLE user_training_stats ADD COLUMN daily_modules JSON DEFAULT '{}'"))
        print("Added daily_modules column.")
    except Exception as e:
        print(f"Skipped adding daily_modules: {e}")
    
    conn.commit()
    print("Migration complete.")
