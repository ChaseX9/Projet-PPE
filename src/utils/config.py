"""Configuration settings for the robo-advisor."""
from pathlib import Path
# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UNIVERSE_FILE = DATA_DIR / "universe.csv"
DATABASE_URL = f"sqlite:///{DATA_DIR}/robo_advisor.db"

# Data update settings
YAHOO_FINANCE_PERIOD = "3y"  # Historical data period for volatility calculation
VOLATILITY_WINDOW_YEARS = 3  # Years to use for volatility calculation

# Universe composition - curated list of ETFs and stocks
DEFAULT_ETF_TICKERS = [
    # --- Global / World ---
    "VT", "ACWI", "URTH", "VWCE.DE", "CW8.PA", "IWDA.AS",
    
    # --- US Equities ---
    "VTI", "SPY", "VOO", "QQQ", "IWM", "VUG", "VTV", "DIA", "SCHD",
    
    # --- European Equities (PEA Eligible favorites) ---
    "VGK", "EZU", "FEZ", "IE00B4L5Y983", # iShares Core MSCI Europe
    "ANX.PA", "ESE.PA", "PTPXE.PA", "PMEH.PA", # Amundi/Lyxor PEA ETFs
    "PSP5.PA", "PUST.PA", "PCW8.PA", "PAEEM.PA", # PEA ETFs
    
    # --- Emerging Markets ---
    "VWO", "EEM", "IEMG", "SCHE", "VNM", "MCHI", "INDA",
    
    # --- Fixed Income (Bonds) ---
    "AGG", "BND", "TLT", "LQD", "HYG", "VCIT", "VGIT", "BNDX", "VWOB",
    "EMB", "SHY", "IEF", "TIP", "MUB", "JNK", "MBB",
    
    # --- Sectors & Themes ---
    "XLK", "XLV", "XLF", "XLE", "XLY", "XLP", "XLI", "XLB", "XLRE", "XLU",
    "SMH", "IBB", "KRE", "KBE", "ITA", "ICLN", "TAN", "LIT",
    
    # --- ESG / Sustainable ---
    "ESGV", "ESGU", "SUSL", "VOTE", "DSI", "SUSA", "ESGE"
]

DEFAULT_STOCK_TICKERS = [
    # --- US Large Cap (Tech & Growth) ---
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "AVGO", "ORCL", "ADBE",
    "CRM", "NFLX", "AMD", "TXN", "INTC", "QCOM", "MU", "PANW", "SNPS", "CDNS",
    
    # --- US Large Cap (Value & Defensive) ---
    "JPM", "JNJ", "V", "WMT", "PG", "UNH", "HD", "MA", "DIS", "BAC", "KO", "PEP",
    "CVX", "XOM", "ABBV", "PFE", "MRK", "TMO", "CSCO", "ABT", "VZ", "T",
    
    
    # --- European Blue Chips (CAC40 Complete) ---
    # Luxe
    "MC.PA", "OR.PA", "RMS.PA", "KER.PA",
    # Énergie & Utilities
    "TTE.PA", "ENGI.PA",
    # Industrie & Aéronautique
    "AIR.PA", "AI.PA", "SAF.PA", "SU.PA", "VIE.PA", "SGO.PA",
    # Banques & Finance
    "BNP.PA", "GLE.PA", "ACA.PA",
    # Pharma & Santé
    "SAN.PA", "ERF.PA",
    # Télécoms & Tech
    "ORA.PA", "CS.PA", "DSY.PA", "CAP.PA",
    # Distribution & Consommation
    "BN.PA", "CA.PA", "PUB.PA", "RNO.PA", "STM.PA",
    # Immobilier & Services
    "URW.PA", "WLN.PA",
    
    # --- DAX (Germany) ---
    "ASML", "SAP", "SIE.DE", "DTE.DE", "MBG.DE", "BMW.DE", "BAS.DE", "ALV.DE",
    "VOW3.DE", "DHL.DE", "ADS.DE",
    
    # --- FTSE (UK) & Switzerland ---
    "NESN.SW", "NOVN.SW", "ROG.SW", "AZN", "GSK", "HSBC", "BP", "SHEL",
    "ULVR.L", "DGE.L", "RIO.L",
    
    # --- Emerging Markets Leaders ---
    "TSM", "BABA", "TCEHY", "PDD", "JD", "BIDU", "NTES", "HDB", "IBN", "INFY"
]

