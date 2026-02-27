"""Migration script to add GDPR compliance fields to existing users."""
from sqlalchemy import create_engine, text
from pathlib import Path

# Path to database
DB_PATH = Path(__file__).parent.parent.parent / "data" / "robo_advisor.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

def migrate():
    """Add GDPR fields to users table."""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if columns already exist
        result = conn.execute(text("PRAGMA table_info(users)"))
        existing_columns = {row[1] for row in result}
        
        # Add new columns if they don't exist
        if 'privacy_policy_accepted_at' not in existing_columns:
            print("Adding privacy_policy_accepted_at column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN privacy_policy_accepted_at DATETIME"))
            conn.commit()
        
        if 'cookies_consent' not in existing_columns:
            print("Adding cookies_consent column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN cookies_consent BOOLEAN DEFAULT 0"))
            conn.commit()
        
        if 'marketing_consent' not in existing_columns:
            print("Adding marketing_consent column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN marketing_consent BOOLEAN DEFAULT 0"))
            conn.commit()
        
        if 'data_retention_notified' not in existing_columns:
            print("Adding data_retention_notified column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN data_retention_notified DATETIME"))
            conn.commit()
        
        print("✅ GDPR migration completed successfully!")

if __name__ == "__main__":
    migrate()
