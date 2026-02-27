"""Rule-based explanation engine for portfolio assets (MiFID II compliant)."""
from typing import Dict, List

def explain_asset(asset: Dict) -> Dict[str, str]:
    """
    Generate a differentiated, non-expert-friendly explanation for an asset.
    Differentiates based on role (Core/Secondary/Diversification) and type.
    """
    ticker = asset['ticker']
    name = asset['name']
    asset_type = asset['asset_type']
    asset_class = asset['asset_class']
    volatility = asset['volatility']
    weight = asset['weight']
    is_esg = asset.get('is_esg', False)
    
    # 0. ROLE CLASSIFICATION
    if weight >= 0.50:
        role_label = "conviction"
        role_intro = f"Cette position de forte conviction ({round(weight*100)}%) est le moteur principal de votre performance attendue."
    elif weight > 0.20:
        role_label = "core"
        role_intro = f"Cette position centrale ({round(weight*100)}%) constitue l'un des piliers de votre stratégie."
    elif weight > 0.10:
        role_label = "secondary"
        role_intro = f"Cet actif ({round(weight*100)}%) contribue à l'équilibre et à la performance de votre portefeuille."
    else:
        role_label = "diversification"
        role_intro = f"Cette position de diversification ({round(weight*100)}%) complète votre portefeuille en répartissant les risques."

    # A. IDENTIFICATION
    if 'US' in asset_class: region = "américaine"
    elif 'Europe' in asset_class: region = "européenne"
    elif 'Emerging' in asset_class: region = "des marchés émergents"
    else: region = "internationale"
    
    if asset_type == "ETF":
        type_desc = f"un panier d'actifs diversifiés (ETF) {region}"
    else:
        type_desc = f"une entreprise technologique {region}" if ticker in ['AAPL', 'MSFT', 'GOOGL', 'NVDA'] else f"une entreprise leader {region}"
    
    identification = f"{name} ({ticker}) – Il s'agit d'un investissement dans {type_desc}."
    
    # B. RELIABILITY
    if asset_type == "ETF":
        reliability = "Il permet d'accéder à des centaines de titres en une seule fois, ce qui sécurise votre investissement par une large diversification."
    else:
        reliability = f"C'est un acteur majeur de l'économie {region}, choisi pour sa solidité financière et sa visibilité sur le marché."
    
    if is_esg:
        reliability += " Cet actif respecte des critères de responsabilité sociale et environnementale (ESG)."
    
    # C. ROLE & WEIGHT REASONING
    if 'Bond' in asset_class:
        reasoning = "Sa présence vise à stabiliser votre capital, surtout en période de baisse des marchés."
    elif volatility > 0.35:
        reasoning = "Malgré sa volatilité, il a été sélectionné pour son potentiel de croissance à long terme."
    else:
        reasoning = "C'est un compromis optimal entre risque modéré et rendement attendu."

    # Final Role text combining intro and reasoning
    role_full = f"{role_intro} {reasoning}"
    
    return {
        "identification": identification,
        "reliability": reliability,
        "role": role_full
    }

def explain_portfolio(profile: Dict, positions: List[Dict], category_allocations: Dict) -> str:
    """
    Generate a global portfolio explanation that is 100% coherent with user's inputs.
    
    Args:
        profile: User's risk profile, horizon, and goal
        positions: List of portfolio positions
        category_allocations: Dict with equities/bonds allocation
    
    Returns:
        A coherent, contextual explanation based on actual user inputs
    """
    risk_profile = profile.get('risk_profile', 'Équilibré')
    horizon = profile.get('horizon', 'medium')
    goal = profile.get('goal', 'wealth_growth')
    num_positions = len(positions)
    equity_pct = round(category_allocations.get('equities', 0.6) * 100)
    bond_pct = round(category_allocations.get('bonds', 0.4) * 100)
    
    # Horizon-based intro (MOST IMPORTANT FOR COHERENCE)
    if horizon == 'short':
        horizon_text = "court terme"
        time_adapted = "adapté à votre horizon de moins de 3 ans"
    elif horizon == 'medium':
        horizon_text = "moyen terme"
        time_adapted = "calibré pour un horizon de 3 à 8 ans"
    else:  # long
        horizon_text = "long terme"
        time_adapted = "optimisé pour un horizon de plus de 8 ans"
    
    # Goal-based intro
    if goal == 'retirement':
        goal_text = "préparer votre retraite"
    elif goal == 'wealth_growth':
        goal_text = "faire croître votre capital"
    elif goal == 'project':
        goal_text = "financer votre projet"
    else:  # safety
        goal_text = "préserver votre capital"
    
    # Risk-based strategy
    if risk_profile == "Prudent":
        risk_text = "privilégier la sécurité et limiter les variations"
    elif risk_profile == "Équilibré":
        risk_text = "équilibrer croissance et sécurité"
    else:  # Dynamique
        risk_text = "maximiser le potentiel de croissance"
    
    # Compose coherent intro
    intro = f"Votre portefeuille est conçu pour {goal_text} sur {horizon_text}, en cherchant à {risk_text}. "
    
    # Allocation strategy
    strategy = f"Il est composé de {equity_pct}% d'actifs de croissance et {bond_pct}% d'obligations, {time_adapted}."
    
    # Diversification
    diversification = f" Il contient {num_positions} positions soigneusement sélectionnées pour répartir les risques entre différents secteurs et zones géographiques."
    
    # Reassurance
    reassurance = " Chaque actif a été choisi en fonction de sa fiabilité et de son rôle dans votre stratégie. Les pondérations sont calibrées pour maîtriser le risque global."
    
    return f"{intro}{strategy}{diversification}{reassurance}"
