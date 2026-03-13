#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

# Force a dummy DB URL if needed for imports to work without a real DB file
import os
if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = "sqlite:///data/robo_advisor.db"

from src.data.data_loader import load_or_update_universe
from src.api.endpoints import get_explorer_assets

async def main():
    print("🚀 Starting Automatic Data Update Cycle...")
    
    try:
        # Ensure data directory exists
        data_dir = root / "data"
        if not data_dir.exists():
            data_dir.mkdir(parents=True)
            print(f"Created data directory at {data_dir}")

        print("\n--- Phase 1: Refreshing Universe Data ---")
        # max_age_days=0 forces a fresh fetch from Yahoo Finance for all tickers
        universe = load_or_update_universe(max_age_days=0)
        print(f"✅ Universe refreshed: {len(universe)} assets processed.")
        
        print("\n--- Phase 2: Regenerating Explorer Cache ---")
        # force_refresh=True recalculates sparklines, pedagogy, etc. and saves to data/explorer_cache.json
        explorer_data = await get_explorer_assets(force_refresh=True)
        print(f"✅ Explorer cache updated: {len(explorer_data)} assets cached.")
        
        print("\n✨ Cycle completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during update cycle: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
