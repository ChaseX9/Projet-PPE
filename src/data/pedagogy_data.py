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
    "VWCE.DE": {
        "pedagogy_short": "L'un des ETF les plus diversifiés au monde, couvrant plus de 3 700 entreprises.",
        "pedagogy_long": "Le Vanguard FTSE All-World est la référence ultime pour un investissement passif global. Il inclut des entreprises de pays développés ET émergents, ce qui en fait un outil 'tout-en-un' pour une diversification géographique totale.",
        "utility": "Socle de portefeuille. Diversification mondiale incluant les pays émergents.",
        "suitable_profiles": ["Prudent", "Équilibré", "Dynamique"],
        "why_capinvest": "Frais bas (0.22%), réplication physique, ultra-diversifié.",
        "key_takeaways": [
            "Exposition mondiale (Développés + Émergents)",
            "Réplication physique très précise",
            "Idéal pour un investissement de long terme"
        ]
    },
    "IWDA.AS": {
        "pedagogy_short": "Exposition aux 1 500 plus grandes entreprises des pays développés.",
        "pedagogy_long": "L'iShares Core MSCI World est l'un des plus gros ETF au monde. Il permet d'investir dans les 23 pays les plus développés (USA, Europe, Japon, etc.). Contrairement au All-World, il n'inclut pas les pays émergents.",
        "utility": "Cœur de portefeuille solide sur les marchés stables et matures.",
        "suitable_profiles": ["Prudent", "Équilibré", "Dynamique"],
        "why_capinvest": "Liquidité exceptionnelle, frais minimes, leader mondial du marché.",
        "key_takeaways": [
            "Focus sur les pays développés",
            "Grande stabilité historique",
            "Excellente liquidité"
        ]
    },
    "INDA": {
        "pedagogy_short": "Accédez à la croissance fulgurante de l'économie Indienne.",
        "pedagogy_long": "L'iShares MSCI India permet de s'exposer aux plus grandes capitalisations en Inde. C'est un marché émergent à forte croissance mais avec une volatilité plus élevée que les marchés développés.",
        "utility": "Satellite de portefeuille pour booster la performance via les émergents.",
        "suitable_profiles": ["Dynamique"],
        "why_capinvest": "Leader sur l'exposition indienne, diversification hors Chine/USA.",
        "key_takeaways": [
            "Potentiel de croissance élevé",
            "Diversification géographique spécifique",
            "Risque/Volatilité plus importants"
        ]
    },
    "MCHI": {
        "pedagogy_short": "Investissez dans les géants technologiques et industriels Chinois.",
        "pedagogy_long": "Cet ETF iShares cible les plus grandes entreprises chinoises (Tencent, Alibaba, Meituan). La Chine est la 2ème puissance mondiale, offrant une diversification indispensable mais soumise à des risques politiques particuliers.",
        "utility": "Exposition tactique sur la deuxième économie mondiale.",
        "suitable_profiles": ["Dynamique"],
        "why_capinvest": "Exposition directe et liquide aux leaders chinois.",
        "key_takeaways": [
            "Accès aux leaders de la Tech chinoise",
            "Deuxième puissance mondiale",
            "Volatilité politique et économique"
        ]
    },
    "AGG": {
        "pedagogy_short": "Le socle de sécurité pour votre poche obligataire.",
        "pedagogy_long": "L'iShares Core U.S. Aggregate Bond est l'un des outils de référence pour la sécurité. Il regroupe des milliers d'obligations d'État et d'entreprises de haute qualité, offrant stabilité et revenus réguliers.",
        "utility": "Protection du capital et réduction de la volatilité globale du portefeuille.",
        "suitable_profiles": ["Prudent", "Équilibré"],
        "why_capinvest": "Faible risque, revenus réguliers, excellent stabilisateur.",
        "key_takeaways": [
            "Sécurité du capital",
            "Faible volatilité",
            "Revenu régulier via les coupons"
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

def generate_fallback_pedagogy(ticker: str, name: str, asset_type: str, zone: str, volatility_level: str) -> dict:
    """Generate an intelligent fallback pedagogical description."""
    is_etf = asset_type.upper() == "ETF"
    
    # Improved zone detection for Global/World assets often misclassified by exchange
    effective_zone = zone
    if is_etf:
        global_keywords = ["World", "All-World", "Global", "ACWI", "Total World"]
        if any(kw.lower() in name.lower() for kw in global_keywords):
            effective_zone = "Global"
    
    # Base description
    if is_etf:
        desc = f"Cet ETF permet d'investir dans un panier diversifié d'actifs situés en zone {effective_zone}."
        utility = "Outil de diversification permettant d'accéder à un marché entier en une fois."
        takeaways = [
            f"Exposition groupée ({effective_zone})",
            "Frais réduits par rapport à la gestion active",
            "Liquidité assurée par la structure ETF"
        ]
    else:
        desc = f"Cette action représente une part du capital d'une entreprise majeure de la zone {effective_zone}."
        utility = "Recherche de performance ciblée sur un leader de son secteur."
        takeaways = [
            f"Investissement direct ({effective_zone})",
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

def get_asset_pedagogy(ticker: str, name: str, asset_type: str, zone: str, volatility_level: str) -> dict:
    """Get pedagogical data with smart fallback."""
    if ticker in PEDAGOGY_DATA:
        return PEDAGOGY_DATA[ticker]
    
    return generate_fallback_pedagogy(ticker, name, asset_type, zone, volatility_level)
