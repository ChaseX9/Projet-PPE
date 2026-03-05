"""Unit tests for optimization engine selection."""
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.profile.schemas import QuestionnaireInput, InvestmentGoal, Horizon, RiskTolerance, LossCapacity, KnowledgeLevel, Experience
from src.profile.profile_builder import build_raw_profile
from src.profile.profile_engine import refine_profile
from src.portfolio.recommender import build_portfolio

def test_engine_selection():
    # 1. Non-expert user requesting Black-Litterman
    non_expert_input = QuestionnaireInput(
        investment_goal=InvestmentGoal.WEALTH_GROWTH,
        horizon=Horizon.LONG,
        risk_tolerance=RiskTolerance.HIGH,
        loss_capacity=LossCapacity.HIGH,
        knowledge_level=KnowledgeLevel.NOVICE,
        experience=Experience.NONE,
        use_black_litterman=True
    )
    raw = build_raw_profile(non_expert_input)
    refined = refine_profile(raw)
    portfolio = build_portfolio(refined)
    
    print(f"Test Non-Expert + BL=True: Method = {portfolio['optimization_method']}")
    assert portfolio['optimization_method'] == "Markowitz"
    
    # 2. Expert user requesting Black-Litterman
    expert_input = QuestionnaireInput(
        investment_goal=InvestmentGoal.WEALTH_GROWTH,
        horizon=Horizon.LONG,
        risk_tolerance=RiskTolerance.HIGH,
        loss_capacity=LossCapacity.HIGH,
        knowledge_level=KnowledgeLevel.EXPERT,
        experience=Experience.EXTENSIVE,
        use_black_litterman=True
    )
    raw_exp = build_raw_profile(expert_input)
    refined_exp = refine_profile(raw_exp)
    portfolio_bl = build_portfolio(refined_exp)
    
    print(f"Test Expert + BL=True: Method = {portfolio_bl['optimization_method']}")
    assert portfolio_bl['optimization_method'] == "Black-Litterman"

    # 3. Expert user NOT requesting Black-Litterman
    expert_no_bl = QuestionnaireInput(
        investment_goal=InvestmentGoal.WEALTH_GROWTH,
        horizon=Horizon.LONG,
        risk_tolerance=RiskTolerance.HIGH,
        loss_capacity=LossCapacity.HIGH,
        knowledge_level=KnowledgeLevel.EXPERT,
        experience=Experience.EXTENSIVE,
        use_black_litterman=False
    )
    raw_no = build_raw_profile(expert_no_bl)
    refined_no = refine_profile(raw_no)
    portfolio_mw = build_portfolio(refined_no)
    
    print(f"Test Expert + BL=False: Method = {portfolio_mw['optimization_method']}")
    assert portfolio_mw['optimization_method'] == "Markowitz"

if __name__ == "__main__":
    try:
        test_engine_selection()
        print("\n✅ All engine selection tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
