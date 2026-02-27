"""Utility for seeding the CapInvest Academy curriculum."""
from sqlalchemy.orm import Session
from .models import Module, Lesson, Question

def auto_seed_if_empty(db: Session):
    """Seed the curriculum only if no modules exist."""
    if db.query(Module).count() > 0:
        return False
        
    print("🌱 Database empty. Seeding full curriculum...")
    
    MODULES = [
        {
            "title": "Les bases de l'investissement",
            "description": "Découvrez les fondamentaux pour bien débuter votre parcours d'investisseur",
            "level": "beginner",
            "order": 1,
            "icon": "🎯",
            "lessons": [
                {
                    "title": "Qu'est-ce qu'investir ?",
                    "content": """Investir, c'est mettre votre argent au travail pour générer des revenus futurs. C'est l'un des outils les plus puissants pour construire votre patrimoine sur le long terme.

**Pourquoi investir plutôt qu'épargner ?**

L'épargne classique (livret A, compte courant) est sécurisée mais souffre d'un ennemi silencieux : l'inflation. Si votre livret rapporte 3% et que l'inflation est à 4%, vous perdez en réalité 1% de pouvoir d'achat chaque année. Investir permet de viser des rendements supérieurs à l'inflation.

**Les trois piliers fondamentaux**

• **Le capital** : c'est l'argent que vous mettez en jeu. Plus vous investissez tôt et régulièrement, plus les effets des intérêts composés seront puissants.

• **Le rendement** : c'est le gain que vous espérez réaliser, exprimé en pourcentage annuel. Un rendement de 7% par an double votre capital en 10 ans (règle des 72).

• **Le risque** : c'est la possibilité de perdre une partie ou la totalité de votre capital. Il est impossible d'éliminer totalement le risque, mais on peut le gérer intelligemment.

**La règle des 72**

Pour estimer combien de temps il faut pour doubler votre capital, divisez 72 par le taux de rendement annuel. Exemple : à 6% par an, votre capital double en 72/6 = 12 ans.

**Quand commencer ?**

Le meilleur moment pour commencer à investir, c'est maintenant. Le temps est votre meilleur allié grâce aux intérêts composés. 100€ investis à 7% par an deviennent :
- 197€ après 10 ans
- 387€ après 20 ans
- 762€ après 30 ans

**Les différentes formes d'investissement**

Il existe de nombreuses façons d'investir : actions en bourse, obligations, immobilier, fonds d'investissement (ETF), assurance-vie, PEA... Chaque véhicule a ses avantages, ses risques et sa fiscalité propre. Nous les étudierons en détail dans les modules suivants.""",
                    "example": "Marie a 25 ans et investit 200€ par mois dans un ETF World avec un rendement historique de 7% par an. À 65 ans, elle aura investi 96 000€ au total mais son capital sera de 525 000€ grâce aux intérêts composés. Son voisin Paul commence à 35 ans avec le même effort mensuel : il n'aura que 243 000€ à 65 ans. Ces 10 ans de différence lui ont coûté 282 000€ !",
                    "estimated_minutes": 10,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quelle est la principale différence entre épargner et investir ?",
                            "choices": ["Le montant minimum requis", "Le niveau de risque et le potentiel de rendement", "La durée de placement obligatoire", "Le type de banque utilisée"],
                            "correct_answer": "Le niveau de risque et le potentiel de rendement",
                            "explanation": "L'épargne privilégie la sécurité du capital avec un rendement limité, tandis que l'investissement accepte un risque en échange d'un rendement potentiellement supérieur à l'inflation."
                        },
                        {
                            "type": "multiple_choice",
                            "prompt": "Selon la règle des 72, combien de temps faut-il pour doubler son capital à un taux de 8% par an ?",
                            "choices": ["8 ans", "9 ans", "10 ans", "12 ans"],
                            "correct_answer": "9 ans",
                            "explanation": "La règle des 72 : 72 / 8 = 9 ans. C'est une approximation rapide très utile pour estimer la croissance de son capital."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Investir garantit toujours un gain supérieur à l'épargne classique.",
                            "choices": None,
                            "correct_answer": "false",
                            "explanation": "Faux. L'investissement comporte des risques et peut entraîner des pertes, surtout à court terme. C'est pourquoi l'horizon de placement et la diversification sont essentiels."
                        }
                    ]
                },
                {
                    "title": "Risque et rendement : le couple fondamental",
                    "content": """La relation entre risque et rendement est la loi fondamentale de la finance. Comprendre ce principe est essentiel pour prendre de bonnes décisions d'investissement.

**Le principe de base**

Plus le rendement potentiel est élevé, plus le risque est important. Il n'existe pas de rendement élevé sans risque. Si quelqu'un vous promet un rendement de 20% par an sans risque, c'est une arnaque.

**La classification des actifs par niveau de risque**

De moins risqué à plus risqué :

1. **Livrets réglementés** (Livret A, LDDS) : risque quasi-nul, capital garanti par l'État, rendement actuel ~3%

2. **Fonds euros d'assurance-vie** : capital garanti par l'assureur, rendement ~2-3%

3. **Obligations d'État** (OAT françaises, Bunds allemands) : risque très faible, rendement ~3-4%

4. **Obligations d'entreprises** (investment grade) : risque modéré, rendement ~4-6%

5. **Actions de grandes entreprises** (CAC40, S&P500) : risque modéré à élevé, rendement historique ~7-10% par an sur le long terme

6. **Small caps et marchés émergents** : risque élevé, rendement potentiel plus élevé

7. **Cryptomonnaies, start-ups, options** : risque très élevé, rendement potentiel très élevé ou perte totale

**Comment mesurer le risque ?**

La volatilité est la mesure standard du risque. Elle indique l'amplitude des variations de prix. Un actif très volatil peut gagner ou perdre 30% en quelques mois. Un actif peu volatil fluctue peu.

**La notion de risque acceptable**

Votre tolérance au risque dépend de :
- Votre horizon de placement (plus c'est long, plus vous pouvez prendre de risques)
- Votre situation financière (n'investissez jamais de l'argent dont vous avez besoin à court terme)
- Votre psychologie (pouvez-vous dormir si votre portefeuille baisse de 30% ?)

**Le risque diminue avec le temps**

Sur 1 an, les actions peuvent perdre 40%. Sur 20 ans, elles n'ont jamais été négatives sur les marchés développés. Le temps est le meilleur antidote au risque.""",
                    "example": "En 2022, les marchés actions ont chuté de 15 à 25%. Un investisseur qui avait besoin de son argent cette année-là a subi une perte réelle. Un investisseur avec un horizon de 20 ans a simplement attendu la remontée (qui a eu lieu en 2023 avec +20%). C'est pourquoi on dit : n'investissez en bourse que l'argent dont vous n'avez pas besoin avant 5 à 10 ans.",
                    "estimated_minutes": 12,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quel actif présente généralement le risque le plus faible parmi les suivants ?",
                            "choices": ["Actions de start-ups", "Obligations d'État de pays développés", "Cryptomonnaies", "Actions de marchés émergents"],
                            "correct_answer": "Obligations d'État de pays développés",
                            "explanation": "Les obligations d'État des pays développés (France, Allemagne, USA) sont garanties par des États solvables et constituent l'investissement le moins risqué après les livrets réglementés."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Un placement sans risque peut offrir un rendement très élevé de façon durable.",
                            "choices": None,
                            "correct_answer": "false",
                            "explanation": "Faux. C'est le principe fondamental de la finance : pas de risque = pas de rendement élevé. Toute promesse de rendement élevé garanti est un signal d'alarme."
                        },
                        {
                            "type": "multiple_choice",
                            "prompt": "Pourquoi le risque des actions diminue-t-il avec un horizon de placement long ?",
                            "choices": ["Parce que les actions deviennent moins volatiles", "Parce qu'on a le temps d'attendre une remontée après une baisse", "Parce que les dividendes compensent les pertes", "Parce que la fiscalité est réduite"],
                            "correct_answer": "Parce qu'on a le temps d'attendre une remontée après une baisse",
                            "explanation": "Historiquement, les marchés actions ont toujours fini par remonter après une crise. Un horizon long permet de traverser les crises sans être forcé de vendre à perte."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Comprendre les actions",
            "description": "Maîtrisez le fonctionnement des actions et leur rôle dans un portefeuille",
            "level": "beginner",
            "order": 2,
            "icon": "📈",
            "lessons": [
                {
                    "title": "Qu'est-ce qu'une action ?",
                    "content": """Une action est un titre de propriété qui représente une fraction du capital d'une entreprise. En achetant une action, vous devenez actionnaire, c'est-à-dire copropriétaire de l'entreprise.

**Comment fonctionne le marché des actions ?**

Les entreprises émettent des actions pour lever des fonds (lors d'une introduction en bourse, ou IPO). Ces actions sont ensuite échangées sur des marchés boursiers (Euronext Paris, NYSE, NASDAQ...) entre investisseurs. Le prix d'une action fluctue en permanence selon l'offre et la demande.

**Les droits de l'actionnaire**

En tant qu'actionnaire, vous bénéficiez de plusieurs droits :

• **Droit aux dividendes** : une partie des bénéfices peut être redistribuée aux actionnaires. Ce n'est pas obligatoire et dépend de la politique de l'entreprise.

• **Droit de vote** : lors des assemblées générales, vous pouvez voter sur les grandes décisions de l'entreprise (nomination des dirigeants, stratégie...).

• **Droit à l'information** : les entreprises cotées sont obligées de publier leurs résultats financiers régulièrement.

• **Droit sur l'actif net** : en cas de liquidation de l'entreprise, vous avez droit à une part des actifs restants (après remboursement des créanciers).

**Les deux sources de gain**

1. **La plus-value** : vous achetez une action à 100€ et la revendez à 150€ = +50€ de gain.

2. **Les dividendes** : l'entreprise distribue une partie de ses bénéfices. Si elle verse 3€ par action et que vous en possédez 10, vous recevez 30€.

**Les risques spécifiques aux actions**

• **Risque de marché** : toutes les actions baissent lors d'une crise générale.
• **Risque spécifique** : l'entreprise peut mal performer ou faire faillite.
• **Risque de liquidité** : pour les petites entreprises, il peut être difficile de vendre rapidement.

**Comment lire une cotation boursière ?**

Quand vous voyez "LVMH : 750€ (+1,2%)", cela signifie que l'action LVMH vaut 750€ et a progressé de 1,2% dans la journée. Le volume d'échange indique combien d'actions ont été échangées.""",
                    "example": "Vous achetez 10 actions TotalEnergies à 60€ chacun, soit 600€ investis. Un an plus tard, l'action vaut 70€ (plus-value de 100€) et TotalEnergies a versé un dividende de 3€ par action (30€ de dividendes). Votre gain total est de 130€, soit un rendement de 21,7% sur l'année. Mais si TotalEnergies avait chuté à 50€, vous auriez perdu 100€ malgré les dividendes.",
                    "estimated_minutes": 12,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Que représente une action ?",
                            "choices": ["Une dynamique de dette", "Une part de propriété de l'entreprise", "Un prêt à court terme", "Une assurance perte"],
                            "correct_answer": "Une part de propriété de l'entreprise",
                            "explanation": "Une action est une fraction du capital d'une entreprise. En l'achetant, vous devenez copropriétaire et partagez les succès comme les difficultés de l'entreprise."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Les dividendes sont garantis et versés chaque année.",
                            "choices": None,
                            "correct_answer": "false",
                            "explanation": "Faux. Les dividendes sont décidés par le conseil d'administration et votés en assemblée générale. Ils peuvent être réduits, supprimés ou augmentés selon les résultats de l'entreprise."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Les ETF : investir simplement",
            "description": "Découvrez les fonds indiciels pour une diversification maximale à moindre coût",
            "level": "beginner",
            "order": 3,
            "icon": "📊",
            "lessons": [
                {
                    "title": "Qu'est-ce qu'un ETF ?",
                    "content": """Un ETF (Exchange Traded Fund), aussi appelé 'tracker', est un fonds d'investissement qui cherche à répliquer la performance d'un indice boursier, comme le CAC 40 ou le S&P 500.

**Le concept de gestion passive**

Contrairement aux fonds classiques où un gérant choisit des actions pour essayer de 'battre le marché' (gestion active), un ETF se contente de copier l'indice (gestion passive). C'est beaucoup plus simple et surtout beaucoup moins cher.

**Les avantages majeurs des ETF**

• **Diversification instantanée** : en achetant une seule part d'un ETF MSCI World, vous investissez indirectement dans plus de 1 500 entreprises à travers le monde.

• **Frais réduits** : les frais de gestion d'un ETF sont généralement de 0,1% à 0,5% par an, contre 1,5% à 2,5% pour les fonds bancaires classiques. Sur 20 ans, cette différence peut représenter des dizaines de milliers d'euros.

• **Transparence** : vous savez exactement ce qu'il y a dans votre ETF (la composition de l'indice).

• **Liquidité** : les ETF s'achètent et se vendent en bourse à tout moment de la journée, comme une action.

**Comment choisir un ETF ?**

1. **L'indice répliqué** : est-ce un indice large (Monde, USA, Europe) ou sectoriel (Tech, Santé) ?
2. **Les frais (TER)** : plus ils sont bas, mieux c'est.
3. **Le mode de réplication** : Physique (le fonds détient les actions) ou Synthétique (via un contrat financier).
4. **La politique de dividende** : Capitalisation (les dividendes sont réinvestis) ou Distribution (les dividendes vous sont versés).""",
                    "example": "Pour investir dans les 40 plus grandes entreprises françaises : 1) Acheter les 40 actions une par une (long, coûteux) ou 2) Acheter un seul ETF CAC 40 (rapide, diversification immédiate).",
                    "estimated_minutes": 10,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quel est le principal avantage de la gestion passive (ETF) par rapport à la gestion active ?",
                            "choices": ["Des frais beaucoup plus bas", "La garantie de ne jamais perdre d'argent", "Un gérant qui choisit les meilleures actions", "Une fiscalité nulle"],
                            "correct_answer": "Des frais beaucoup plus bas",
                            "explanation": "La gestion passive coûte beaucoup moins cher car elle ne nécessite pas une équipe de gérants pour analyser chaque entreprise. Cette économie de frais booste votre rendement net sur le long terme."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Un ETF permet d'investir dans des centaines d'entreprises en un seul achat.",
                            "choices": None,
                            "correct_answer": "true",
                            "explanation": "Vrai. C'est l'essence même de l'ETF : regrouper de nombreux titres pour offrir une diversification immédiate aux investisseurs."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Les Indices Boursiers",
            "description": "Apprenez à lire les baromètres de l'économie mondiale",
            "level": "beginner",
            "order": 4,
            "icon": "🏎️",
            "lessons": [
                {
                    "title": "Les grands indices mondiaux",
                    "content": """Un indice boursier est un indicateur de la performance d'un marché ou d'un secteur. Il sert de point de repère (benchmark) pour les investisseurs.

**Les indices incontournables**

• **S&P 500** : les 500 plus grandes entreprises américaines. C'est l'indice le plus suivi au monde.
• **MSCI World** : environ 1 500 entreprises de 23 pays développés. C'est la base de nombreux portefeuilles diversifiés.
• **NASDAQ 100** : les 100 plus grandes entreprises technologiques américaines (Apple, Microsoft, Google...).
• **CAC 40** : les 40 fleurons de l'économie française (LVMH, TotalEnergies, Sanofi...).
• **Euro Stoxx 50** : les 50 plus grandes entreprises de la zone euro.

**Comment sont calculés les indices ?**

La plupart des indices sont "pondérés par la capitalisation boursière". Cela signifie que plus une entreprise est grosse (valeur totale de ses actions), plus elle a de poids dans l'indice. Si Apple pèse 7% du S&P 500, ses variations de prix auront beaucoup plus d'impact que celles d'une petite entreprise pesant 0,01%.""",
                    "example": "Le CAC 40 n'est pas une simple moyenne des prix des 40 actions. LVMH a un poids beaucoup plus important que Renault. Si l'action LVMH monte de 5%, le CAC 40 montera beaucoup plus que si l'action Renault monte de 5%.",
                    "estimated_minutes": 10,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quel indice regroupe les 500 plus grandes entreprises américaines ?",
                            "choices": ["NASDAQ", "CAC 40", "S&P 500", "Nikkei 225"],
                            "correct_answer": "S&P 500",
                            "explanation": "Le Standard & Poor's 500 est considéré comme l'indicateur le plus représentatif du marché boursier américain et de l'économie mondiale."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Analyse Fondamentale",
            "description": "Apprenez à évaluer la valeur réelle d'une entreprise",
            "level": "intermediate",
            "order": 5,
            "icon": "🔍",
            "lessons": [
                {
                    "title": "Les piliers de l'analyse fondamentale",
                    "content": """L'analyse fondamentale consiste à étudier la santé financière d'une entreprise pour déterminer si son prix en bourse est justifié. On ne regarde pas les graphiques, mais les comptes de l'entreprise.

**Les documents clés**

• **Le Compte de Résultat** : montre si l'entreprise gagne de l'argent (Chiffre d'Affaires - Dépenses = Bénéfice).
• **Le Bilan** : montre ce que l'entreprise possède (Actifs) et ce qu'elle doit (Passif/Dettes).
• **Le Flux de Trésorerie (Cash Flow)** : montre l'argent réel qui entre et sort. C'est le juge de paix, car le bénéfice comptable peut être manipulé.

**Les ratios essentiels**

• **P/E Ratio (Price-to-Earnings)** : compare le prix de l'action au bénéfice par action. Un P/E de 15 signifie que vous payez 15 fois le bénéfice annuel.
• **Dividend Yield** : le dividende annuel divisé par le prix de l'action (le rendement en cash).
• **Dette / EBITDA** : mesure la capacité de l'entreprise à rembourser ses dettes grâce à son activité.""",
                    "example": "Une entreprise avec un P/E de 5 peut sembler bon marché, mais si son chiffre d'affaires baisse chaque année, c'est peut-être un 'Value Trap' (piège à valeur). À l'inverse, une entreprise avec un P/E de 30 peut être une excellente affaire si ses bénéfices doublent chaque année.",
                    "estimated_minutes": 15,
                    "xp_reward": 20,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Que compare le ratio P/E ?",
                            "choices": ["Le prix au chiffre d'affaires", "Le prix au bénéfice", "La dette au capital", "Le dividende au prix"],
                            "correct_answer": "Le prix au bénéfice",
                            "explanation": "Le Price-to-Earnings ratio indique combien d'euros un investisseur est prêt à payer pour chaque euro de bénéfice généré par l'entreprise."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Bourse et Économie",
            "description": "Comprenez l'impact de la macro-économie sur vos placements",
            "level": "intermediate",
            "order": 6,
            "icon": "🌍",
            "lessons": [
                {
                    "title": "L'impact des taux d'intérêt",
                    "content": """Les taux d'intérêt, fixés par les banques centrales (comme la BCE ou la FED), sont le "prix de l'argent". Ils ont une influence majeure sur la bourse.

**Quand les taux montent :**
• Emprunter coûte plus cher pour les entreprises (moins de bénéfices).
• Les consommateurs consomment moins (crédits plus chers).
• Les placements sans risque (livrets, obligations) deviennent plus attractifs par rapport aux actions.
• Résultat : la bourse a tendance à baisser.

**Quand les taux baissent :**
• L'argent est "facile" et pas cher.
• Les entreprises investissent et les consommateurs dépensent.
• Les investisseurs se tournent vers les actions pour trouver du rendement.
• Résultat : la bourse a tendance à monter.

**L'inflation : l'ennemie de l'épargnant**
L'inflation est la hausse des prix. Elle réduit votre pouvoir d'achat. L'investissement en actions a historiquement été l'un des meilleurs remparts contre l'inflation sur le long terme.""",
                    "example": "En 2022, pour lutter contre l'inflation, la FED a remonté ses taux brutalement de 0% à plus de 4%. En conséquence, le S&P 500 a chuté de près de 20% sur l'année.",
                    "estimated_minutes": 12,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quel est l'impact général d'une hausse des taux d'intérêt sur les actions ?",
                            "choices": ["Elles montent mécaniquement", "Elles ont tendance à baisser", "Cela n'a aucun impact", "Les dividendes sont supprimés"],
                            "correct_answer": "Elles ont tendance à baisser",
                            "explanation": "Une hausse des taux renchérit le coût de la dette pour les entreprises et rend les placements sécurisés plus compétitifs, ce qui pèse sur la valorisation des actions."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Diversifier pour réduire le risque",
            "description": "Apprenez à construire un portefeuille équilibré et résilient",
            "level": "intermediate",
            "order": 7,
            "icon": "🎨",
            "lessons": [
                {
                    "title": "Pourquoi et comment diversifier ?",
                    "content": """La diversification est l'un des rares "repas gratuits" en finance : elle permet de réduire le risque sans sacrifier le rendement. C'est le principe de ne pas mettre tous ses œufs dans le même panier.

**Les niveaux de diversification**

1. **Diversification géographique** : Répartir entre différentes zones (USA, Europe, Émergents).
2. **Diversification sectorielle** : Ne pas tout mettre dans la Tech ou l'Énergie.
3. **Diversification par classes d'actifs** : Combiner actions (croissance) et obligations (stabilité).

**La corrélation : concept clé**
La corrélation mesure comment deux actifs évoluent ensemble. Pour diversifier efficacement, on cherche des actifs peu corrélés, qui ne baissent pas tous en même temps.""",
                    "example": "En 2022, alors que les actions technologiques chutaient de 30%, les actions du secteur de l'énergie progressaient de 40%. Un investisseur diversifié a vu son capital protégé par cette compensation naturelle.",
                    "estimated_minutes": 15,
                    "xp_reward": 20,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "La diversification permet principalement de :",
                            "choices": ["Garantir un gain à 100%", "Réduire le risque sans sacrifier le rendement", "Ne plus payer de frais", "Prédire l'avenir"],
                            "correct_answer": "Réduire le risque sans sacrifier le rendement",
                            "explanation": "C'est l'atout majeur de la gestion de portefeuille : diluer les risques spécifiques à une entreprise ou un pays."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Psychologie de l'investisseur",
            "description": "Évitez les pièges émotionnels et prenez de meilleures décisions",
            "level": "intermediate",
            "order": 8,
            "icon": "🧠",
            "lessons": [
                {
                    "title": "Les biais cognitifs",
                    "content": """Notre cerveau n'est pas conçu pour la bourse. Nous sommes biologiquement programmés pour la survie, ce qui génère des biais dangereux pour nos investissements.

**Les biais majeurs :**
• **L'aversion à la perte** : la douleur d'une perte est 2x plus forte que la joie d'un gain. Cela pousse à vendre trop tôt ou garder des 'canards boiteux' trop longtemps.
• **Le FOMO (Fear Of Missing Out)** : la peur de rater le train, qui pousse à acheter au plus haut par euphorie.
• **Le biais de récence** : croire que ce qui s'est passé hier se passera forcément demain.""",
                    "example": "Vendre toutes ses actions en panique lors d'une baisse de 10% est la réaction émotionnelle typique de l'aversion à la perte, alors que l'investisseur rationnel y voit souvent une opportunité d'achat.",
                    "estimated_minutes": 15,
                    "xp_reward": 20,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Qu'est-ce que le FOMO ?",
                            "choices": ["Un indice boursier", "La peur de rater une opportunité", "Une taxe sur les bénéfices", "Le nom d'un robot trader"],
                            "correct_answer": "La peur de rater une opportunité",
                            "explanation": "C'est la peur irrationnelle de ne pas participer à un mouvement de hausse, ce qui conduit souvent à acheter des actifs surévalués."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Investissement responsable (ESG)",
            "description": "Investir en accord avec vos valeurs environnementales et sociales",
            "level": "intermediate",
            "order": 9,
            "icon": "🌱",
            "lessons": [
                {
                    "title": "Les critères ESG",
                    "content": """L'investissement ESG permet d'aligner vos objectifs financiers avec vos convictions éthiques.

**E (Environnement)** : impact sur le climat, gestion des déchets.
**S (Social)** : respect des droits humains, bien-être des salariés.
**G (Gouvernance)** : transparence de la direction, lutte contre la corruption.

Les entreprises bien notées sur ces critères sont souvent plus résilientes sur le long terme car elles gèrent mieux leurs risques juridiques et d'image.""",
                    "example": "Un fonds 'ISR' exclura les entreprises de tabac ou d'armement et privilégiera les leaders de la transition énergétique.",
                    "estimated_minutes": 12,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Que signifie le S dans ESG ?",
                            "choices": ["Spéculation", "Social", "Stabilité", "Secteur"],
                            "correct_answer": "Social",
                            "explanation": "Le pilier Social évalue la relation de l'entreprise avec ses employés, ses clients et les communautés où elle opère."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Fiscalité",
            "description": "Optimisez vos gains en choisissant la bonne enveloppe",
            "level": "intermediate",
            "order": 10,
            "icon": "🏛️",
            "lessons": [
                {
                    "title": "Le PEA vs le CTO",
                    "content": """En France, le choix de l'enveloppe fiscale est crucial pour la performance finale.

• **Le PEA (Plan d'Épargne en Actions)** : exonération d'impôts sur le revenu après 5 ans d'ouverture. Seuls les prélèvements sociaux (17,2%) restent dus. Idéal pour les actions européennes.
• **Le CTO (Compte-Titres Ordinaire)** : pas d'avantage fiscal (Flat Tax de 30% sur les gains), mais permet d'acheter des actions partout dans le monde (USA, Asie) sans limite de versement.""",
                    "example": "Sur 1 000€ de gain, le PEA vous permet de garder 828€, contre seulement 700€ sur un CTO. Sur 20 ans, la différence est colossale.",
                    "estimated_minutes": 15,
                    "xp_reward": 20,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quel est le principal avantage du PEA après 5 ans ?",
                            "choices": ["Aucun impôt sur le revenu sur les gains", "Les dividendes sont doublés", "On peut retirer l'argent sans frais", "La banque offre un bonus"],
                            "correct_answer": "Aucun impôt sur le revenu sur les gains",
                            "explanation": "Après 5 ans, vous ne payez que les prélèvements sociaux (17,2%) au lieu de la Flat Tax complète de 30%."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Construction de Portefeuille",
            "description": "Apprenez à assembler vos briques pour atteindre vos objectifs",
            "level": "intermediate",
            "order": 11,
            "icon": "🏗️",
            "lessons": [
                {
                    "title": "Les 3 profils types",
                    "content": """Il n'y a pas de 'meilleur' portefeuille universel, mais il y a un portefeuille adapté à votre profil d'investisseur.

**1. Profil Défensif (Prudent)**
• Objectif : protéger son capital.
• Composition : 20% Actions / 80% Obligations ou Fonds Euros.
• Volatilité : faible.

**2. Profil Équilibré**
• Objectif : croissance modérée et risque contrôlé.
• Composition : 50% Actions / 50% Obligations.
• Volatilité : moyenne.

**3. Profil Dynamique (Offensif)**
• Objectif : performance maximale sur le long terme.
• Composition : 90% Actions / 10% Obligations ou Or.
• Volatilité : élevée (acceptation des fortes baisses temporaires).""",
                    "example": "Jean, 25 ans, avec un horizon de placement de 40 ans, choisit un profil Dynamique. Marie, 62 ans, qui part à la retraite dans 3 ans, choisit un profil Défensif pour ne pas risquer son épargne juste avant d'en avoir besoin.",
                    "estimated_minutes": 15,
                    "xp_reward": 20,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quelle est la caractéristique d'un profil Dynamique ?",
                            "choices": ["Une part prépondérante d'actions", "Aucun risque de perte", "Uniquement des livrets bancaires", "Une garantie du capital par l'État"],
                            "correct_answer": "Une part prépondérante d'actions",
                            "explanation": "Le profil dynamique cherche la croissance long terme via les actions, en acceptant une volatilité plus élevée."
                        }
                    ]
                }
            ]
        },
        {
            "title": "Passer à l'action",
            "description": "Les étapes concrètes pour débuter",
            "level": "beginner",
            "order": 12,
            "icon": "🚀",
            "lessons": [
                {
                    "title": "Votre feuille de route",
                    "content": """Voici les étapes pour commencer sereinement :

1. **Épargne de précaution** : gardez 3 à 6 mois de dépenses sur un livret avant d'investir.
2. **Définir son horizon** : n'investissez en actions que de l'argent dont vous n'avez pas besoin pendant au moins 5 à 10 ans.
3. **Choisir son enveloppe** : ouvrez un PEA ou une Assurance-Vie.
4. **Automatiser** : mettez en place un virement mensuel automatique (DCA).
5. **Rester discipliné** : ne vendez pas pendant les tempêtes. Les meilleurs investisseurs sont souvent ceux qui oublient leur mot de passe !""",
                    "example": "Débuter avec 50€/mois sur un ETF World via un PEA est infiniment plus efficace que d'attendre d'avoir 10 000€ pour 'tout miser' au bon moment.",
                    "estimated_minutes": 10,
                    "xp_reward": 15,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quelle est la première étape avant d'investir en bourse ?",
                            "choices": ["Tout miser sur le Bitcoin", "Se constituer une épargne de précaution", "Emprunter de l'argent", "Démissionner pour devenir trader"],
                            "correct_answer": "Se constituer une épargne de précaution",
                            "explanation": "L'épargne de précaution vous évite de devoir vendre vos investissements boursiers en urgence (et potentiellement en perte) si vous avez un imprévu."
                        }
                    ]
                }
            ]
        }
    ]

    try:
        # Check if modules already exist
        existing_count = db.query(Module).count()
        if existing_count > 0:
            print(f"La base contient déjà {existing_count} modules. Pas de seeding nécessaire.")
            return True

        print(f"Seeding de {len(MODULES)} modules enrichis...")
        
        for mod_data in MODULES:
            module = Module(
                title=mod_data["title"],
                description=mod_data["description"],
                level=mod_data["level"],
                order=mod_data["order"],
                icon=mod_data["icon"]
            )
            db.add(module)
            db.flush() # Pour récupérer l'ID du module

            for idx, lesson_data in enumerate(mod_data["lessons"], 1):
                lesson = Lesson(
                    module_id=module.id,
                    title=lesson_data["title"],
                    content=lesson_data["content"],
                    example=lesson_data.get("example"),
                    order=idx,
                    estimated_minutes=lesson_data["estimated_minutes"],
                    xp_reward=lesson_data["xp_reward"]
                )
                db.add(lesson)
                db.flush() # Pour récupérer l'ID de la leçon

                for q_idx, q_data in enumerate(lesson_data["questions"], 1):
                    # Handle multiple choice and true/false
                    choices = q_data.get("choices")
                    if q_data["type"] == "true_false" and not choices:
                        choices = ["Vrai", "Faux"]
                    
                    question = Question(
                        lesson_id=lesson.id,
                        type=q_data["type"],
                        prompt=q_data["prompt"],
                        choices=choices,
                        correct_answer=q_data["correct_answer"],
                        explanation=q_data["explanation"],
                        order=q_idx
                    )
                    db.add(question)
        
        db.commit()
        print("✅ Seeding terminé avec succès !")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du seeding : {e}")
        db.rollback()
        return False
