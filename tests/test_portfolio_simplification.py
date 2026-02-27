import pytest
from src.portfolio.recommender import simplify_portfolio
from src.profile.schemas import (
    RefinedProfile, RawProfile, QuestionnaireInput, 
    ExpertiseLevel, RiskProfile, InvestmentGoal, 
    Horizon, RiskTolerance, LossCapacity, KnowledgeLevel, Experience
)
from src.utils.config import (
    SIMPLIFY_LIMIT_NON_EXPERT, 
    SIMPLIFY_LIMIT_EXPERT, 
    MIN_WEIGHT_THRESHOLD
)

def create_mock_profile(expertise=ExpertiseLevel.NON_EXPERT):
    qi = QuestionnaireInput(
        investment_goal=InvestmentGoal.RETIREMENT,
        horizon=Horizon.LONG,
        risk_tolerance=RiskTolerance.HIGH,
        loss_capacity=LossCapacity.HIGH,
        knowledge_level=KnowledgeLevel.EXPERT,
        experience=Experience.EXTENSIVE,
        use_black_litterman=False
    )
    
    raw = RawProfile(
        risk_score=0.8,
        horizon_score=0.8,
        expertise_level=expertise,
        constraints=[],
        raw_responses=qi
    )
    
    return RefinedProfile(
        risk_profile=RiskProfile.DYNAMIQUE,
        risk_score=0.8,
        horizon_score=0.8,
        expertise_level=expertise,
        confidence_score=0.9,
        coherence_flags={},
        explanation_level="high",
        raw_profile=raw
    )

def test_dust_removal():
    profile = create_mock_profile()
    # Weights with many small components
    weights = {
        "AAPL": 0.40,
        "MSFT": 0.40,
        "DUST1": 0.01,
        "DUST2": 0.015,
        "DUST3": 0.024,
        "VALID1": 0.15
    }
    
    simplified = simplify_portfolio(weights, profile)
    
    # Should only keep AAPL, MSFT, VALID1
    assert "DUST1" not in simplified
    assert "DUST2" not in simplified
    assert "DUST3" not in simplified
    assert "AAPL" in simplified
    assert "MSFT" in simplified
    assert "VALID1" in simplified
    
    # Check renormalization
    assert sum(simplified.values()) == pytest.approx(1.0)
    # AAPL should go from 40% of original (0.95 total) to ~42.1%
    assert simplified["AAPL"] > 0.40

def test_position_limit_non_expert():
    profile = create_mock_profile(ExpertiseLevel.NON_EXPERT)
    # Create 20 valid positions (all above 2.5%)
    weights = {f"TICKER_{i}": 0.05 for i in range(20)}
    
    simplified = simplify_portfolio(weights, profile)
    
    assert len(simplified) == SIMPLIFY_LIMIT_NON_EXPERT
    assert sum(simplified.values()) == pytest.approx(1.0)

def test_position_limit_expert():
    profile = create_mock_profile(ExpertiseLevel.EXPERT)
    # Create 20 valid positions
    weights = {f"TICKER_{i}": 0.05 for i in range(20)}
    
    simplified = simplify_portfolio(weights, profile)
    
    assert len(simplified) == SIMPLIFY_LIMIT_EXPERT
    assert sum(simplified.values()) == pytest.approx(1.0)

def test_extreme_case():
    profile = create_mock_profile()
    # If all are below threshold (e.g. 50 assets at 2% each)
    weights = {f"TICKER_{i}": 0.02 for i in range(50)}
    
    simplified = simplify_portfolio(weights, profile)
    
    # Should fallback to top N and renormalize
    assert len(simplified) == SIMPLIFY_LIMIT_NON_EXPERT
    assert sum(simplified.values()) == pytest.approx(1.0)
