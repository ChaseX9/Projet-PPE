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
    VOLATILITY_WINDOW_YEARS,
    REFERENCE_ASSETS,
    REFERENCE_ASSET_BONUS,
    RISK_FREE_RATE
)

# ============================================================
# SECTOR DETECTION (for sector-based diversification)
# ============================================================

# Mapping Yahoo Finance sector names → our internal canonical names
YAHOO_SECTOR_MAP = {
    "Technology": "Technologie",
    "Healthcare": "Santé",
    "Financial Services": "Finance",
    "Energy": "Énergie",
    "Consumer Cyclical": "Consommation Cyclique",
    "Consumer Defensive": "Consommation Défensive",
    "Industrials": "Industrie",
    "Basic Materials": "Matières Premières",
    "Real Estate": "Immobilier",
    "Communication Services": "Communication",
    "Utilities": "Services Publics",
}

# Manual sector override for well-known tickers (faster and more reliable than API calls)
MANUAL_SECTOR_MAP = {
    # ---- Technology ----
    "AAPL": "Technologie", "MSFT": "Technologie", "NVDA": "Technologie",
    "GOOGL": "Technologie", "META": "Technologie", "AVGO": "Technologie",
    "ORCL": "Technologie", "ADBE": "Technologie", "CRM": "Technologie",
    "AMD": "Technologie", "TXN": "Technologie", "INTC": "Technologie",
    "QCOM": "Technologie", "MU": "Technologie", "PANW": "Technologie",
    "SNPS": "Technologie", "CDNS": "Technologie",
    "DSY.PA": "Technologie", "CAP.PA": "Technologie", "STM.PA": "Technologie",
    "SAP": "Technologie", "ASML": "Technologie",
    # ---- Finance ----
    "JPM": "Finance", "BAC": "Finance", "V": "Finance", "MA": "Finance",
    "GS": "Finance", "MS": "Finance", "WFC": "Finance",
    "BNP.PA": "Finance", "GLE.PA": "Finance", "ACA.PA": "Finance",
    "ALV.DE": "Finance",
    # ---- Healthcare ----
    "JNJ": "Santé", "UNH": "Santé", "PFE": "Santé", "MRK": "Santé",
    "ABT": "Santé", "TMO": "Santé", "ABBV": "Santé",
    "SAN.PA": "Santé", "ERF.PA": "Santé",
    "NESN.SW": "Santé", "NOVN.SW": "Santé", "ROG.SW": "Santé",
    "AZN": "Santé", "GSK": "Santé",
    # ---- Energy ----
    "XOM": "Énergie", "CVX": "Énergie", "TTE.PA": "Énergie",
    "BP": "Énergie", "SHEL": "Énergie", "ENGI.PA": "Énergie", "EDF.PA": "Énergie",
    "BAS.DE": "Matières Premières",
    # ---- Consumer ----
    "WMT": "Consommation Défensive", "PG": "Consommation Défensive",
    "KO": "Consommation Défensive", "PEP": "Consommation Défensive",
    "AMZN": "Consommation Cyclique", "HD": "Consommation Cyclique",
    "TSLA": "Consommation Cyclique", "NFLX": "Communication",
    "DIS": "Communication", "VZ": "Communication", "T": "Communication",
    "BN.PA": "Consommation Défensive", "CA.PA": "Consommation Défensive",
    "PUB.PA": "Communication", "RNO.PA": "Consommation Cyclique",
    # ---- Industry ----
    "AIR.PA": "Industrie", "SAF.PA": "Industrie", "SU.PA": "Industrie",
    "VIE.PA": "Industrie", "SGO.PA": "Industrie", "AI.PA": "Industrie",
    "SIE.DE": "Industrie", "DHL.DE": "Industrie", "ADS.DE": "Industrie",
    "DTE.DE": "Communication",
    # ---- Luxury / Consumer Cyclical ----
    "MC.PA": "Luxe", "OR.PA": "Luxe", "RMS.PA": "Luxe", "KER.PA": "Luxe",
    # ---- ETF sectors ----
    "XLK": "Technologie", "XLV": "Santé", "XLF": "Finance",
    "XLE": "Énergie", "XLY": "Consommation Cyclique", "XLP": "Consommation Défensive",
    "XLI": "Industrie", "XLB": "Matières Premières", "XLRE": "Immobilier",
    "XLU": "Services Publics",
    "SMH": "Technologie", "IBB": "Santé", "ITA": "Industrie",
    "ICLN": "Énergie", "TAN": "Énergie", "LIT": "Technologie",
    "KRE": "Finance", "KBE": "Finance",
    # ---- ETF World / Multi-secteur ----
    "VT": "Multi-secteur", "ACWI": "Multi-secteur", "VWCE.DE": "Multi-secteur",
    "CW8.PA": "Multi-secteur", "IWDA.AS": "Multi-secteur", "URTH": "Multi-secteur",
    "VTI": "Multi-secteur", "SPY": "Multi-secteur", "VOO": "Multi-secteur",
    "QQQ": "Technologie",  # QQQ is tech-heavy
    "IWM": "Multi-secteur", "VUG": "Multi-secteur", "VTV": "Multi-secteur",
    "DIA": "Multi-secteur", "SCHD": "Multi-secteur",
    "VGK": "Multi-secteur (Europe)", "EZU": "Multi-secteur (Europe)", "FEZ": "Multi-secteur (Europe)",
    "ANX.PA": "Multi-secteur (Europe)", "ESE.PA": "Multi-secteur (Europe)",
    "PSP5.PA": "Multi-secteur (Europe)", "PUST.PA": "Multi-secteur",
    "PCW8.PA": "Multi-secteur", "PAEEM.PA": "Multi-secteur (Émergents)",
    "VWO": "Multi-secteur (Émergents)", "EEM": "Multi-secteur (Émergents)",
    "IEMG": "Multi-secteur (Émergents)", "SCHE": "Multi-secteur (Émergents)",
    "MCHI": "Multi-secteur (Émergents)", "INDA": "Multi-secteur (Émergents)",
    "BABA": "Consommation Cyclique", "TSM": "Technologie",
    # ---- Bonds ----
    "AGG": "Obligations", "BND": "Obligations", "TLT": "Obligations",
    "LQD": "Obligations", "HYG": "Obligations", "VCIT": "Obligations",
    "VGIT": "Obligations", "BNDX": "Obligations", "VWOB": "Obligations",
    "EMB": "Obligations", "SHY": "Obligations", "IEF": "Obligations",
    "TIP": "Obligations", "MUB": "Obligations", "JNK": "Obligations", "MBB": "Obligations",
    # ---- ESG ----
    "ESGV": "Multi-secteur", "ESGU": "Multi-secteur", "SUSL": "Multi-secteur",
    "VOTE": "Multi-secteur", "DSI": "Multi-secteur", "SUSA": "Multi-secteur",
    "ESGE": "Multi-secteur (Émergents)",
    # ---- Immobilier ----
    "URW.PA": "Immobilier", "WLN.PA": "Immobilier",
    # ---- Matières premièresr / Mines ----
    "RIO.L": "Matières Premières",
    # ---- UK ----
    "ULVR.L": "Consommation Défensive", "DGE.L": "Consommation Défensive",
    "HSBC": "Finance", "BP": "Énergie",
    # ---- Divers EU ----
    "MBG.DE": "Consommation Cyclique", "BMW.DE": "Consommation Cyclique",
    "VOW3.DE": "Consommation Cyclique",
    # ---- Inde / Emergents ----
    "HDB": "Finance", "IBN": "Finance", "INFY": "Technologie",
    "PDD": "Consommation Cyclique", "JD": "Consommation Cyclique",
    "BIDU": "Technologie", "NTES": "Communication", "TCEHY": "Communication",
}


