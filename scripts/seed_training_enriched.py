"""
Seed enriched educational content for CapInvest Academy.
This replaces all lessons with much longer, more detailed content.
Run with: python3 -m scripts.seed_training_enriched
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


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
                        "choices": ["Une dette de l'entreprise envers vous", "Une part de propriété de l'entreprise", "Un prêt que vous faites à l'entreprise", "Une garantie de remboursement"],
                        "correct_answer": "Une part de propriété de l'entreprise",
                        "explanation": "Une action est une fraction du capital d'une entreprise. En l'achetant, vous devenez copropriétaire et partagez les succès comme les difficultés de l'entreprise."
                    },
                    {
                        "type": "true_false",
                        "prompt": "Les dividendes sont garantis et versés chaque année.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux. Les dividendes sont décidés par le conseil d'administration et votés en assemblée générale. Ils peuvent être réduits, supprimés ou augmentés selon les résultats de l'entreprise."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Quelles sont les deux principales sources de gain pour un actionnaire ?",
                        "choices": ["Les intérêts et les commissions", "Les plus-values et les dividendes", "Les remboursements et les coupons", "Les loyers et les revenus fonciers"],
                        "correct_answer": "Les plus-values et les dividendes",
                        "explanation": "Un actionnaire peut gagner de deux façons : la plus-value (hausse du prix de l'action) et les dividendes (distribution d'une partie des bénéfices)."
                    }
                ]
            },
            {
                "title": "Stratégies d'investissement en actions",
                "content": """Il existe plusieurs façons d'investir en actions. Chaque stratégie a ses avantages, ses inconvénients et convient à des profils différents.

**1. L'investissement passif (Buy & Hold)**

Acheter des actions ou des ETF et les conserver sur le long terme, sans chercher à anticiper les mouvements du marché. C'est la stratégie recommandée pour la grande majorité des investisseurs particuliers.

Avantages :
- Peu de temps à consacrer
- Frais réduits (peu de transactions)
- Bénéficie de la croissance économique à long terme
- Évite les erreurs émotionnelles

Inconvénients :
- Nécessite de la patience
- Pas de protection lors des baisses

**2. Le DCA (Dollar Cost Averaging) - Investissement régulier**

Investir une somme fixe à intervalles réguliers (ex : 200€ chaque mois), peu importe le niveau du marché. Cette stratégie permet de lisser le prix d'achat moyen et d'éviter d'investir tout au mauvais moment.

Exemple : vous investissez 100€/mois. En janvier, l'action vaut 10€ (vous achetez 10 actions). En février, elle vaut 5€ (vous achetez 20 actions). Votre prix moyen est de 6,67€ au lieu de 7,50€ si vous aviez tout investi en janvier.

**3. L'investissement value (valeur)**

Chercher des actions sous-évaluées par rapport à leur valeur intrinsèque. Popularisé par Warren Buffett. Nécessite une analyse approfondie des entreprises.

**4. L'investissement growth (croissance)**

Investir dans des entreprises à fort potentiel de croissance, même si elles sont chères. Typiquement les entreprises technologiques. Plus risqué mais potentiellement très rentable.

**5. Le trading actif**

Acheter et vendre fréquemment pour profiter des variations de court terme. Très chronophage, très risqué. Études montrent que 80-90% des traders particuliers perdent de l'argent sur le long terme.

**Quelle stratégie choisir ?**

Pour un débutant : le DCA sur des ETF diversifiés est la stratégie la plus simple et la plus efficace statistiquement. Elle ne demande pas d'expertise et bénéficie de la croissance des marchés mondiaux.

**Les indicateurs clés à connaître**

