"""
Suggestion rules for questionnaire guidance.

These rules define smart suggestions to guide users toward coherent investment profiles.
All rules are defined declaratively for auditability and testability (MiFID II compliance).

Architecture:
- Backend defines rules (source of truth)
- Frontend executes rules (real-time UX)
- Rules are versioned and auditable
"""
from typing import List, Dict, Any

# Version tracking for audit trail
RULES_VERSION = "5.1.0"  # Added missing loss_medium_risk rule (P100)

# Structural order of fields in the UI (Strictly enforced)
# Suggestions can only target fields with a STRICTLY HIGHER index
# Order follows real robo-advisor standards (Yomoni, Nalo, Wealthfront)
FIELD_ORDER = {
    "knowledge_level": 0,
    "experience": 1,
    "investment_goal": 2,
    "horizon": 3,
    "loss_capacity": 4,      # MiFID II: before risk tolerance
    "risk_tolerance": 5,     # Within allowed range set by loss_capacity
    "investment_amount": 6,  # Financial details after risk profile
    "investment_mode": 7,
    "portfolio_structure": 8 # Internal signal only
}

# Rule structure:
# {
#     "id": unique identifier
#     "priority": execution priority (higher = executed first)
#     "condition": dict of field:value pairs that trigger the rule
#     "suggestion": {
#         "field": target field to suggest for
#         "suggested_values": list of recommended values
#         "explanation": French explanation for the user
#         "confidence": "high" | "medium" | "low"
#     }
# }

