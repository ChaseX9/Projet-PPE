"""Pydantic schemas for user profiling (MiFID II)."""
from enum import Enum
from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, validator

class InvestmentGoal(Enum):
    RETIREMENT = "retirement"
    WEALTH_GROWTH = "wealth_growth"
    PROJECT = "project"  # (e.g., buying a house)
    SAFETY = "safety"

class Horizon(Enum):
    SHORT = "short"   # < 3 years
    MEDIUM = "medium" # 3-8 years
    LONG = "long"     # > 8 years

class RiskTolerance(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class LossCapacity(Enum):
    NONE = "none"
    SMALL = "small"
    MEDIUM = "medium"
    HIGH = "high"

class KnowledgeLevel(Enum):
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"

class Experience(Enum):
    NONE = "none"
    SOME = "some"
    EXTENSIVE = "extensive"

class RiskProfile(Enum):
    PRUDENT = "Prudent"
    EQUILIBRE = "Équilibré"
    DYNAMIQUE = "Dynamique"

class ExpertiseLevel(Enum):
    NON_EXPERT = "non_expert"
    EXPERT = "expert"

class InvestmentAmount(Enum):
    UNDER_100 = "under_100"
    FROM_100_TO_500 = "100_to_500"
    FROM_500_TO_1000 = "500_to_1000"
    OVER_1000 = "over_1000"

class InvestmentMode(Enum):
    ONE_TIME = "one_time"
    RECURRING = "recurring"
    BOTH = "both"

class QuestionnaireInput(BaseModel):
    """Input received from the frontend questionnaire."""
    investment_goal: InvestmentGoal
    horizon: Horizon
    risk_tolerance: RiskTolerance
    loss_capacity: LossCapacity
    knowledge_level: KnowledgeLevel
    experience: Experience
    
    # Optional details
    esg_preference: bool = False
    sector_preferences: Optional[List[str]] = None
    liquidity_need: bool = False
    use_black_litterman: bool = False
    market_views: Optional[List[Dict]] = None
    
    # New Phase 5 questions
    investment_amount: Union[float, InvestmentAmount] = InvestmentAmount.FROM_100_TO_500
    investment_mode: InvestmentMode = InvestmentMode.ONE_TIME

class RawProfile(BaseModel):
    """Raw profile after initial scoring (Bloc B)."""
    user_id: Optional[str] = None
    risk_score: float  # 0 to 1
    horizon_score: float # 0 to 1
    expertise_level: ExpertiseLevel
    constraints: List[str]
    raw_responses: QuestionnaireInput

class RefinedProfile(BaseModel):
    """Final refined profile after ML classification (Bloc C)."""
    risk_profile: RiskProfile
    expertise_level: ExpertiseLevel
    risk_score: float
    horizon_score: float
    confidence_score: float
    coherence_flags: Dict[str, str]
    explanation_level: str  # standard, detailed, expert
    raw_profile: RawProfile