- **PER (Price Earnings Ratio)** : prix de l'action / bénéfice par action. Mesure si une action est chère ou bon marché.
- **Rendement du dividende** : dividende annuel / prix de l'action. Ex : 3% signifie que vous recevez 3€ pour 100€ investis.
- **Capitalisation boursière** : valeur totale de l'entreprise en bourse.""",
                "example": "Comparaison sur 20 ans : Thomas investit 10 000€ d'un coup en bourse en janvier 2000 (juste avant l'éclatement de la bulle internet). Il perd 50% et met 10 ans à retrouver son niveau. Sophie investit 500€ par mois pendant 20 ans (DCA). Elle profite des baisses pour acheter moins cher et finit avec un capital bien supérieur à Thomas malgré le même investissement total. Le DCA protège des mauvais timings.",
                "estimated_minutes": 15,
                "xp_reward": 20,
                "questions": [
                    {
                        "type": "multiple_choice",
                        "prompt": "Quelle stratégie est généralement recommandée pour les investisseurs débutants ?",
                        "choices": ["Le trading quotidien", "Le DCA sur des ETF diversifiés", "L'investissement dans des start-ups", "L'achat d'options"],
                        "correct_answer": "Le DCA sur des ETF diversifiés",
                        "explanation": "Le DCA (investissement régulier) sur des ETF diversifiés est simple, peu coûteux, et statistiquement plus performant que la plupart des stratégies actives pour les particuliers."
                    },
                    {
                        "type": "true_false",
                        "prompt": "La majorité des traders particuliers actifs battent le marché sur le long terme.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux. Les études montrent que 80 à 90% des traders particuliers perdent de l'argent ou sous-performent le marché sur le long terme, notamment à cause des frais et des erreurs émotionnelles."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Quel est l'avantage principal du DCA (investissement régulier) ?",
                        "choices": ["Il garantit un rendement fixe", "Il permet de lire le prix d'achat moyen", "Il évite de payer des impôts", "Il permet de battre le marché"],
                        "correct_answer": "Il permet de lire le prix d'achat moyen",
                        "explanation": "Le DCA lisse le prix d'achat moyen en achetant plus d'actions quand elles sont bon marché et moins quand elles sont chères, réduisant l'impact d'un mauvais timing."
                    }
                ]
            }
        ]
    },
    {
        "title": "Les ETF : investir simplement",
        "description": "Comprenez les fonds indiciels et leur intérêt pour diversifier facilement",
        "level": "beginner",
        "order": 3,
        "icon": "📊",
        "lessons": [
            {
                "title": "Qu'est-ce qu'un ETF ?",
                "content": """Un ETF (Exchange Traded Fund), ou fonds indiciel coté, est l'un des outils d'investissement les plus révolutionnaires des dernières décennies. Il combine la diversification d'un fonds avec la simplicité d'une action.

**Le principe de fonctionnement**

Un ETF réplique automatiquement la performance d'un indice boursier (CAC40, S&P500, MSCI World...). Au lieu d'acheter individuellement les 40 actions du CAC40, vous achetez une seule part d'ETF CAC40 qui les contient toutes dans les mêmes proportions.

**Les grands indices boursiers**

• **CAC40** : les 40 plus grandes entreprises françaises (LVMH, TotalEnergies, Airbus...)
• **S&P500** : les 500 plus grandes entreprises américaines (Apple, Microsoft, Amazon...)
• **MSCI World** : environ 1 500 entreprises de 23 pays développés
• **MSCI Emerging Markets** : entreprises des pays émergents (Chine, Inde, Brésil...)

**Les avantages des ETF**

1. **Diversification instantanée** : un seul ETF World vous expose à des milliers d'entreprises dans le monde entier.

2. **Frais très bas** : les ETF sont gérés passivement (ils suivent mécaniquement un indice). Les frais annuels sont de 0,1% à 0,5%, contre 1,5% à 2,5% pour les fonds actifs.

3. **Transparence** : vous savez exactement ce que contient l'ETF à tout moment.

4. **Liquidité** : comme une action, vous pouvez acheter ou vendre un ETF à tout moment pendant les heures de bourse.

5. **Accessibilité** : certains ETF sont accessibles dès quelques euros.

**ETF physique vs synthétique**

• **ETF physique** : achète réellement les actions de l'indice. Plus sûr et transparent.
• **ETF synthétique** : utilise des produits dérivés pour répliquer l'indice. Légèrement moins cher mais avec un risque de contrepartie.

**Comment choisir un ETF ?**

Critères importants :
- **L'indice répliqué** : choisissez un indice large et diversifié
- **Les frais (TER)** : plus c'est bas, mieux c'est
- **L'encours** : préférez les ETF avec un encours important (>100M€) pour la liquidité
- **La méthode de réplication** : physique ou synthétique
- **La politique de distribution** : capitalisant (réinvestit les dividendes) ou distribuant""",
                "example": "Avec 500€, vous pouvez acheter une part d'ETF MSCI World (ex: Amundi MSCI World). Vous êtes instantanément exposé à Apple, Microsoft, Nestlé, Toyota, LVMH et 1 495 autres entreprises dans 23 pays. Les frais annuels sont de 0,38%, soit 1,90€ par an. Un fonds actif équivalent vous coûterait 10€ à 12,50€ par an pour une performance souvent inférieure.",
                "estimated_minutes": 12,
                "xp_reward": 15,
                "questions": [
                    {
                        "type": "multiple_choice",
                        "prompt": "Quelle est la principale différence entre un ETF et un fonds actif ?",
                        "choices": ["Le niveau de risque", "Les frais et la gestion passive vs active", "Le nombre d'actions détenues", "La fiscalité"],
                        "correct_answer": "Les frais et la gestion passive vs active",
                        "explanation": "Un ETF réplique mécaniquement un indice (gestion passive, frais bas 0,1-0,5%). Un fonds actif est géré par des gérants qui cherchent à battre le marché (frais élevés 1,5-2,5%), mais y parviennent rarement sur le long terme."
                    },
                    {
                        "type": "true_false",
                        "prompt": "Les ETF ont généralement des frais plus élevés que les fonds actifs.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux. Les ETF sont passifs et ont des frais très bas (0,1-0,5% par an) contre 1,5-2,5% pour les fonds actifs. Sur 20 ans, cette différence de frais représente une différence de performance considérable."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Combien d'entreprises contient environ un ETF MSCI World ?",
                        "choices": ["40 entreprises", "500 entreprises", "1 500 entreprises", "10 000 entreprises"],
                        "correct_answer": "1 500 entreprises",
                        "explanation": "L'indice MSCI World contient environ 1 500 entreprises de 23 pays développés, offrant une diversification géographique et sectorielle exceptionnelle."
                    }
                ]
            }
        ]
    },
    {
        "title": "Diversifier pour réduire le risque",
        "description": "Apprenez à construire un portefeuille équilibré et résilient",
        "level": "intermediate",
        "order": 4,
        "icon": "🎨",
        "lessons": [
            {
                "title": "Pourquoi et comment diversifier ?",
                "content": """La diversification est l'un des rares "repas gratuits" en finance : elle permet de réduire le risque sans sacrifier le rendement. C'est le principe de ne pas mettre tous ses œufs dans le même panier.

**Le principe mathématique**

Quand deux actifs ne sont pas parfaitement corrélés (ils ne bougent pas toujours dans le même sens), les combiner réduit la volatilité globale du portefeuille. C'est la magie de la diversification.

**Les niveaux de diversification**

1. **Diversification géographique**
Répartir entre différentes zones géographiques :
- Europe (CAC40, Euro Stoxx 600)
- États-Unis (S&P500, NASDAQ)
- Pays émergents (Chine, Inde, Brésil)
- Marchés développés hors US (Japon, Australie, Canada)

2. **Diversification sectorielle**
Ne pas concentrer dans un seul secteur :
- Technologie (Apple, Microsoft, NVIDIA)
- Santé (Sanofi, Pfizer, Johnson & Johnson)
- Finance (BNP Paribas, JPMorgan)
- Énergie (TotalEnergies, Shell)
- Consommation (LVMH, L'Oréal, Nestlé)
- Industrie, immobilier, utilities...

3. **Diversification par classes d'actifs**
Combiner différents types d'investissements :
- Actions : rendement élevé, risque élevé
- Obligations : rendement modéré, risque faible
- Immobilier (SCPI, REIT) : revenus réguliers
- Or : valeur refuge en période de crise
- Liquidités : sécurité et disponibilité

4. **Diversification temporelle (DCA)**
Investir régulièrement plutôt qu'en une seule fois.

**La corrélation : concept clé**

La corrélation mesure comment deux actifs évoluent ensemble. Une corrélation de +1 signifie qu'ils bougent toujours dans le même sens (aucun bénéfice à les combiner). Une corrélation de -1 signifie qu'ils bougent en sens opposé (diversification parfaite). En pratique, on cherche des actifs avec une corrélation faible ou négative.

**Exemple : actions vs obligations**

Historiquement, quand les actions baissent fortement (crise), les obligations d'État ont tendance à monter (les investisseurs fuient vers la sécurité). Un portefeuille 60% actions / 40% obligations est moins volatil qu'un portefeuille 100% actions.

**Les limites de la diversification**

La diversification ne protège pas contre le risque systémique (crise mondiale comme 2008 ou COVID-2020 où tout baisse en même temps). Elle réduit le risque spécifique (faillite d'une entreprise, crise d'un secteur).""",
                "example": "En 2022, la tech a chuté de 30% (NASDAQ -33%) mais l'énergie a progressé de 40% (TotalEnergies +20%). Un portefeuille 100% tech aurait perdu 33%. Un portefeuille diversifié 50% tech / 50% énergie aurait perdu seulement 6,5%. La diversification a sauvé 26,5% de performance ! C'est la magie de la non-corrélation entre secteurs.",
                "estimated_minutes": 15,
                "xp_reward": 20,
                "questions": [
                    {
                        "type": "multiple_choice",
                        "prompt": "La diversification permet principalement de :",
                        "choices": ["Augmenter le rendement garanti", "Réduire le risque spécifique sans sacrifier le rendement", "Éviter de payer des impôts", "Battre le marché plus facilement"],
                        "correct_answer": "Réduire le risque spécifique sans sacrifier le rendement",
                        "explanation": "La diversification réduit le risque lié à une entreprise ou un secteur particulier, sans nécessairement sacrifier le rendement. C'est le seul 'repas gratuit' en finance."
                    },
                    {
                        "type": "true_false",
                        "prompt": "La diversification protège totalement contre les crises mondiales.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux. La diversification réduit le risque spécifique mais pas le risque systémique. Lors d'une crise mondiale (2008, COVID), presque tous les actifs baissent simultanément."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Qu'est-ce que la corrélation entre deux actifs ?",
                        "choices": ["Leur rendement moyen commun", "La mesure de comment ils évoluent ensemble", "Leur niveau de risque combiné", "Leur frais de gestion"],
                        "correct_answer": "La mesure de comment ils évoluent ensemble",
                        "explanation": "La corrélation mesure si deux actifs bougent dans le même sens (+1), en sens opposé (-1) ou indépendamment (0). Pour diversifier efficacement, on cherche des actifs peu corrélés."
                    }
                ]
            }
        ]
    },
    {
        "title": "Psychologie de l'investisseur",
        "description": "Évitez les pièges émotionnels et prenez de meilleures décisions",
        "level": "intermediate",
        "order": 5,
        "icon": "🧠",
        "lessons": [
            {
                "title": "Les biais cognitifs qui ruinent les investisseurs",
                "content": """Notre cerveau n'est pas conçu pour investir. Il est programmé pour survivre dans un environnement de prédateurs, pas pour gérer un portefeuille boursier. Résultat : nous commettons des erreurs systématiques qui coûtent cher.

**Les principaux biais cognitifs**

**1. L'aversion aux pertes**
Nous ressentons la douleur d'une perte deux fois plus intensément que le plaisir d'un gain équivalent. Perdre 100€ fait deux fois plus mal que gagner 100€ fait plaisir. Conséquence : on vend trop tôt pour "sécuriser" les gains et on garde trop longtemps les positions perdantes en espérant qu'elles remontent.

**2. La panique lors des baisses (comportement moutonnier)**
Quand les marchés baissent, la peur s'empare des investisseurs. Tout le monde vend en même temps, ce qui amplifie la baisse. Les investisseurs qui vendent en panique cristallisent leurs pertes au pire moment.

**3. L'euphorie lors des bulles (FOMO)**
"Fear Of Missing Out" : la peur de rater une opportunité. Quand tout le monde parle d'un investissement (Bitcoin en 2021, actions tech en 1999), les investisseurs achètent au sommet, juste avant l'effondrement.

**4. Le biais de confirmation**
On cherche inconsciemment les informations qui confirment nos croyances et on ignore celles qui les contredisent. Si vous pensez qu'une action va monter, vous ne lirez que les analyses positives.

**5. L'excès de confiance**
La plupart des investisseurs pensent être meilleurs que la moyenne. Impossible statistiquement. Cet excès de confiance pousse à prendre trop de risques et à trader trop fréquemment.

**6. L'ancrage**
On s'accroche à un prix de référence arbitraire. "Je ne vendrai pas tant que l'action n'est pas revenue à son prix d'achat." Ce prix n'a aucune signification pour le marché.

**7. Le biais de récence**
On extrapole le passé récent dans le futur. Après 3 ans de hausse, on pense que ça va continuer. Après une crise, on pense que ça va continuer à baisser.

**Comment lutter contre ces biais ?**

• Automatiser ses investissements (DCA mensuel automatique)
• Se fixer des règles à l'avance et les respecter
• Ne pas regarder son portefeuille tous les jours
• Avoir un plan écrit et s'y tenir
• Se rappeler que les émotions sont le pire conseiller financier""",
                "example": "Mars 2020 : le COVID fait chuter les marchés de 35% en un mois. Des millions d'investisseurs paniquent et vendent. Ceux qui ont vendu ont cristallisé une perte de 35%. Ceux qui sont restés investis ont vu leurs portefeuilles remonter de +60% en 12 mois. La panique a coûté 95% de performance à ceux qui ont cédé à leurs émotions. La leçon : les crises sont des opportunités pour les investisseurs disciplinés.",
                "estimated_minutes": 15,
                "xp_reward": 20,
                "questions": [
                    {
                        "type": "multiple_choice",
                        "prompt": "Qu'est-ce que l'aversion aux pertes ?",
                        "choices": ["La peur d'investir en bourse", "Le fait de ressentir les pertes plus intensément que les gains", "La tendance à vendre trop tôt", "Le refus de prendre des risques"],
                        "correct_answer": "Le fait de ressentir les pertes plus intensément que les gains",
                        "explanation": "L'aversion aux pertes est un biais cognitif où la douleur d'une perte est ressentie environ 2 fois plus intensément que le plaisir d'un gain équivalent. Cela pousse à des décisions irrationnelles."
                    },
                    {
                        "type": "true_false",
                        "prompt": "Il est recommandé de vendre ses actions dès qu'elles baissent de 10% pour limiter les pertes.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux. Les baisses temporaires sont normales. Vendre en panique transforme une perte temporaire en perte définitive. Sauf si les fondamentaux de l'entreprise ont changé, il vaut mieux rester investi."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Quelle est la meilleure façon de lutter contre les biais émotionnels en investissement ?",
                        "choices": ["Suivre les conseils des médias financiers", "Automatiser ses investissements et se fixer des règles à l'avance", "Surveiller son portefeuille plusieurs fois par jour", "Investir uniquement dans ce qu'on connaît"],
                        "correct_answer": "Automatiser ses investissements et se fixer des règles à l'avance",
                        "explanation": "Automatiser (DCA mensuel) et se fixer des règles à l'avance permet de retirer l'émotion de l'équation. On investit mécaniquement, sans être influencé par la peur ou l'euphorie du moment."
                    }
                ]
            }
        ]
    },
    {
        "title": "Investissement responsable (ESG)",
        "description": "Investir en accord avec vos valeurs environnementales et sociales",
        "level": "intermediate",
        "order": 6,
        "icon": "🌱",
        "lessons": [
            {
                "title": "L'investissement ESG : aligner rendement et valeurs",
                "content": """L'investissement ESG (Environnement, Social, Gouvernance) est une approche qui intègre des critères extra-financiers dans les décisions d'investissement. Il permet d'investir en accord avec ses valeurs sans sacrifier la performance.

**Les trois piliers de l'ESG**

**E - Environnement**
• Empreinte carbone et stratégie climatique
• Utilisation des énergies renouvelables
• Gestion des déchets et de l'eau
• Biodiversité et impact sur les écosystèmes
• Adaptation au changement climatique

**S - Social**
• Conditions de travail et sécurité des employés
• Diversité et inclusion (genre, origine, handicap)
• Relations avec les communautés locales
• Chaîne d'approvisionnement responsable
• Respect des droits humains

**G - Gouvernance**
• Indépendance et composition du conseil d'administration
• Rémunération des dirigeants
• Lutte contre la corruption et la fraude
• Transparence et qualité de l'information financière
• Droits des actionnaires minoritaires

**Les différentes approches ESG**

1. **L'exclusion** : exclure certains secteurs controversés (armement, tabac, charbon, jeux d'argent, alcool)

2. **Le best-in-class** : sélectionner les meilleures entreprises de chaque secteur selon les critères ESG, même dans des secteurs controversés

3. **L'intégration ESG** : intégrer les critères ESG dans l'analyse financière classique

4. **L'impact investing** : investir dans des projets avec un impact social ou environnemental mesurable

**Performance ESG vs marché classique**

Contrairement aux idées reçues, les investissements ESG ont généralement une performance similaire ou légèrement supérieure aux investissements classiques sur le long terme. Les entreprises bien notées ESG ont souvent une meilleure gestion des risques.

**Les labels et certifications**

• **Label ISR** (Investissement Socialement Responsable) : label français
• **Label Greenfin** : pour les fonds verts
• **Article 8 et 9 SFDR** : classification européenne des fonds ESG

**Les risques de greenwashing**

Certaines entreprises ou fonds se prétendent ESG sans l'être vraiment. Vérifiez les labels officiels et les rapports de durabilité détaillés.""",
                "example": "Un ETF MSCI World ESG Leaders exclut les 20% d'entreprises les moins bien notées ESG et surpondère les meilleures. Sur 10 ans, sa performance est quasi-identique au MSCI World classique (+/-1% par an), mais avec une empreinte carbone réduite de 40% et sans exposition aux entreprises de charbon ou d'armement controversé.",
                "estimated_minutes": 12,
                "xp_reward": 15,
                "questions": [
                    {
                        "type": "multiple_choice",
                        "prompt": "Que signifie le 'G' dans ESG ?",
                        "choices": ["Géographie", "Gouvernance", "Gestion", "Garantie"],
                        "correct_answer": "Gouvernance",
                        "explanation": "G = Gouvernance : qualité de la direction, transparence, droits des actionnaires, lutte contre la corruption. Une bonne gouvernance est souvent corrélée à une meilleure performance financière long terme."
                    },
                    {
                        "type": "true_false",
                        "prompt": "Les investissements ESG ont systématiquement une performance inférieure aux investissements classiques.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux. Les études montrent que les investissements ESG ont une performance similaire ou légèrement supérieure sur le long terme. Les entreprises bien notées ESG gèrent mieux leurs risques."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Qu'est-ce que le greenwashing ?",
                        "choices": ["Une technique de nettoyage écologique", "Se prétendre ESG sans l'être vraiment", "Un label officiel européen", "Une stratégie d'investissement dans les énergies vertes"],
                        "correct_answer": "Se prétendre ESG sans l'être vraiment",
                        "explanation": "Le greenwashing consiste à se présenter comme écologique ou responsable sans que cela soit réellement le cas. C'est pourquoi il faut vérifier les labels officiels (ISR, Greenfin, SFDR)."
                    }
                ]
            }
        ]
    },
    {
        "title": "Passer à l'action",
        "description": "Les étapes concrètes pour débuter votre parcours d'investisseur",
        "level": "beginner",
        "order": 7,
        "icon": "🚀",
        "lessons": [
            {
                "title": "Choisir le bon compte d'investissement",
                "content": """Avant d'investir, vous devez choisir le bon véhicule fiscal. En France, plusieurs enveloppes fiscales permettent d'investir avec des avantages importants.

**1. Le PEA (Plan d'Épargne en Actions)**

Le PEA est l'enveloppe reine pour investir en actions européennes avec une fiscalité avantageuse.

Caractéristiques :
- Plafond de versement : 150 000€ (225 000€ pour le PEA-PME)
- Investissements autorisés : actions et ETF d'entreprises européennes
- Fiscalité après 5 ans : seulement 17,2% de prélèvements sociaux (vs 30% pour un CTO)
- Avant 5 ans : 30% de flat tax sur les gains

Idéal pour : investir à long terme dans des ETF européens ou des actions françaises/européennes.

**2. Le Compte-Titres Ordinaire (CTO)**

Le CTO offre une liberté totale d'investissement sans plafond.

Caractéristiques :
- Pas de plafond de versement
- Accès à tous les marchés mondiaux (actions US, ETF World, obligations...)
- Fiscalité : 30% de flat tax sur les gains (PFU)
- Possibilité d'opter pour le barème progressif de l'IR

Idéal pour : investir au-delà du plafond PEA, accéder aux marchés non-européens, ou si vous avez un taux marginal d'imposition faible.

**3. L'Assurance-Vie**

L'assurance-vie est le placement préféré des Français avec plus de 1 800 milliards d'euros.

Caractéristiques :
- Pas de plafond de versement
- Accès à des fonds euros (capital garanti) et des unités de compte (actions, ETF, SCPI...)
- Fiscalité avantageuse après 8 ans : abattement de 4 600€/an (9 200€ pour un couple)
- Avantages successoraux importants

Idéal pour : épargne long terme, transmission de patrimoine, diversification avec des fonds euros.

**4. Le PER (Plan d'Épargne Retraite)**

Le PER est dédié à la préparation de la retraite avec un avantage fiscal immédiat.

Caractéristiques :
- Versements déductibles du revenu imposable
- Capital bloqué jusqu'à la retraite (sauf cas exceptionnels)
- Fiscalité à la sortie selon le mode de déblocage

Idéal pour : les contribuables fortement imposés qui veulent préparer leur retraite.

**Quelle stratégie adopter ?**

Pour un débutant, la stratégie optimale est souvent :
1. Ouvrir un PEA dès maintenant (le compteur des 5 ans commence à la date d'ouverture)
2. Investir dans des ETF World ou S&P500 via le PEA
3. Compléter avec une assurance-vie pour la diversification et la transmission
4. Utiliser un CTO si vous souhaitez accéder aux marchés non-européens

**Où ouvrir ces comptes ?**

Courtiers en ligne recommandés (frais bas) :
- Boursorama, Fortuneo, Bourse Direct (PEA et CTO)
- Trade Republic, Degiro (CTO)
- Linxea, Lucya Cardif (assurance-vie)""",
                "example": "Lucas, 28 ans, ouvre un PEA chez Boursorama en janvier 2024. Il investit 200€/mois dans un ETF MSCI World (via un ETF synthétique éligible PEA). En 2029, son PEA a 5 ans. Si ses 12 000€ investis ont généré 3 000€ de gains, il ne paiera que 516€ d'impôts (17,2%) au lieu de 900€ (30%) s'il avait utilisé un CTO. Économie : 384€ grâce au PEA.",
                "estimated_minutes": 15,
                "xp_reward": 20,
                "questions": [
                    {
                        "type": "multiple_choice",
                        "prompt": "Quel compte offre la meilleure fiscalité après 5 ans pour investir en actions européennes ?",
                        "choices": ["Compte-titres ordinaire (CTO)", "PEA (Plan d'Épargne en Actions)", "Livret A", "Compte courant"],
                        "correct_answer": "PEA (Plan d'Épargne en Actions)",
                        "explanation": "Le PEA bénéficie d'une exonération d'impôt sur les plus-values après 5 ans (seuls les prélèvements sociaux de 17,2% restent dus, vs 30% pour un CTO)."
                    },
                    {
                        "type": "multiple_choice",
                        "prompt": "Quel est le plafond de versement du PEA classique ?",
                        "choices": ["100 000€", "150 000€", "200 000€", "Pas de plafond"],
                        "correct_answer": "150 000€",
                        "explanation": "Le PEA classique a un plafond de versement de 150 000€. Il existe aussi le PEA-PME avec un plafond de 225 000€ supplémentaires pour investir dans les PME européennes."
                    },
                    {
                        "type": "true_false",
                        "prompt": "Il faut attendre d'avoir beaucoup d'argent avant d'ouvrir un PEA.",
                        "choices": None,
                        "correct_answer": "false",
                        "explanation": "Faux ! Il faut ouvrir un PEA le plus tôt possible car le compteur des 5 ans (pour bénéficier de la fiscalité avantageuse) commence à la date d'ouverture, pas à la date du premier versement."
                    }
                ]
            }
        ]
    }
]


