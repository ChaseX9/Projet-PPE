"""ML-based profile classification and MiFID II coherence checking."""
import numpy as np
from typing import Dict, Tuple
from .schemas import RawProfile, RefinedProfile, RiskProfile, ExpertiseLevel, LossCapacity, RiskTolerance

def simulate_ml_classification(risk_score: float, horizon_score: float) -> RiskProfile:
    """
    Simulates a logic/ML-driven classification.
    In a real app, this might call a scikit-learn model trained on thousands of profiles.
    """
    # Simple rule-based logic that represents a trained model's decision boundary
    if risk_score < 0.4:
        return RiskProfile.PRUDENT
    elif risk_score < 0.7:
        return RiskProfile.EQUILIBRE
    else:
        return RiskProfile.DYNAMIQUE

def normalize_investment_amount(amount) -> 'InvestmentAmount':
    """Helper to map an exact float amount to the corresponding Enum."""
    from .schemas import InvestmentAmount
    if isinstance(amount, InvestmentAmount):
        return amount
    try:
        val = float(amount)
        if val < 100:
            return InvestmentAmount.UNDER_100
        elif val <= 500:
            return InvestmentAmount.FROM_100_TO_500
        elif val <= 1000:
            return InvestmentAmount.FROM_500_TO_1000
        else:
            return InvestmentAmount.OVER_1000
    except (ValueError, TypeError):
        return InvestmentAmount.FROM_100_TO_500

def check_coherence(profile: RawProfile) -> Dict[str, str]:
    """
    MiFID II Coherence checks.
    Flags inconsistencies or provides pedagogical warnings for non-expert users.
    """
    flags = {}
    responses = profile.raw_responses
    
    # 1. High risk tolerance vs No loss capacity
    if responses.risk_tolerance == RiskTolerance.HIGH and responses.loss_capacity == LossCapacity.NONE:
        flags["risk_vs_capacity"] = "⚠️ Tolérance au risque élevée mais capacité de perte nulle : prudence recommandée."
        
    # 2. Expert knowledge vs No experience
    if responses.knowledge_level == ExpertiseLevel.EXPERT and responses.experience.value == "none":
        flags["knowledge_vs_experience"] = "💡 Connaissances expertes sans expérience pratique : nous privilégions la transparence."
    
    # New Phase 5 checks
    from .schemas import InvestmentAmount, InvestmentMode
    
    # 3. Small amount + High Risk
    normalized_amount = normalize_investment_amount(responses.investment_amount)
    if normalized_amount in [InvestmentAmount.UNDER_100, InvestmentAmount.FROM_100_TO_500] and \
       responses.risk_tolerance == RiskTolerance.HIGH:
        flags["amount_risk"] = "⚠️ Petit montant avec risque élevé : privilégiez une approche simple pour débuter."

    # 4. Recurring investment + Short horizon
    from .schemas import Horizon
    if responses.investment_mode in [InvestmentMode.RECURRING, InvestmentMode.BOTH] and responses.horizon == Horizon.SHORT:
        flags["mode_horizon"] = "💡 Investissement récurrent : un horizon plus long permet de mieux lisser les risques."

    return flags

def refine_profile(raw_profile: RawProfile) -> RefinedProfile:
    """
    Refine the profile (Bloc C).
    Applies ML classification, coherence checks, and determines explanation level.
    """
    # 1. Classification
    risk_profile = simulate_ml_classification(raw_profile.risk_score, raw_profile.horizon_score)
    
    # 2. Coherence
    coherence_flags = check_coherence(raw_profile)
    
    # 3. Confidence score (simplified ML confidence)
    confidence = 0.95 if not coherence_flags else 0.65
    
    # 4. Explanation level (Required by MiFID II for transparency)
    explanation_level = "standard"
    if raw_profile.expertise_level == ExpertiseLevel.EXPERT:
        explanation_level = "expert"
    elif coherence_flags:
        explanation_level = "detailed"
        
    return RefinedProfile(
        risk_profile=risk_profile,
        expertise_level=raw_profile.expertise_level,
        risk_score=raw_profile.risk_score,
        horizon_score=raw_profile.horizon_score,
        confidence_score=confidence,
        coherence_flags=coherence_flags,
        explanation_level=explanation_level,
        raw_profile=raw_profile
    )
