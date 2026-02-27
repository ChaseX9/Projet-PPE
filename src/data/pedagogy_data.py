"""Pedagogical data for the Investment Library (Explorer)."""

PEDAGOGY_DATA = {
    # --- ETFs (Global / World) ---
    "VT": {
        "pedagogy_short": "Exposition ultime : plus de 9 000 entreprises du monde entier en une seule ligne.",
        "pedagogy_long": "Le Vanguard Total World Stock est l'outil de référence pour capturer la croissance mondiale. Il investit dans pratiquement toutes les entreprises cotées au monde, des géants de la Tech US aux leaders industriels japonais.",
        "utility": "Cœur de portefeuille. Diversification maximale géographique et sectorielle.",
        "suitable_profiles": ["Prudent", "Équilibré", "Dynamique"],
        "why_capinvest": "Frais extrêmement bas, liquidité parfaite, recommandé par la plupart des académiques.",
        "key_takeaways": [
            "Diversification mondiale complète",
            "Frais de gestion minimaux",
            "Stabilité grâce à la dilution du risque"
        ]
    },
    "CW8.PA": {
        "pedagogy_short": "L'outil favori des investisseurs européens pour s'exposer aux 1 500 plus grandes entreprises mondiales.",
        "pedagogy_long": "Cet ETF Amundi suit l'indice MSCI World. Il est particulièrement prisé en France car il permet d'exposer son PEA aux plus grandes capitalisations mondiales (Apple, Microsoft, LVMH, etc.) avec une fiscalité avantageuse.",
        "utility": "Performance historique solide tirée par les leaders mondiaux.",
        "suitable_profiles": ["Équilibré", "Dynamique"],
        "why_capinvest": "Éligible au PEA, géré par Amundi (leader européen), excellente réplication de l'indice.",
        "key_takeaways": [
            "Accès aux leaders mondiaux",
            "Éligible au PEA",
            "Moteur de performance long terme"
        ]
    },
    
    # --- Stocks (US) ---
    "AAPL": {
        "pedagogy_short": "Leader mondial de l'électronique grand public et des services numériques.",
        "pedagogy_long": "Apple n'est plus seulement un fabricant d'iPhone, c'est un écosystème de services (Cloud, Musique, Paiements) générant des revenus récurrents massifs. C'est l'une des entreprises les plus rentables de l'histoire.",
        "utility": "Croissance solide soutenue par une marque forte et un écosystème captif.",
        "suitable_profiles": ["Équilibré", "Dynamique"],
        "why_capinvest": "Position de cash dominante, barrières à l'entrée élevées, historique de dividendes croissants.",
        "key_takeaways": [
            "Marque la plus puissante au monde",
            "Revenus services très réguliers",
            "Solidité financière exceptionnelle"
        ]
    },
}

def generate_fallback_pedagogy(ticker: str, asset_type: str, zone: str, volatility_level: str) -> dict:
    """Generate an intelligent fallback pedagogical description."""
    is_etf = asset_type.upper() == "ETF"
    
    # Base description
    if is_etf:
        desc = f"Cet ETF permet d'investir dans un panier diversifié d'actifs situés en zone {zone}."
        utility = "Outil de diversification permettant d'accéder à un marché entier en une fois."
        takeaways = [
            f"Exposition groupée ({zone})",
            "Frais réduits par rapport à la gestion active",
            "Liquidité assurée par la structure ETF"
        ]
    else:
        desc = f"Cette action représente une part du capital d'une entreprise majeure de la zone {zone}."
        utility = "Recherche de performance ciblée sur un leader de son secteur."
        takeaways = [
            f"Investissement direct ({zone})",
            "Sensibilité aux performances de l'entreprise",
            "Potentiel de dividendes ou croissance"
        ]

    # Adjust based on volatility
    if volatility_level == "Faible":
        desc += " Son comportement historique est relativement stable, ce qui en fait un socle prudent."
        profiles = ["Prudent", "Équilibré"]
    elif volatility_level == "Élevé":
        desc += " Sa volatilité est importante, ce qui nécessite un horizon de long terme pour lisser les risques."
        profiles = ["Dynamique"]
    else:
        desc += " Il présente un équilibre entre recherche de rendement et risque maîtrisé."
        profiles = ["Équilibré", "Dynamique"]

    return {
        "pedagogy_short": desc if len(desc) < 100 else desc[:97] + "...",
        "pedagogy_long": desc,
        "utility": utility,
        "suitable_profiles": profiles,
        "why_capinvest": "Sélectionné pour sa liquidité et sa représentativité du marché ciblé.",
        "key_takeaways": takeaways
    }

def get_asset_pedagogy(ticker: str, asset_type: str, zone: str, volatility_level: str) -> dict:
    """Get pedagogical data with smart fallback."""
    if ticker in PEDAGOGY_DATA:
        return PEDAGOGY_DATA[ticker]
    
    return generate_fallback_pedagogy(ticker, asset_type, zone, volatility_level)
