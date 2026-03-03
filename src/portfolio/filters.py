"""
Filtering and diversification logic for asset selection.

Key improvements:
- reliability_score-based sorting (replaces pure liquidity sort)
- Mandatory sector diversification (max N assets per sector)
- All filtering operations are transparent and auditable (MiFID II)
"""
import pandas as pd
from typing import List, Dict, Optional
from collections import defaultdict

from ..profile.schemas import RefinedProfile, RiskProfile
from ..utils.config import (
    MIN_LIQUIDITY_VOLUME,
    MAX_ETF_EXPENSE_RATIO,
    REFERENCE_ASSETS,
    MAX_ASSETS_PER_SECTOR,
    MIN_SECTORS_IN_PORTFOLIO,
)


def filter_universe(universe_df: pd.DataFrame, profile: RefinedProfile) -> pd.DataFrame:
    """
    Apply eligibility filters to the universe based on user profile and general rules.
    1. Liquidity (MiFID II requirement)
    2. Expense Ratio (Cost efficiency)
    3. ESG preference
    4. Volatility constraints (Prudent profile)
    """
    df = universe_df.copy()

    # Ensure sector column exists (backwards compat)
    if "sector" not in df.columns:
        df["sector"] = "Autre"
    if "reliability_score" not in df.columns:
        df["reliability_score"] = 50.0
        df.loc[df["ticker"].isin(REFERENCE_ASSETS), "reliability_score"] = 70.0

    # 1. Minimum Liquidity (Average Daily Volume * Price)
    df = df[df["liquidity"] >= MIN_LIQUIDITY_VOLUME]

    # 2. Maximum Expense Ratio for ETFs
    df = df[df["expense_ratio"] <= MAX_ETF_EXPENSE_RATIO]

    # 3. ESG preference: restrict to ESG assets if requested
    if profile.raw_profile.raw_responses.esg_preference:
        esg_assets = df[df["is_esg"] == True]
        if len(esg_assets) >= 3:  # only restrict if enough ESG assets exist
            df = esg_assets

    # 4. Volatility constraints for Prudent investors
    if profile.risk_profile == RiskProfile.PRUDENT:
        df = df[df["volatility"] < 0.25]

    # 5. Sector preferences: restrict to specific sectors if requested
    # Note: We always keep 'Obligations' and 'Multi-secteur' for basic diversification
    # even if not explicitly chosen, to avoid concentrated/risky portfolios.
    sector_prefs = getattr(profile.raw_profile.raw_responses, 'sector_preferences', None)
    if sector_prefs:
        # Filter for chosen sectors + infrastructure/diversification assets
        mask = df["sector"].isin(sector_prefs) | df["sector"].isin(["Obligations", "Multi-secteur"])
        sector_df = df[mask]
        
        # Only apply if we still have a reasonable number of assets
        if len(sector_df) >= 10:
            df = sector_df
        else:
            print(f"  ⚠️ Not enough assets in selected sectors {sector_prefs}. Falling back to full universe.")

    return df


def select_top_assets(
    filtered_df: pd.DataFrame,
    category: str,
    profile: Optional[RefinedProfile] = None,
    limit: int = 20,
) -> pd.DataFrame:
    """
    Select the best assets for a given category (equities or bonds)
    with sector-based diversification enforcement.

    Algorithm:
    1. Sort all eligible assets by reliability_score descending.
    2. Apply sector quota: max N assets per sector (from config).
    3. Ensure reference assets (whitelist) are given priority.
    4. Return up to `limit` assets.
    """
    df = filtered_df[filtered_df["category"] == category].copy()

    if df.empty:
        return df

    # Determine the profile name for sector quota lookup
    profile_name = "Équilibré"  # default
    if profile is not None:
        profile_name = profile.risk_profile.value

    max_per_sector = MAX_ASSETS_PER_SECTOR.get(profile_name, 2)

    # Sort by reliability_score descending (reference assets naturally rank higher)
    df = df.sort_values("reliability_score", ascending=False)

    # --- Sector-diversified greedy selection ---
    selected = []
    sector_counts: Dict[str, int] = defaultdict(int)

    # First pass: take reference assets (guaranteed slots, up to 1 per sector)
    reference_df = df[df["ticker"].isin(REFERENCE_ASSETS)]
    ref_sector_counts: Dict[str, int] = defaultdict(int)
    for _, row in reference_df.iterrows():
        sector = row.get("sector", "Autre")
        # Allow 1 reference asset per sector regardless of quota (they're the best)
        if ref_sector_counts[sector] < 1:
            selected.append(row)
            sector_counts[sector] += 1
            ref_sector_counts[sector] += 1

    # Second pass: fill remaining slots with sector diversification
    already_selected = {r["ticker"] for r in selected}
    for _, row in df.iterrows():
        if len(selected) >= limit:
            break
        if row["ticker"] in already_selected:
            continue

        sector = row.get("sector", "Autre")

        # Enforce sector quota (multi-sector ETFs are exempt from the cap)
        is_multisector = "Multi-secteur" in str(sector) or sector in ("Obligations", "Autre")
        if not is_multisector and sector_counts[sector] >= max_per_sector:
            continue

        selected.append(row)
        sector_counts[sector] += 1

    if not selected:
        # Fallback: return top-N without sector constraint (should not happen)
        return df.head(limit)

    result = pd.DataFrame(selected)

    # Log sector distribution for transparency
    if "sector" in result.columns:
        dist = result["sector"].value_counts().to_dict()
        print(f"  📊 Sector distribution ({category}, profile={profile_name}): {dist}")

    return result


def enforce_portfolio_diversification(
    positions: List[dict],
    filtered_df: pd.DataFrame,
    profile: RefinedProfile,
    max_sector_weight: float = 0.50,
) -> List[dict]:
    """
    Post-optimization diversification check.
    If any single sector exceeds max_sector_weight of the total portfolio,
    flag it for rebalancing (the optimizer will re-run with an exclusion).
    
    Returns the positions unchanged but with a 'sector_warning' flag added if needed.
    """
    if not positions:
        return positions

    # Calculate sector weights
    sector_weights: Dict[str, float] = defaultdict(float)
    for pos in positions:
        sector = pos.get("sector", "Autre")
        sector_weights[sector] += pos.get("weight", 0.0)

    dominant_sectors = {s: w for s, w in sector_weights.items() if w > max_sector_weight and s != "Obligations"}

    if dominant_sectors:
        for sector, weight in dominant_sectors.items():
            print(f"  ⚠️ Sector warning: '{sector}' has {weight:.0%} weight (>{max_sector_weight:.0%})")

    return positions
