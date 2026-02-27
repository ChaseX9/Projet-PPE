"""
Suggestion engine for smart questionnaire guidance.

Evaluates rules and generates contextual suggestions based on user responses.
Designed for transparency, auditability, and MiFID II compliance.
"""
from typing import Dict, List, Any, Optional
from .suggestion_rules import get_all_rules, get_rules_version, FIELD_ORDER


class Suggestion:
    """Represents a single suggestion for the user."""
    
    def __init__(
        self,
        rule_id: str,
        field: str,
        suggested_values: List[str],
        explanation: str,
        confidence: str,
        current_value: Optional[str] = None
    ):
        self.rule_id = rule_id
        self.field = field
        self.suggested_values = suggested_values
        self.explanation = explanation
        self.confidence = confidence
        self.current_value = current_value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "rule_id": self.rule_id,
            "field": self.field,
            "suggested_values": self.suggested_values,
            "explanation": self.explanation,
            "confidence": self.confidence,
            "current_value": self.current_value
        }
    
    def is_followed(self) -> bool:
        """Check if the current value matches the suggestion."""
        if self.current_value is None:
            return False
        return self.current_value in self.suggested_values


def _matches_condition(condition: Dict[str, Any], responses: Dict[str, Any]) -> bool:
    """
    Check if user responses match a rule's condition.
    
    Args:
        condition: Rule condition dict
        responses: User's current responses
        
    Returns:
        True if all conditions are met
    """
    for field, expected_value in condition.items():
        actual_value = responses.get(field)
        
        # Handle list of acceptable values
        if isinstance(expected_value, list):
            if actual_value not in expected_value:
                return False
        else:
            if actual_value != expected_value:
                return False
    
    return True


def evaluate_suggestions(responses: Dict[str, Any]) -> List[Suggestion]:
    """
    Evaluate all rules and return applicable suggestions.
    
    Args:
        responses: User's current questionnaire responses
        
    Returns:
        List of applicable suggestions, sorted by priority
    """
    rules = get_all_rules()
    suggestions = []
    
    # Sort rules by priority (highest first)
    sorted_rules = sorted(rules, key=lambda r: r.get('priority', 0), reverse=True)
    
    for rule in sorted_rules:
        # STRUCTURAL PROTECTION: Enforce unidirectional flow
        target_field = rule['suggestion']['field']
        target_order = FIELD_ORDER.get(target_field, 99)
        
        is_retroactive = False
        for cond_field in rule['condition'].keys():
            cond_order = FIELD_ORDER.get(cond_field, 0)
            if target_order <= cond_order:
                is_retroactive = True
                break
        
        if is_retroactive:
            continue
            
        # Check if condition matches
        if _matches_condition(rule['condition'], responses):
            suggestion_data = rule['suggestion']
            field = suggestion_data['field']
            current_value = responses.get(field)
            
            # Create suggestion object
            suggestion = Suggestion(
                rule_id=rule['id'],
                field=field,
                suggested_values=suggestion_data['suggested_values'],
                explanation=suggestion_data['explanation'],
                confidence=suggestion_data['confidence'],
                current_value=current_value
            )
            
            suggestions.append(suggestion)
    
    return suggestions


def calculate_coherence_score(responses: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate overall coherence of the profile.
    
    This is NOT a "grade" but a pedagogical indicator.
    
    Args:
        responses: User's current questionnaire responses
        
    Returns:
        Dict with:
            - status: "excellent" | "good" | "needs_reflection"
            - message: User-friendly message (always pedagogical, never judgmental)
            - followed_count: Number of suggestions followed
            - total_count: Total number of applicable suggestions
    """
    suggestions = evaluate_suggestions(responses)
    
    if not suggestions:
        return {
            "status": "excellent",
            "message": "Profil très cohérent",
            "followed_count": 0,
            "total_count": 0
        }
    
    followed = sum(1 for s in suggestions if s.is_followed())
    total = len(suggestions)
    ratio = followed / total if total > 0 else 1.0
    
    # Pedagogical thresholds (not judgmental)
    if ratio >= 0.8:
        status = "excellent"
        message = "Profil très cohérent"
    elif ratio >= 0.5:
        status = "good"
        message = "Profil cohérent"
    else:
        status = "needs_reflection"
        # NEVER use negative language like "mauvais" or "incohérent"
        message = "Certaines réponses méritent réflexion"
    
    return {
        "status": status,
        "message": message,
        "followed_count": followed,
        "total_count": total
    }


def get_suggestions_for_field(field: str, responses: Dict[str, Any]) -> List[Suggestion]:
    """
    Get suggestions specifically for a given field.
    
    Args:
        field: Target field name
        responses: User's current responses
        
    Returns:
        List of suggestions for that field
    """
    all_suggestions = evaluate_suggestions(responses)
    return [s for s in all_suggestions if s.field == field]
