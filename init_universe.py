"""Initialize or update the investment universe data."""
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.data.data_loader import load_or_update_universe

if __name__ == "__main__":
    print("Updating investment universe (this may take a minute)...")
    try:
        df = load_or_update_universe(max_age_days=0) # Force update
        print(f"✓ Universe updated: {len(df)} assets processed.")
    except Exception as e:
        print(f"❌ Error updating universe: {e}")
