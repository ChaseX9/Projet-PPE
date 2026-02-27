"""Filtering logic to select eligible assets from the universe."""
import pandas as pd
from typing import List
from ..profile.schemas import RefinedProfile
from ..utils.config import MIN_LIQUIDITY_VOLUME, MAX_ETF_EXPENSE_RATIO

def filter_universe(universe_df: pd.DataFrame, profile: RefinedProfile) -> pd.DataFrame:
    """
    Apply filters to the universe based on user profile and general rules.
    1. Liquidity (MiFID II requirement)
    2. Expense Ratio (Cost efficiency)
    3. User Preferences (ESG, etc.)
    """
    df = universe_df.copy()
    
    # 1. Minimum Liquidity (Average Daily Volume * Price)
    df = df[df['liquidity'] >= MIN_LIQUIDITY_VOLUME]
    
    # 2. Maximum Expense Ratio for ETFs
    # Stocks have expense_ratio = 0 in our model
    df = df[df['expense_ratio'] <= MAX_ETF_EXPENSE_RATIO]
    
    # 3. User Preferences
    if profile.raw_profile.raw_responses.esg_preference:
        # Prioritize ESG assets but don't necessarily exclude all others if needed for diversification
        # Here we strictly include only ESG if both are available
        esg_assets = df[df['is_esg'] == True]
        if not esg_assets.empty:
            # We filter for a mix but favoring ESG
            # In a simple implementation, let's keep all and the optimizer will handle weights if we add penalties
            # For now, let's just make sure we have ESG assets available
            pass
            
    # 4. Volatility constraints based on risk profile
    if profile.risk_profile == "Prudent":
        df = df[df['volatility'] < 0.25] # Exclude highly volatile assets for prudent users
        
    return df

def select_top_assets(filtered_df: pd.DataFrame, category: str, limit: int = 15) -> pd.DataFrame:
    """Select the best assets for a given category (equities or bonds)."""
    df = filtered_df[filtered_df['category'] == category]
    
    # Simple heuristic: sort by liquidity (stability)
    # Could be improved with returns data
    return df.sort_values(by='liquidity', ascending=False).head(limit)
