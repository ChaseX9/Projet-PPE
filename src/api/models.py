"""FastAPI request/response models."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

from ..profile.schemas import (
    InvestmentGoal,
    Horizon,
    RiskTolerance,
    LossCapacity,
    KnowledgeLevel,
    Experience,
    RiskProfile,
    ExpertiseLevel,
    InvestmentAmount,
    InvestmentMode
)

class MarketView(BaseModel):
    """Market view for Black-Litterman optimization."""
    ticker: str
    direction: str  # bullish, neutral, bearish
    confidence: str # low, medium, high

class RecommendationRequest(BaseModel):
    """Request for portfolio recommendation."""
    investment_goal: InvestmentGoal
    horizon: Horizon
    risk_tolerance: RiskTolerance
    loss_capacity: LossCapacity
    knowledge_level: KnowledgeLevel
    experience: Experience
    investment_amount: Union[float, InvestmentAmount] = InvestmentAmount.FROM_100_TO_500
    investment_mode: InvestmentMode = InvestmentMode.ONE_TIME
    esg_preference: bool = False
    sector_preferences: Optional[List[str]] = None
    liquidity_need: bool = False
    use_black_litterman: bool = False
    market_views: Optional[List[MarketView]] = None
    force_universe_update: bool = False
    excluded_tickers: Optional[List[str]] = None
    parent_portfolio_id: Optional[int] = None  # For tracking adjusted portfolios

class PortfolioPosition(BaseModel):
    """Single position in the portfolio."""
    ticker: str
    weight: float
    name: str
    asset_type: str
    asset_class: str
    category: str
    geography: str
    sector: Optional[str] = None
    volatility: float
    reliability_score: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    explanation: Optional[Dict[str, str]] = None  # identification, reliability, role

class ProfileSummary(BaseModel):
    """Summary of user profile for response."""
    risk_profile: RiskProfile
    expertise_level: ExpertiseLevel
    risk_score: float
    horizon_score: float
    confidence_score: float
    coherence_flags: Dict[str, str]
    explanation_level: str
    raw_responses: Dict[str, Any] = Field(default_factory=dict)

class PortfolioSummary(BaseModel):
    """Portfolio summary for response."""
    positions: List[PortfolioPosition]
    category_allocations: Dict[str, float]
    expected_return: float
    volatility: float
    sharpe_ratio: float
    optimization_method: str
    processed_views: Optional[Dict[str, float]] = None # Ticker -> Effective return shift
    total_positions: int
    portfolio_explanation: Optional[str] = None  # Global portfolio explanation

class RecommendationResponse(BaseModel):
    """Response containing profile and portfolio recommendation."""
    profile: ProfileSummary
    portfolio: PortfolioSummary
    portfolio_id: Optional[int] = None  # Added for tracking

class PortfolioDetailResponse(BaseModel):
    """Detailed view for history."""
    id: int
    created_at: str
    profile: ProfileSummary
    portfolio: PortfolioSummary

class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    universe_loaded: bool
    universe_age_days: Optional[int] = None

class ExplorerAsset(BaseModel):
    """Asset representation for the Investment Library (Explorer)."""
    ticker: str
    name: str
    asset_type: str
    asset_class: str
    category: str
    geography: str
    sector: Optional[str] = None
    volatility_level: str  # Faible, Modéré, Élevé
    volatility_score: float
    is_esg: bool
    
    # Pedagogy
    pedagogy_short: str
    pedagogy_long: str
    utility: str
    why_capinvest: str
    suitable_profiles: List[str]
    key_takeaways: List[str]
    
    # Visuals
    sparkline: List[dict]
    has_sparkline: bool
