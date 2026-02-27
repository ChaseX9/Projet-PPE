"""Data loader for fetching and processing financial data from Yahoo Finance."""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
import time

from .universe import AssetType, AssetClass, AssetCategory, InvestmentAsset
from .storage import save_universe_to_csv, load_universe_from_csv, get_universe_age
from ..utils.config import (
    DEFAULT_ETF_TICKERS, 
    DEFAULT_STOCK_TICKERS, 
    UNIVERSE_FILE, 
    YAHOO_FINANCE_PERIOD,
    VOLATILITY_WINDOW_YEARS
)

def fetch_asset_info(ticker: str) -> Dict:
    """Fetch metadata for a single asset."""
    t = yf.Ticker(ticker)
    info = t.info
    
    quote_type = info.get('quoteType', '').upper()
    is_etf = quote_type == 'ETF'
    
    # Use dynamic classification
    asset_class, category, geography = classify_asset(ticker, info)
    
    asset_data = {
        "ticker": ticker,
        "name": info.get('shortName', info.get('longName', ticker)),
        "asset_type": AssetType.ETF if is_etf else AssetType.STOCK,
        "asset_class": asset_class,
        "category": category,
        "geography": geography,
        "is_esg": asset_class == AssetClass.ESG,
    }
    
    return asset_data

def classify_asset(ticker: str, info: Dict) -> tuple:
    """
    Dynamically classify an asset based on Yahoo Finance metadata.
    Returns: (AssetClass, AssetCategory, geography_string)
    """
    name = info.get('longName', '').lower()
    short_name = info.get('shortName', '').lower()
    quote_type = info.get('quoteType', '').upper()
    currency = info.get('currency', '').upper()
    
    # Initialize defaults
    asset_class = AssetClass.EQUITIES_WORLD
    category = AssetCategory.EQUITIES
    geography = "Global"
    
    # 1. Detect Bonds / Fixed Income
    if quote_type == 'ETF' and any(word in name or word in short_name for word in ["bond", "treasury", "fixed income", "debt", "obligations", "corporate"]):
        return AssetClass.FIXED_INCOME, AssetCategory.BONDS, "Global"
        
    # 2. Detect ESG
    if any(word in name or word in short_name for word in ["esg", "sustainable", "socially responsible", "durable", "impact"]):
        return AssetClass.ESG, AssetCategory.EQUITIES, "Global"
        
    # 4. Detect Sectors (keep as equities but specific class)
    if "select sector" in name or "sector index" in name or ticker.startswith("XL"):
        return AssetClass.SECTOR, AssetCategory.EQUITIES, "Global"

    # 4. Geography Detection
    eu_suffixes = (".PA", ".DE", ".AS", ".LS", ".MI", ".MC", ".SW", ".L", ".FR", ".EU")
    if ticker.endswith(eu_suffixes) or currency == 'EUR':
        asset_class = AssetClass.EQUITIES_EU
        geography = "Europe"
    elif currency == 'USD':
        # Check if it's Emerging Markets (EEM, VWO, etc.)
        if any(word in name for word in ["emerging", "china", "india", "brazil", "taiwan", "vnm", "mchi"]):
            asset_class = AssetClass.EQUITIES_EM
            geography = "Emerging"
        else:
            asset_class = AssetClass.EQUITIES_US
            geography = "US"
    elif any(word in name for word in ["emerging", "emerge"]):
        asset_class = AssetClass.EQUITIES_EM
        geography = "Emerging"

    return asset_class, category, geography

def calculate_volatility(ticker: str, period: str = YAHOO_FINANCE_PERIOD) -> Optional[float]:
    """Calculate annualized volatility from historical returns."""
    try:
        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            return None
            
        # Daily returns
        returns = data['Close'].pct_change().dropna()
        
        # Annualized volatility (252 trading days)
        vol = returns.std() * np.sqrt(252)
        return float(vol)
    except Exception:
        return None

def get_sparkline(ticker: str, period: str = "3y", points: int = 20) -> List[float]:
    """Get a simplified list of price points for sparkline charts (Normalized 0-1)."""
    return get_sparklines_batch([ticker], period, points).get(ticker, [])

