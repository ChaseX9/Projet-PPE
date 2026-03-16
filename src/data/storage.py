"""Storage utilities for investment universe (CSV processing)."""
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import os

def save_universe_to_csv(df: pd.DataFrame, file_path: Path):
    """
    Save the universe DataFrame to CSV.
    
    Args:
        df: DataFrame containing the universe
        file_path: Path to the CSV file
    """
    if df is None or df.empty:
        print(f"⚠️  Not saving empty DataFrame to {file_path}. Preserving existing file.")
        return

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(file_path, index=False)
    
    # Save a hidden metadata file for timestamp
    meta_path = file_path.with_suffix('.meta')
    with open(meta_path, 'w') as f:
        f.write(datetime.now().isoformat())

def load_universe_from_csv(file_path: Path) -> pd.DataFrame:
    """
    Load the universe DataFrame from CSV. Handles EmptyDataError.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame or None if file doesn't exist or is empty
    """
    if not file_path.exists():
        return None
    
    try:
        # Check file size first
        if os.path.getsize(file_path) == 0:
            print(f"⚠️  File {file_path} is empty.")
            return None
            
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def get_universe_age(file_path: Path) -> Optional[int]:
    """
    Get the age of the universe file in days.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Age in days or None if file doesn't exist
    """
    meta_path = file_path.with_suffix('.meta')
    if not meta_path.exists():
        if not file_path.exists():
            return None
        # Fallback to file mtime if meta missing
        mtime = os.path.getmtime(file_path)
        last_updated = datetime.fromtimestamp(mtime)
    else:
        with open(meta_path, 'r') as f:
            last_updated = datetime.fromisoformat(f.read())
            
    age = (datetime.now() - last_updated).days
    return age