# Risk profile allocation targets
RISK_ALLOCATIONS = {
    "Prudent": {
        "equities": 0.30,
        "bonds": 0.70
    },
    "Équilibré": {
        "equities": 0.60,
        "bonds": 0.40
    },
    "Dynamique": {
        "equities": 0.80,
        "bonds": 0.20
    }
}

# Portfolio constraints (UPDATED for Phase 5)
# Global asset count limits (all users)
MIN_ASSETS = 2  # Allow concentrated portfolios when justified
MAX_ASSETS = 10  # Main limit for all users

# Dynamic max weight per asset (by risk profile)
# Prudent investors can have more concentration (fewer, larger positions)
MAX_WEIGHT_PRUDENT = 0.50  # Up to 50% for prudent (allows 60/40 portfolios)
MAX_WEIGHT_EQUILIBRE = 0.35  # Up to 35% for balanced
MAX_WEIGHT_DYNAMIQUE = 0.30  # Up to 30% for dynamic
MAX_WEIGHT_PER_ASSET = 0.35  # Global default

# NO minimum weight threshold - allow natural optimization results
# Removed: MIN_WEIGHT_THRESHOLD

# Optimization settings
MARKOWITZ_TARGET_RETURN = None  # Let it optimize for max Sharpe ratio
RISK_FREE_RATE = 0.02  # 2% annual risk-free rate assumption

# Black-Litterman settings
BL_TAU = 0.05  # Uncertainty in prior estimate
BL_RISK_AVERSION = 2.5  # Market risk aversion parameter

# Filtering & Simplification constraints
MIN_LIQUIDITY_VOLUME = 1000000  # $1M minimum daily volume
MAX_ETF_EXPENSE_RATIO = 0.005  # 0.5% max expense ratio for ETFs
MIN_WEIGHT_THRESHOLD = 0.025  # 2.5% minimum weight for any asset
SIMPLIFY_LIMIT_NON_EXPERT = 8
SIMPLIFY_LIMIT_EXPERT = 12

# API settings
API_TITLE = "CapInvest Recommendation Engine"
API_DESCRIPTION = "MiFID II compliant investment recommendation service"
API_VERSION = "0.1.0"

# Portfolio constraints (UPDATED for Phase 5)

# ========== WHITELIST : Actifs de Référence ==========
# Ces actifs sont universellement reconnus et reçoivent un bonus sur le reliability_score.
REFERENCE_ASSETS = {
    # ETFs World - Incontournables
    "VT", "ACWI", "VWCE.DE", "CW8.PA", "IWDA.AS", "URTH",
    # ETFs US - Piliers
    "SPY", "VOO", "VTI", "QQQ", "IWM",
    # ETFs Européens PEA - Reconnus
    "ANX.PA", "PSP5.PA", "PUST.PA", "PCW8.PA",
    # ETFs Obligations - Solides
    "AGG", "BND", "TLT", "LQD", "BNDX",
    # Actions US - Blue Chips mondiales
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "JPM", "JNJ", "V", "WMT", "PG",
    "UNH", "XOM", "CVX", "KO", "PEP", "HD", "MA", "BAC",
    # Actions EU - Champions nationaux très connus
    "MC.PA", "OR.PA", "TTE.PA", "AIR.PA", "BNP.PA", "SAN.PA", "ASML",
    "NESN.SW", "NOVN.SW", "AZN",
    # ETFs ESG - Référence
    "ESGV", "ESGU",
}

# Bonus de fiabilité accordé aux actifs de la whitelist (ajouté au reliability_score)
REFERENCE_ASSET_BONUS = 20

# ========== DIVERSIFICATION SECTORIELLE ==========
# Nombre max d'actifs par secteur dans la sélection finale
MAX_ASSETS_PER_SECTOR = {
    "Prudent": 1,
    "Équilibré": 2,
    "Dynamique": 2,
}
# Nombre minimum de secteurs différents dans le portefeuille final (hors obligations)
MIN_SECTORS_IN_PORTFOLIO = 3