def get_sparklines_batch(tickers: List[str], period: str = "3y", points: int = 20) -> Dict[str, List[float]]:
    """Fetch and normalize sparklines for multiple tickers in one batch."""
    if not tickers:
        return {}
        
    results = {}
    
    # Process in sub-batches of 50 to avoid URI length or rate limit issues
    batch_size = 50
    for i in range(0, len(tickers), batch_size):
        sub_tickers = tickers[i:i+batch_size]
        try:
            # Download sub-batch
            data = yf.download(sub_tickers, period=period, progress=False, timeout=20, group_by='ticker')
            if data.empty:
                continue
            
            for ticker in sub_tickers:
                try:
                    # Robust handling of yfinance return structure
                    if len(sub_tickers) > 1 and isinstance(data.columns, pd.MultiIndex):
                        if ticker not in data.columns.levels[0]: continue
                        ticker_data = data[ticker]
                    else:
                        # Single ticker or simplified DataFrame
                        ticker_data = data
                    
                    if 'Close' in ticker_data:
                        prices = ticker_data['Close']
                    elif 'Adj Close' in ticker_data:
                        prices = ticker_data['Adj Close']
                    else:
                        continue
                    
                    # Flatten and remove NaNs
                    vals = np.array(prices).flatten()
                    vals = vals[~np.isnan(vals)]
                    
                    if len(vals) < 2:
                        results[ticker] = []
                        continue
                        
                    indices = np.linspace(0, len(vals) - 1, points, dtype=int)
                    sampled = vals[indices]
                    
                    min_p = np.min(sampled)
                    max_p = np.max(sampled)
                    if max_p == min_p:
                        results[ticker] = [0.5] * points
                    else:
                        normalized = (sampled - min_p) / (max_p - min_p)
                        results[ticker] = [round(float(p), 4) for p in normalized]
                except Exception as inner_e:
                    print(f"Error processing sparkline for {ticker}: {inner_e}")
                    results[ticker] = []
        except Exception as e:
            print(f"Sub-batch sparkline error ({i}-{i+batch_size}): {e}")
                
    return results

def fetch_universe_batch(tickers: List[str], asset_type: AssetType) -> pd.DataFrame:
    """Fetch data for a batch of tickers."""
    results = []
    
    print(f"Fetching data for {len(tickers)} {asset_type.value}s...")
    
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            
            # Basic info
            name = info.get('shortName', info.get('longName', ticker))
            
            # Performance stats
            hist = t.history(period="1y")
            if hist.empty:
                continue
            
            # Volatility (annualized std of daily returns)
            returns = hist['Close'].pct_change().dropna()
            volatility = float(returns.std() * np.sqrt(252))
            
            # Liquidity (avg daily volume * last price)
            avg_volume = float(hist['Volume'].mean())
            last_price = float(hist['Close'].iloc[-1])
            liquidity = avg_volume * last_price
            
            # Use dynamic classification
            asset_class, category, geography = classify_asset(ticker, info)
                
            results.append({
                "ticker": ticker,
                "name": name,
                "asset_type": asset_type.value,
                "asset_class": asset_class.value,
                "category": category.value,
                "geography": geography,
                "volatility": volatility,
                "avg_volume": avg_volume,
                "last_price": last_price,
                "liquidity": liquidity,
                "expense_ratio": info.get('expenseRatio', 0.001) if asset_type == AssetType.ETF else 0.0,
                "is_esg": asset_class == AssetClass.ESG
            })
            
            # Small delay to respect rate limits
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue
            
    return pd.DataFrame(results)

def load_or_update_universe(max_age_days: int = 7) -> pd.DataFrame:
    """Load universe from cache or update if older than max_age_days."""
    age = get_universe_age(UNIVERSE_FILE)
    
    if age is not None and age < max_age_days:
        print(f"Universe is {age} days old, loading from file...")
        return load_universe_from_csv(UNIVERSE_FILE)
        
    print("Universe missing or outdated. Fetching fresh data from Yahoo Finance...")
    
    etf_df = fetch_universe_batch(DEFAULT_ETF_TICKERS, AssetType.ETF)
    stock_df = fetch_universe_batch(DEFAULT_STOCK_TICKERS, AssetType.STOCK)
    
    full_df = pd.concat([etf_df, stock_df], ignore_index=True)
    save_universe_to_csv(full_df, UNIVERSE_FILE)
    
    return full_df
