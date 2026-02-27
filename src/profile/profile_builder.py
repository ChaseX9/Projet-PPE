"""Logic to convert questionnaire responses into a raw investment profile."""
from .schemas import (
    QuestionnaireInput, RawProfile, ExpertiseLevel, 
    Horizon, RiskTolerance, LossCapacity, KnowledgeLevel, Experience
)

def calculate_risk_score(input_data: QuestionnaireInput) -> float:
    """Calculate a base risk score from 0 to 1."""
    # Mapping tolerance to scores
    tolerance_map = {RiskTolerance.LOW: 0.2, RiskTolerance.MEDIUM: 0.5, RiskTolerance.HIGH: 0.9}
    
    # Mapping loss capacity to scores (MiFID II: Very important)
    capacity_map = {
        LossCapacity.NONE: 0.0, 
        LossCapacity.SMALL: 0.3, 
        LossCapacity.MEDIUM: 0.6, 
        LossCapacity.HIGH: 1.0
    }
    
    base_score = (tolerance_map[input_data.risk_tolerance] * 0.4) + \
                 (capacity_map[input_data.loss_capacity] * 0.6)
    
    # Phase 13: DCA Bonus
    # Recurring investment reduces timing risk, allowing for a slightly higher risk score (+0.05)
    from .schemas import InvestmentMode
    if input_data.investment_mode in [InvestmentMode.RECURRING, InvestmentMode.BOTH]:
        base_score += 0.05
                 
    return round(min(base_score, 1.0), 2)

def calculate_horizon_score(horizon: Horizon) -> float:
    """Convert horizon to a score from 0 to 1."""
    score_map = {Horizon.SHORT: 0.2, Horizon.MEDIUM: 0.5, Horizon.LONG: 1.0}
    return score_map[horizon]

def determine_expertise(knowledge: KnowledgeLevel, experience: Experience) -> ExpertiseLevel:
    """Determine if the user is an expert based on MiFID II definitions."""
    if knowledge == KnowledgeLevel.EXPERT and experience == Experience.EXTENSIVE:
        return ExpertiseLevel.EXPERT
    return ExpertiseLevel.NON_EXPERT

def build_raw_profile(input_data: QuestionnaireInput) -> RawProfile:
    """Process questionnaire into a RawProfile."""
    risk_score = calculate_risk_score(input_data)
    horizon_score = calculate_horizon_score(input_data.horizon)
    expertise = determine_expertise(input_data.knowledge_level, input_data.experience)
    
    constraints = []
    if input_data.liquidity_need:
        constraints.append("High liquidity required")
    if input_data.esg_preference:
        constraints.append("ESG/Sustainability priority")
    if input_data.use_black_litterman and expertise == ExpertiseLevel.EXPERT:
        constraints.append("Advanced optimization enabled (Black-Litterman)")
        
    return RawProfile(
        risk_score=risk_score,
        horizon_score=horizon_score,
        expertise_level=expertise,
        constraints=constraints,
        raw_responses=input_data
    )
