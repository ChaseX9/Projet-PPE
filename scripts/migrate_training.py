from sqlalchemy import create_engine, text
from src.utils.config import DATABASE_URL

def migrate():
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE user_training_stats ADD COLUMN current_day_module_id INTEGER REFERENCES modules(id)"))
            conn.commit()
            print("Successfully added current_day_module_id column.")
        except Exception as e:
            print(f"Error or already exists: {e}")

if __name__ == "__main__":
    migrate()
