"""Portfolio optimization engines (Markowitz & Black-Litterman)."""
import pandas as pd
import numpy as np
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns, black_litterman, BlackLittermanModel
from typing import Dict, List, Optional, Tuple

from ..utils.config import MAX_WEIGHT_PER_ASSET, RISK_FREE_RATE, BL_TAU, BL_RISK_AVERSION

def get_historical_prices(tickers: List[str], period: str = "3y") -> pd.DataFrame:
    """Fetch historical prices for optimization."""
    data = yf.download(tickers, period=period, progress=False)
    return data['Close']

def optimize_markowitz(
    tickers: List[str], 
    target_returns: Optional[float] = None,
    max_weight: float = 0.15
) -> Dict[str, float]:
    """Standard Markowitz Mean-Variance Optimization."""
    prices = get_historical_prices(tickers)
    if prices.empty:
        return {t: 1.0/len(tickers) for t in tickers}
        
    mu = expected_returns.capm_return(prices)
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    
    ef = EfficientFrontier(mu, S)
    ef.add_constraint(lambda w: w <= max_weight)
    
    try:
        # Maximize Sharpe ratio
        ef.max_sharpe(risk_free_rate=RISK_FREE_RATE)
    except:
        # Fallback to min volatility if max_sharpe fails
        ef = EfficientFrontier(mu, S)
        ef.add_constraint(lambda w: w <= max_weight)
        ef.min_volatility()
        
    weights = ef.clean_weights()
    
    return dict(weights)

def optimize_black_litterman(
    tickers: List[str], 
    qualitative_views: Optional[List[Dict]] = None,
    max_weight: float = 0.15
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Black-Litterman Optimization incorporating qualitative investor views.
    Returns (weights, effective_return_shifts).
    """
    prices = get_historical_prices(tickers)
    if prices.empty:
        return {t: 1.0/len(tickers) for t in tickers}, {}
        
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    
    # Equilibrium market returns (Priors)
    # In a real system, we'd use market caps. Here we assume equal starting weights for simplicity
    mcaps = {t: 1.0 for t in tickers} 
    delta = BL_RISK_AVERSION
    prior = black_litterman.market_implied_prior_returns(mcaps, delta, S)
    
    # Process qualitative views
    # View mapping: bullish (+5%), neutral (0%), bearish (-5%)
    # Confidence scaling: low (0.2), medium (0.5), high (1.0)
    views = {}
    confidences = {}
    return_shifts = {}
    
    mapping = {"bullish": 0.05, "neutral": 0.0, "bearish": -0.05}
    conf_mapping = {"low": 0.2, "medium": 0.5, "high": 1.0}
    
    if qualitative_views:
        for v in qualitative_views:
            ticker = v.get('ticker')
            if ticker in tickers:
                direction = v.get('direction', 'neutral')
                confidence_str = v.get('confidence', 'medium')
                
                # Numeric return shift
                shift = mapping.get(direction, 0.0)
                # Absolute view = prior + shift
                views[ticker] = prior[ticker] + shift
                # Confidence scaling
                confidences[ticker] = conf_mapping.get(confidence_str, 0.5)
                # Log the shift for transparency
                return_shifts[ticker] = shift

    # If no valid views remain after filtering, run neutral BL
    if not views:
        ret_bl = prior
        S_bl = S
    else:
        bl = BlackLittermanModel(
            S, 
            pi=prior, 
            absolute_views=views, 
            omega=None, # Automatically calculate based on confidences
            view_confidences=list(confidences.values()),
            tau=BL_TAU
        )
        ret_bl = bl.bl_returns()
        S_bl = bl.bl_cov()
    
    # Portfolio construction based on BL returns
    ef = EfficientFrontier(ret_bl, S_bl)
    ef.add_constraint(lambda w: w <= max_weight)
    
    try:
        ef.max_sharpe(risk_free_rate=RISK_FREE_RATE)
    except:
        # Fallback to min volatility if max_sharpe fails
        ef = EfficientFrontier(ret_bl, S_bl)
        ef.add_constraint(lambda w: w <= max_weight)
        ef.min_volatility()
    
    return dict(ef.clean_weights()), return_shifts

def get_portfolio_performance(weights: Dict[str, float], prices: pd.DataFrame) -> Tuple[float, float, float]:
    """Calculate expected return, volatility and Sharpe ratio."""
    mu = expected_returns.capm_return(prices)
    S = risk_models.CovarianceShrinkage(prices).ledoit_wolf()
    
    w_list = np.array([weights[t] for t in prices.columns])
    
    ret = np.dot(w_list, mu)
    vol = np.sqrt(np.dot(w_list.T, np.dot(S, w_list)))
    sharpe = (ret - RISK_FREE_RATE) / vol
    
    return float(ret), float(vol), float(sharpe)