def detect_sector(ticker: str, info: Dict) -> str:
    """
    Detect the sector of an asset. Uses a manual map first for speed and reliability,
    then falls back to Yahoo Finance API data.
    """
    # 1. Manual map (fast, reliable)
    if ticker in MANUAL_SECTOR_MAP:
        return MANUAL_SECTOR_MAP[ticker]
    
    # 2. Yahoo Finance API 'sector' field
    yf_sector = info.get("sector", "")
    if yf_sector:
        return YAHOO_SECTOR_MAP.get(yf_sector, yf_sector)
    
    # 3. Fallback: classify by bond keywords
    name = info.get("longName", "").lower()
    if any(w in name for w in ["bond", "treasury", "fixed income", "obligations"]):
        return "Obligations"
    
    return "Autre"


# ============================================================
# RELIABILITY SCORE CALCULATION
# ============================================================

def calculate_reliability_score(
    ticker: str,
    sharpe_ratio: float,
    liquidity: float,
    max_drawdown: float,
    listing_years: float,
    all_liquidities: pd.Series,
) -> float:
    """
    Calculate a reliability score from 0 to 100.
    - Sharpe Ratio: 40 pts (risk-adjusted performance)
    - Liquidity (AUM): 30 pts (normalized vs universe)
    - Stability (inverse max drawdown): 20 pts
    - Seniority (listing years): 10 pts
    + REFERENCE_ASSET_BONUS if in whitelist
    """
    score = 0.0

    # --- 1. Sharpe Ratio (40 pts) ---
    # Good Sharpe = > 1.0. Excellent = > 2.0. Cap at 3.
    clamped_sharpe = max(0.0, min(sharpe_ratio, 3.0))
    score += (clamped_sharpe / 3.0) * 40.0

    # --- 2. Liquidity / AUM (30 pts) ---
    # Log-normalize vs the entire universe to reward large, well-known assets
    if all_liquidities is not None and len(all_liquidities) > 1 and liquidity > 0:
        log_liq = np.log1p(liquidity)
        log_max = np.log1p(all_liquidities.max())
        log_min = np.log1p(all_liquidities.min())
        if log_max > log_min:
            normalized_liq = (log_liq - log_min) / (log_max - log_min)
        else:
            normalized_liq = 0.5
        score += normalized_liq * 30.0
    else:
        score += 10.0  # neutral if unknown

    # --- 3. Stability / Max Drawdown (20 pts) ---
    # max_drawdown is a negative number (e.g., -0.35 = -35% worst drawdown)
    # Less negative = more stable
    clamp_dd = max(-1.0, min(max_drawdown, 0.0))  # ensure [-1, 0]
    # Convert: 0% drawdown = 20pts, -100% = 0pts
    score += (1.0 + clamp_dd) * 20.0

    # --- 4. Seniority (10 pts) ---
    # > 10 years = full 10pts, linear before
    score += min(listing_years / 10.0, 1.0) * 10.0

    # --- 5. Reference Asset Bonus ---
    if ticker in REFERENCE_ASSETS:
        score += REFERENCE_ASSET_BONUS

    return round(min(score, 100.0), 1)