SUGGESTION_RULES: List[Dict[str, Any]] = [
    # ========== PRIORITY 80: HORIZON → RISK RULES (MiFID II: Second Priority) ==========
    # Rule 1: Short Horizon → Moderate Risk
    {
        "id": "horizon_risk_short",
        "priority": 80,
        "condition": {"horizon": "short"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["low", "medium"],
            "explanation": (
                "Pour un horizon court terme, un risque modéré protège mieux votre capital. "
                "Il ne laisse pas assez de temps pour récupérer des pertes importantes."
            ),
            "confidence": "high"
        }
    },
    
    # Rule 2: Long Horizon → Higher Risk Acceptable
    {
        "id": "horizon_risk_long",
        "priority": 80,
        "condition": {"horizon": "long"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["medium", "high"],
            "explanation": (
                "Un horizon long terme permet d'absorber les variations du marché et "
                "de viser une croissance plus ambitieuse."
            ),
            "confidence": "medium"
        }
    },
    
    # ========== GOAL → HORIZON RULES ==========
    # Rule 3: Retirement Goal → Long Horizon
    {
        "id": "goal_retirement_horizon",
        "priority": 75,
        "condition": {"investment_goal": "retirement"},
        "suggestion": {
            "field": "horizon",
            "suggested_values": ["long"],
            "explanation": (
                "La préparation de la retraite s'inscrit naturellement dans le long terme. "
                "Les investisseurs choisissent souvent un horizon de plus de 8 ans "
                "pour bénéficier de l'effet du temps sur les rendements."
            ),
            "confidence": "high"
        }
    },
    
    # Rule 4: Project Goal → Short/Medium Horizon
    {
        "id": "goal_project_horizon",
        "priority": 75,
        "condition": {"investment_goal": "project"},
        "suggestion": {
            "field": "horizon",
            "suggested_values": ["short", "medium"],
            "explanation": (
                "Les projets immobiliers ou personnels ont souvent une échéance précise. "
                "Les investisseurs choisissent généralement un horizon court à moyen terme "
                "pour s'assurer que les fonds soient disponibles au moment voulu."
            ),
            "confidence": "medium"
        }
    },
    
    # Rule 4b: Safety Goal → Short/Medium Horizon (Pedagogical coupling)
    {
        "id": "goal_safety_horizon",
        "priority": 75,
        "condition": {"investment_goal": "safety"},
        "suggestion": {
            "field": "horizon",
            "suggested_values": ["short", "medium"],
            "explanation": (
                "Un objectif de préservation du capital est généralement associé "
                "à un horizon court à moyen terme, car un horizon plus long expose "
                "davantage aux fluctuations du marché."
            ),
            "confidence": "high"
        }
    },
    
    # Rule 4c: Wealth Growth → Medium/Long Horizon (Pedagogical coupling)
    {
        "id": "goal_growth_horizon",
        "priority": 75,
        "condition": {"investment_goal": "wealth_growth"},
        "suggestion": {
            "field": "horizon",
            "suggested_values": ["medium", "long"],
            "explanation": (
                "La croissance du capital se construit dans la durée. "
                "Un horizon moyen à long terme permet de traverser les cycles "
                "de marché et de capter le potentiel de performance."
            ),
            "confidence": "medium"
        }
    },
    
    # ========== AMOUNT RULES ==========
    # Rule 5: Small Amount → Concentrated Portfolio (SIGNAL)
    {
        "id": "amount_small_concentration",
        "priority": 8,
        "condition": {"investment_amount": ["under_100", "100_to_500"]},
        "suggestion": {
            "field": "portfolio_structure",
            "suggested_values": ["prefer_concentration"],
            "explanation": (
                "Pour débuter avec un petit montant, un portefeuille concentré sur "
                "quelques positions solides est plus facile à comprendre et à gérer."
            ),
            "confidence": "medium"
        }
    },
    
    # Rule 6: Large Amount → Diversification
    {
        "id": "amount_large_diversification",
        "priority": 8,
        "condition": {"investment_amount": "over_1000"},
        "suggestion": {
            "field": "portfolio_structure",
            "suggested_values": ["prefer_diversification"],
            "explanation": (
                "Avec ce montant, vous pouvez bénéficier d'une meilleure diversification "
                "pour répartir les risques sur plusieurs positions."
            ),
            "confidence": "medium"
        }
    },
    
    # ========== PRIORITY 60: KNOWLEDGE/EXPERIENCE → RISK RULES (MiFID II: Fourth Priority) ==========
    # Rule 7: Novice → Lower Risk (Reassuring Tone)
    {
        "id": "knowledge_novice_risk",
        "priority": 60,
        "condition": {"knowledge_level": "novice"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["low", "medium"],
            "explanation": (
                "En tant que novice, il est souvent préférable de commencer par une tolérance "
                "au risque limitée pour vous familiariser sereinement avec les marchés."
            ),
            "confidence": "high"
        }
    },
    
    # Rule 7b: Intermediate → Balanced Risk
    {
        "id": "knowledge_intermediate_risk",
        "priority": 60,
        "condition": {"knowledge_level": "intermediate"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["medium"],
            "explanation": (
                "Votre profil intermédiaire est bien adapté à un risque modéré, "
                "offrant un équilibre entre sécurité et potentiel de rendement."
            ),
            "confidence": "medium"
        }
    },
    
    # Rule 8: No Experience → Lower Risk
    {
        "id": "experience_none_risk",
        "priority": 60,
        "condition": {"experience": "none"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["low"],
            "explanation": (
                "Sans expérience préalable, un risque faible est recommandé pour "
                "commencer en douceur et apprendre les mécanismes de l'investissement."
            ),
            "confidence": "high"
        }
    },
    
    # ========== PRIORITY 70: GOAL → RISK RULES (MiFID II: Third Priority) ==========
    # Rule 9: Safety Goal → Low Risk
    {
        "id": "goal_safety_risk",
        "priority": 70,
        "condition": {"investment_goal": "safety"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["low"],
            "explanation": (
                "Pour préserver votre capital, un risque faible est cohérent avec "
                "votre objectif de sécurité."
            ),
            "confidence": "high"
        }
    },
    
    # Rule 10: Wealth Growth Goal → Medium/High Risk
    {
        "id": "goal_growth_risk",
        "priority": 70,
        "condition": {"investment_goal": "wealth_growth"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["medium", "high"],
            "explanation": (
                "Pour faire croître votre capital, un niveau de risque modéré à élevé "
                "permet de viser une meilleure performance."
            ),
            "confidence": "medium"
        }
    },
    
    # ========== MODE → HORIZON RULES (INVALID: 7 -> 3) ==========
    # REMOVED: mode_recurring_horizon (Retroactive)
    
    # ========== PRIORITY 100: LOSS CAPACITY → RISK RULES (MIFID II: DOMINATES ALL) ==========
    # Rule 12: No Loss Capacity → Low Risk ONLY
    {
        "id": "loss_none_risk",
        "priority": 100, # HIGHEST: MiFID II Compliance - Loss Capacity Dominates
        "condition": {"loss_capacity": "none"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["low"],
            "explanation": (
                "Sans capacité de perte, seul un risque faible est approprié. "
                "Tout niveau supérieur pourrait compromettre votre capital."
            ),
            "confidence": "high"
        }
    },
    
    # Rule 12b: Small Loss Capacity → Low or Medium Risk
    {
        "id": "loss_small_risk",
        "priority": 100,
        "condition": {"loss_capacity": "small"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["low", "medium"],
            "explanation": (
                "Avec une capacité de perte faible (< 10%), un risque limité "
                "est recommandé pour protéger votre capital."
            ),
            "confidence": "high"
        }
    },

    # Rule 12c: Medium Loss Capacity → Medium Risk MAX  ← WAS MISSING
    {
        "id": "loss_medium_risk",
        "priority": 100,
        "condition": {"loss_capacity": "medium"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["medium"],
            "explanation": (
                "Avec une capacité de perte moyenne (10-25%), un risque modéré "
                "est le niveau maximum recommandé pour rester dans vos limites financières."
            ),
            "confidence": "high"
        }
    },

    
    # Rule 13: High Loss Capacity → Higher Risk OK
    {
        "id": "loss_high_risk",
        "priority": 100,
        "condition": {"loss_capacity": "high"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["medium", "high"],
            "explanation": (
                "Votre capacité à absorber des pertes significatives (> 25%) "
                "vous permet d'envisager un profil de risque plus dynamique, "
                "si cela correspond à vos objectifs."
            ),
            "confidence": "medium"
        }
    },
    
    # Rule 14: Expert → High Risk Possible (Performance Tone)
    {
        "id": "knowledge_expert_risk",
        "priority": 60,
        "condition": {"knowledge_level": "expert"},
        "suggestion": {
            "field": "risk_tolerance",
            "suggested_values": ["high"],
            "explanation": (
                "Grâce à votre expertise technique, vous disposez de la connaissance "
                "nécessaire pour viser des stratégies de performance plus dynamiques."
            ),
            "confidence": "low"
        }
    },
    
    # ========== HORIZON → GOAL SUGGESTIONS (INVALID: 3 -> 2) ==========
    # REMOVED: horizon_short_goal (Retroactive)
    # REMOVED: horizon_long_goal (Retroactive)
    
    # ========== REMOVED RULES ==========
    # amount_small_risk_high: REMOVED (retroactive after reorder: amount[6] → risk[5])
    # The field order change (amount now after risk) makes this structurally invalid.
    
    # NOTE: Retroactive rules (e.g., Horizon → Goal, Risk → Goal, Amount → Risk) are 
    # structurally blocked by the Suggestion Engine to ensure pedagogical flow.
]


