"""Initialize the database tables."""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.database.database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("✓ Database initialized successfully.")