def calculate_sharpe_and_drawdown(ticker: str, period: str = YAHOO_FINANCE_PERIOD):
    """
    Calculate Sharpe ratio and max drawdown for an asset from historical data.
    Returns (annualized_return, volatility, sharpe, max_drawdown, listing_years).
    """
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        if hist.empty or len(hist) < 50:
            return 0.0, 0.2, 0.0, -0.5, 2.0
        
        prices = hist["Close"].dropna()
        returns = prices.pct_change().dropna()

        # Annualized return
        total_return = (prices.iloc[-1] / prices.iloc[0]) - 1
        n_years = len(prices) / 252
        ann_return = (1 + total_return) ** (1 / max(n_years, 0.5)) - 1

        # Annualized volatility
        vol = float(returns.std() * np.sqrt(252))

        # Sharpe
        sharpe = (ann_return - RISK_FREE_RATE) / vol if vol > 0 else 0.0

        # Max drawdown
        rolling_max = prices.cummax()
        drawdown = (prices - rolling_max) / rolling_max
        max_dd = float(drawdown.min())

        # Listing years (approximate)
        listing_date = t.info.get("firstTradeDateEpochUtc")
        if listing_date:
            listing_years = (datetime.now().timestamp() - listing_date) / (365.25 * 24 * 3600)
        else:
            listing_years = n_years  # fallback

        return ann_return, vol, sharpe, max_dd, max(listing_years, 0.5)

    except Exception as e:
        print(f"Error in sharpe/drawdown for {ticker}: {e}")
        return 0.0, 0.2, 0.0, -0.5, 2.0


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
        "sector": detect_sector(ticker, info),
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
        
    # 3. Detect Sectors
    if "select sector" in name or "sector index" in name or ticker.startswith("XL"):
        return AssetClass.SECTOR, AssetCategory.EQUITIES, "Global"

    # 4. Geography Detection
    eu_suffixes = (".PA", ".DE", ".AS", ".LS", ".MI", ".MC", ".SW", ".L", ".FR", ".EU")
    if ticker.endswith(eu_suffixes) or currency == 'EUR':
        asset_class = AssetClass.EQUITIES_EU
        geography = "Europe"
    elif currency == 'USD':
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
            
        returns = data['Close'].pct_change().dropna()
        vol = returns.std() * np.sqrt(252)
        return float(vol)
    except Exception:
        return None


def get_sparkline(ticker: str, period: str = "3y", points: int = 20) -> List[dict]:
    """Get a simplified list of price points and dates for sparkline charts."""
    return get_sparklines_batch([ticker], period, points).get(ticker, [])


