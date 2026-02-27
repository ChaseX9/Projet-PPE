"""Management of target asset allocations by risk profile."""
from typing import Dict
from ..profile.schemas import RiskProfile
from ..utils.config import RISK_ALLOCATIONS

def get_target_allocation(profile: RiskProfile) -> Dict[str, float]:
    """Get the target equity/bond allocation for a given risk profile."""
    # profile is an enum, we need its value (e.g., "Prudent")
    return RISK_ALLOCATIONS.get(profile.value, RISK_ALLOCATIONS["Équilibré"])

def validate_allocation(allocation: Dict[str, float]):
    """Ensure allocation sums to 1.0 (100%)."""
    total = sum(allocation.values())
    if not (0.99 <= total <= 1.01):
        raise ValueError(f"Allocation must sum to 1.0, got {total}")
