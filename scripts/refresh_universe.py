#!/usr/bin/env python3
"""
Refresh the universe.csv file with all tickers from config.py
Run this from the project root: python scripts/refresh_universe.py
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.data_loader import load_or_update_universe
from src.data.storage import save_universe_to_csv
from src.data.data_loader import fetch_universe_batch, AssetType
from src.utils.config import DEFAULT_ETF_TICKERS, DEFAULT_STOCK_TICKERS

if __name__ == "__main__":
    print("🔄 Refreshing universe with expanded stock list...")
    print("This may take a few minutes to fetch data from Yahoo Finance...")
    
    try:
        # Force a full refresh by fetching all tickers fresh
        etf_df = fetch_universe_batch(DEFAULT_ETF_TICKERS, AssetType.ETF)
        stock_df = fetch_universe_batch(DEFAULT_STOCK_TICKERS, AssetType.STOCK)
        
        import pandas as pd
        full_df = pd.concat([etf_df, stock_df], ignore_index=True)
        
        universe_file = project_root / "data" / "universe.csv"
        save_universe_to_csv(full_df, universe_file)
        
        print("\n✅ Universe successfully updated!")
        print(f"📁 Check: {universe_file}")
        print(f"📊 Total assets in universe: {len(full_df)}")
        print(f"   - ETFs: {len(etf_df)}")
        print(f"   - Stocks: {len(stock_df)}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