def get_sparklines_batch(tickers: List[str], period: str = "3y", points: int = 20) -> Dict[str, List[dict]]:
    """Fetch and format sparklines for multiple tickers in one batch."""
    if not tickers:
        return {}
        
    results = {}
    batch_size = 50
    
    for i in range(0, len(tickers), batch_size):
        sub_tickers = tickers[i:i+batch_size]
        try:
            data = yf.download(sub_tickers, period=period, progress=False, timeout=20, group_by='ticker')
            if data.empty:
                continue
            
            for ticker in sub_tickers:
                try:
                    if len(sub_tickers) > 1 and isinstance(data.columns, pd.MultiIndex):
                        if ticker not in data.columns.levels[0]: continue
                        ticker_data = data[ticker]
                    else:
                        ticker_data = data
                    
                    if 'Close' in ticker_data:
                        prices = ticker_data['Close']
                    elif 'Adj Close' in ticker_data:
                        prices = ticker_data['Adj Close']
                    else:
                        continue
                    
                    clean_prices = prices.dropna()
                    
                    if len(clean_prices) < 2:
                        results[ticker] = []
                        continue
                        
                    indices = np.linspace(0, len(clean_prices) - 1, points, dtype=int)
                    sampled_prices = clean_prices.iloc[indices].values
                    # The index is a DatetimeIndex
                    sampled_dates = clean_prices.index[indices].strftime('%Y-%m-%d').tolist()
                    
                    sparkline_data = []
                    for k in range(len(sampled_prices)):
                        sparkline_data.append({
                            "date": sampled_dates[k],
                            "price": round(float(sampled_prices[k]), 4)
                        })
                        
                    results[ticker] = sparkline_data
                except Exception as inner_e:
                    print(f"Error processing sparkline for {ticker}: {inner_e}")
                    results[ticker] = []
        except Exception as e:
            print(f"Sub-batch sparkline error ({i}-{i+batch_size}): {e}")
                
    return results


def fetch_universe_batch(tickers: List[str], asset_type: AssetType) -> pd.DataFrame:
    """Fetch data for a batch of tickers, including sector and reliability score."""
    results = []
    
    print(f"Fetching data for {len(tickers)} {asset_type.value}s...")
    
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            
            name = info.get('shortName', info.get('longName', ticker))
            
            # Performance stats
            hist = t.history(period="3y")
            if hist.empty or len(hist) < 30:
                print(f"  ⚠️ Skipping {ticker} - insufficient history")
                continue
            
            # --- Volatility ---
            returns = hist['Close'].pct_change().dropna()
            volatility = float(returns.std() * np.sqrt(252))
            
            # --- Liquidity ---
            avg_volume = float(hist['Volume'].mean())
            last_price = float(hist['Close'].iloc[-1])
            liquidity = avg_volume * last_price
            
            # --- Annualized return & Sharpe ---
            prices = hist['Close'].dropna()
            n_years = len(prices) / 252
            total_return = (prices.iloc[-1] / prices.iloc[0]) - 1
            ann_return = (1 + total_return) ** (1 / max(n_years, 0.5)) - 1
            sharpe = (ann_return - RISK_FREE_RATE) / volatility if volatility > 0 else 0.0

            # --- Max Drawdown ---
            rolling_max = prices.cummax()
            drawdown = (prices - rolling_max) / rolling_max
            max_dd = float(drawdown.min())

            # --- Listing Years ---
            listing_ts = info.get("firstTradeDateEpochUtc")
            if listing_ts:
                listing_years = (datetime.now().timestamp() - listing_ts) / (365.25 * 24 * 3600)
            else:
                listing_years = n_years

            # --- Sector ---
            sector = detect_sector(ticker, info)

            # --- Classification ---
            asset_class, category, geography = classify_asset(ticker, info)
                
            results.append({
                "ticker": ticker,
                "name": name,
                "asset_type": asset_type.value,
                "asset_class": asset_class.value,
                "category": category.value,
                "geography": geography,
                "sector": sector,
                "volatility": volatility,
                "avg_volume": avg_volume,
                "last_price": last_price,
                "liquidity": liquidity,
                "sharpe_ratio": round(sharpe, 4),
                "max_drawdown": round(max_dd, 4),
                "listing_years": round(listing_years, 1),
                "ann_return": round(ann_return, 4),
                "expense_ratio": info.get('expenseRatio', 0.001) if asset_type == AssetType.ETF else 0.0,
                "is_esg": asset_class == AssetClass.ESG,
                # Reliability score calculated AFTER collecting all liquidities
                "reliability_score": 0.0,  # placeholder, calculated below
            })
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            # Potential lock error or rate limit - wait a bit longer
            time.sleep(1)
            continue
            
    if not results:
        print(f"❌ Fetching failed for ALL {len(tickers)} {asset_type.value}s.")
        return pd.DataFrame()
        
    df = pd.DataFrame(results)
    
    # Calculate reliability scores now that we have all liquidities
    if not df.empty and "liquidity" in df.columns:
        liq_series = df["liquidity"]
        df["reliability_score"] = df.apply(
            lambda row: calculate_reliability_score(
                ticker=row["ticker"],
                sharpe_ratio=row.get("sharpe_ratio", 0.0),
                liquidity=row.get("liquidity", 0.0),
                max_drawdown=row.get("max_drawdown", -0.5),
                listing_years=row.get("listing_years", 2.0),
                all_liquidities=liq_series,
            ),
            axis=1
        )
        print(f"  ✅ Reliability scores calculated for {len(df)} assets")
    
    return df


