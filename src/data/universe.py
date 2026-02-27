"""Data models for investment universe."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class AssetType(Enum):
    ETF = "ETF"
    STOCK = "STOCK"

class AssetClass(Enum):
    EQUITIES_US = "Equities - US"
    EQUITIES_EU = "Equities - Europe"
    EQUITIES_EM = "Equities - Emerging Markets"
    EQUITIES_WORLD = "Equities - World"
    FIXED_INCOME = "Fixed Income"
    SECTOR = "Sector"
    ESG = "ESG / Sustainable"

class AssetCategory(Enum):
    EQUITIES = "equities"
    BONDS = "bonds"

class InvestmentAsset(BaseModel):
    """Represents an investment asset in the universe."""
    ticker: str
    name: str
    asset_type: AssetType
    asset_class: AssetClass
    category: AssetCategory
    geography: str
    sector: Optional[str] = None
    expense_ratio: Optional[float] = None
    is_esg: bool = False
    
    # Quantitative stats (calculated)
    volatility: Optional[float] = None
    avg_volume: Optional[float] = None
    last_price: Optional[float] = None

class UniverseMetadata(BaseModel):
    """Metadata about the stored universe."""
    last_updated: str
    asset_count: int
    source: str = "Yahoo Finance"