def compute_max_allowed_risk(profile: dict) -> str:
    """
    Compute maximum allowed risk based on MiFID II regulatory priority.
    
    Priority hierarchy:
    1. loss_capacity (DOMINATES - hard cap)
    2. horizon
    3. investment_goal
    4. knowledge_level/experience
    
    Args:
        profile: Dictionary with keys like loss_capacity, horizon, knowledge_level
        
    Returns:
        Maximum allowed risk level: "low", "medium", or "high"
    """
    loss_capacity = profile.get("loss_capacity", "")
    horizon = profile.get("horizon", "")
    knowledge_level = profile.get("knowledge_level", "")
    
    # PRIORITY 1: Loss Capacity (HARD CAP - MiFID II Compliance)
    # Values match HTML dropdown: none, small, medium, high
    if loss_capacity == "none":
        return "low"  # CANNOT go above - regulatory requirement
    elif loss_capacity in ("small", "medium"):
        # Small (< 10%) or Medium (10-25%) capacity
        # Can go to medium by default
        # Or high ONLY if long horizon + expert (exceptional case)
        if horizon == "long" and knowledge_level == "expert":
            return "high"
        return "medium"
    elif loss_capacity == "high":
        return "high"  # Significant capacity (> 25%) - no restriction
    
    # Default: medium (conservative approach if loss_capacity not specified)
    return "medium"

def get_all_rules() -> List[Dict[str, Any]]:
    """
    Get all suggestion rules.
    
    Returns:
        List of all rule definitions
    """
    return SUGGESTION_RULES

def get_rules_version() -> str:
    """
    Get current rules version for audit trail.
    
    Returns:
        Version string
    """
    return RULES_VERSION