def load_or_update_universe(max_age_days: int = 2) -> pd.DataFrame:
    """Load universe from cache or update if older than max_age_days."""
    age = get_universe_age(UNIVERSE_FILE)
    
    if age is not None and age < max_age_days:
        print(f"Universe is {age} days old, loading from file...")
        df = load_universe_from_csv(UNIVERSE_FILE)
        
        # Guard: load_universe_from_csv returns None if file is missing
        if df is None or df.empty:
            print("⚠️ Universe file missing or empty — forcing fresh fetch.")
            age = None  # fall through to the fetch block below
        else:
            # Backwards compat: add missing columns with defaults
            if "sector" not in df.columns:
                df["sector"] = df["ticker"].map(lambda t: MANUAL_SECTOR_MAP.get(t, "Autre"))
            if "reliability_score" not in df.columns:
                df["reliability_score"] = 50.0  # neutral default
                # Apply reference bonus even for cached data
                df.loc[df["ticker"].isin(REFERENCE_ASSETS), "reliability_score"] = 70.0
            if "sharpe_ratio" not in df.columns:
                df["sharpe_ratio"] = 0.5
            return df
        
    print("Universe missing or outdated. Fetching fresh data from Yahoo Finance...")
    
    # 1. Start with hardcoded defaults
    final_tickers_etf = set(DEFAULT_ETF_TICKERS)
    final_tickers_stock = set(DEFAULT_STOCK_TICKERS)
    
    # 2. Add existing tickers from CSV to avoid de-merging
    existing_df = load_universe_from_csv(UNIVERSE_FILE)
    if existing_df is not None and not existing_df.empty:
        print(f"  🔍 Found {len(existing_df)} existing tickers in {UNIVERSE_FILE.name}")
        for _, row in existing_df.iterrows():
            t = row['ticker']
            # Determine asset type based on the existing record or simple heuristic
            atype = row.get('asset_type', AssetType.STOCK)
            if atype == AssetType.ETF:
                final_tickers_etf.add(t)
            else:
                final_tickers_stock.add(t)
                
    print(f"  🚀 Total to refresh: {len(final_tickers_etf)} ETFs, {len(final_tickers_stock)} Stocks")

    # 3. Fetch fresh data for the COMBINED set
    etf_df = fetch_universe_batch(list(final_tickers_etf), AssetType.ETF)
    stock_df = fetch_universe_batch(list(final_tickers_stock), AssetType.STOCK)
    
    full_df = pd.concat([etf_df, stock_df], ignore_index=True)
    
    if full_df.empty:
        print("❌ Total fresh fetch failed (0 assets). Preserving existing universe file.")
        return existing_df if existing_df is not None else pd.DataFrame()

    # Re-calculate reliability scores across the FULL universe (for proper normalization)
    if not full_df.empty and "liquidity" in full_df.columns:
        liq_series = full_df["liquidity"]
        full_df["reliability_score"] = full_df.apply(
            lambda row: calculate_reliability_score(
                ticker=row["ticker"],
                sharpe_ratio=row.get("sharpe_ratio", 0.0),
                liquidity=row.get("liquidity", 0.0),
                max_drawdown=row.get("max_drawdown", -0.5),
                listing_years=row.get("listing_years", 2.0),
                all_liquidities=liq_series,
            ),
            axis=1
        )
    
    save_universe_to_csv(full_df, UNIVERSE_FILE)
    
    return full_df