def seed_enriched():
    session = Session()

    print("🗑️  Suppression du contenu existant...")
    session.query(Question).delete()
    session.query(Lesson).delete()
    session.query(Module).delete()
    session.commit()

    print("📚 Insertion du nouveau contenu enrichi...")
    total_lessons = 0
    total_questions = 0

    for mod_data in MODULES:
        module = Module(
            title=mod_data["title"],
            description=mod_data["description"],
            level=mod_data["level"],
            order=mod_data["order"],
            icon=mod_data["icon"]
        )
        session.add(module)
        session.flush()

        for idx, lesson_data in enumerate(mod_data["lessons"], 1):
            lesson = Lesson(
                module_id=module.id,
                title=lesson_data["title"],
                content=lesson_data["content"],
                example=lesson_data["example"],
                order=idx,
                estimated_minutes=lesson_data["estimated_minutes"],
                xp_reward=lesson_data["xp_reward"]
            )
            session.add(lesson)
            session.flush()
            total_lessons += 1

            for q_idx, q_data in enumerate(lesson_data["questions"], 1):
                question = Question(
                    lesson_id=lesson.id,
                    type=q_data["type"],
                    prompt=q_data["prompt"],
                    choices=q_data["choices"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"],
                    order=q_idx
                )
                session.add(question)
                total_questions += 1

    session.commit()
    print(f"✅ {session.query(Module).count()} modules insérés")
    print(f"✅ {total_lessons} leçons insérées (contenu enrichi)")
    print(f"✅ {total_questions} questions insérées")
    print("🎉 Terminé ! Les leçons sont maintenant beaucoup plus détaillées.")


if __name__ == "__main__":
    seed_enriched()
