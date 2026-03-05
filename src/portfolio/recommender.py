"""Main orchestrator for generating portfolio recommendations."""
from typing import Dict, List, Optional
import pandas as pd

from ..profile.schemas import RefinedProfile, ExpertiseLevel, RiskProfile
from ..data.data_loader import load_or_update_universe
from .allocation import get_target_allocation
from .filters import filter_universe, select_top_assets, enforce_portfolio_diversification
from .optimizer import optimize_markowitz, optimize_black_litterman, get_historical_prices, get_portfolio_performance
from ..utils.config import (
    MIN_ASSETS, 
    MAX_ASSETS, 
    MAX_WEIGHT_PRUDENT,
    MAX_WEIGHT_EQUILIBRE,
    MAX_WEIGHT_DYNAMIQUE
)

def build_portfolio(profile: RefinedProfile, force_update_universe: bool = False, excluded_tickers: Optional[List[str]] = None) -> Dict:
    """
    Complete workflow to build a recommended portfolio.
    1. Load/Update universe
    2. Filter assets (with optional user exclusions)
    3. Determine allocation targets
    4. Optimize within categories
    5. Aggregate and final formatting
    """
    # 1. Data
    universe = load_or_update_universe(max_age_days=0 if force_update_universe else 7)
    
    # 2. Filtering (with exclusions)
    eligible_assets = filter_universe(universe, profile, excluded_tickers=excluded_tickers)
    
    # 3. Dynamic Max Weight determination based on Risk Profile
    # This allows for natural differentiation and avoids the equal-weight problem
    max_weight_map = {
        RiskProfile.PRUDENT: MAX_WEIGHT_PRUDENT,       # e.g., 0.50
        RiskProfile.EQUILIBRE: MAX_WEIGHT_EQUILIBRE,   # e.g., 0.35
        RiskProfile.DYNAMIQUE: MAX_WEIGHT_DYNAMIQUE    # e.g., 0.30
    }
    dynamic_max_weight = max_weight_map.get(profile.risk_profile, 0.35)
    
    # 4. Allocation
    target_alloc = get_target_allocation(profile.risk_profile)
    
    # 4. Asset Selection & Optimization
    final_weights = {}
    processed_views = {}
    from collections import Counter
    method_counts = Counter()
    
    for category, cat_weight in target_alloc.items():
        if cat_weight <= 0:
            continue
            
        # Select best assets for this category (with sector diversification)
        cat_assets = select_top_assets(eligible_assets, category, profile=profile)
        tickers = cat_assets['ticker'].tolist()
        
        if not tickers:
            continue
            
        # Optimization method depends on expertise and preference (MiFID II constraint)
        use_bl = (
            profile.expertise_level == ExpertiseLevel.EXPERT and 
            profile.raw_profile.raw_responses.use_black_litterman
        )
        
        if use_bl:
            # Pass all qualitative views; optimizer filters by ticker
            qual_views = profile.raw_profile.raw_responses.market_views
            weights, shifts = optimize_black_litterman(tickers, qual_views)
            
            # Aggregate shifts for transparency
            for t, s in shifts.items():
                processed_views[t] = s
            
            # Record what kind of BL was used for this category
            if qual_views and any(v.get('ticker') in tickers for v in qual_views):
                 method_counts["Black-Litterman (with views)"] += 1
            else:
                 method_counts["Black-Litterman (neutral)"] += 1
        else:
            weights = optimize_markowitz(tickers, max_weight=dynamic_max_weight)
            method_counts["Markowitz"] += 1
            
        # Re-scale weights by category target
        for t, w in weights.items():
            final_weights[t] = w * cat_weight
            
    print(f"DEBUG: Positions before simplification: {len(final_weights)}")
            
    # 5. Portfolio Simplification Layer (Product Constraints)
    final_weights = simplify_portfolio(final_weights, profile)
    
    print(f"DEBUG: Positions after simplification: {len(final_weights)}")
            
    # 6. Performance calculation
    all_tickers = list(final_weights.keys())
    prices = get_historical_prices(all_tickers)
    ret, vol, sharpe = get_portfolio_performance(final_weights, prices)
    
    # 7. Format output
    positions = []
    for t, w in final_weights.items():
        # Dust filtering is now handled in simplify_portfolio,
        # but we keep a safety check here.
        if w < 0.0001:
            continue

        info = universe[universe['ticker'] == t].iloc[0]
        positions.append({
            "ticker": t,
            "weight": round(float(w), 4),
            "name": info['name'],
            "asset_type": info['asset_type'],
            "asset_class": info['asset_class'],
            "category": info['category'],
            "geography": info['geography'],
            "sector": info.get('sector', 'Autre'),
            "volatility": round(float(info['volatility']), 4),
            "reliability_score": round(float(info.get('reliability_score', 50.0)), 1),
            "sharpe_ratio": round(float(info.get('sharpe_ratio', 0.0)), 3),
        })

    # Post-optimization diversification check
    positions = enforce_portfolio_diversification(positions, eligible_assets, profile)
        
    # Final method determination
    # If all segments used BL with views, or at least one did, we customize the label
    if method_counts["Black-Litterman (with views)"] > 0:
        final_method = "Black-Litterman (with views)"
    elif method_counts["Black-Litterman (neutral)"] > 0:
        final_method = "Black-Litterman (neutral)"
    else:
        final_method = "Markowitz"

    return {
        "positions": positions,
        "category_allocations": target_alloc,
        "expected_return": round(ret, 4),
        "volatility": round(vol, 4),
        "sharpe_ratio": round(sharpe, 4),
        "optimization_method": final_method,
        "processed_views": processed_views,
        "total_positions": len(positions)
    }

def simplify_portfolio(weights: Dict[str, float], profile: RefinedProfile) -> Dict[str, float]:
    """
    Apply Phase 5 simplification rules:
    1. Use a global flexible range (min 2, max 10).
    2. Adapt limit based on investment amount (fewer assets for small amounts).
    3. Renormalize remaining weights (no artificial equal-weight).
    """
    # 1. Determine limit based on investment amount and risk profile
    from ..profile.profile_engine import normalize_investment_amount
    from ..profile.schemas import InvestmentAmount
    
    amount = profile.raw_profile.raw_responses.investment_amount
    normalized_amount = normalize_investment_amount(amount)
    
    # Small amount check (Under 500€) -> limit to fewer assets
    if normalized_amount in [InvestmentAmount.UNDER_100, InvestmentAmount.FROM_100_TO_500]:
        limit = 4 # Simple portfolio for small amounts
    else:
        limit = MAX_ASSETS # Default max
        
    amount_str = amount if isinstance(amount, (int, float, str)) else amount.value
    print(f"DEBUG: Simplifying for amount {amount_str} (Limit: {limit})")
    
    # 2. NO fixed dust filtering (per user request)
    # We keep only significant positions but without a hard threshold that forces equal weight
    simplified = {t: w for t, w in weights.items() if w > 0.001}
    
    # 3. If still too many, keep only the top ones
    if len(simplified) > limit:
        sorted_assets = sorted(simplified.items(), key=lambda x: x[1], reverse=True)
        simplified = dict(sorted_assets[:limit])
        
    # 4. Fallback
    if not simplified and weights:
        sorted_assets = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        simplified = dict(sorted_assets[:limit])

    # 5. Renormalize to ensure sum == 1.0 (100%)
    total_w = sum(simplified.values())
    if total_w > 0:
        simplified = {t: w / total_w for t, w in simplified.items()}
        
    return simplified
