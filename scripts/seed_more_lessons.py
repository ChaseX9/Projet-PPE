"""
Add more lessons to existing Academy modules.
Run with: python3 -m scripts.seed_more_lessons
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Additional lessons to add to existing modules (matched by title)
EXTRA_LESSONS = {
    "Les bases de l'investissement": [
        {
            "title": "L'inflation : l'ennemie silencieuse",
            "content": """L'inflation est la hausse générale et durable des prix. Elle érode silencieusement le pouvoir d'achat de votre épargne. Comprendre l'inflation est essentiel pour tout investisseur.

**Comment l'inflation est-elle mesurée ?**

L'INSEE calcule l'Indice des Prix à la Consommation (IPC) chaque mois en suivant l'évolution du prix d'un "panier" de biens et services représentatifs. En zone euro, la BCE surveille l'IPCH (Indice des Prix à la Consommation Harmonisé).

**L'impact concret sur votre épargne**

Si vous avez 10 000€ sur un compte courant à 0% et que l'inflation est à 4% :
- Après 1 an : votre pouvoir d'achat réel est de 9 615€
- Après 5 ans : 8 219€ de pouvoir d'achat réel
- Après 10 ans : 6 756€ de pouvoir d'achat réel

Vous n'avez rien perdu nominalement, mais vous avez perdu 32% de pouvoir d'achat !

**Le taux réel : ce qui compte vraiment**

Le taux réel = taux nominal - inflation.
- Livret A à 3% avec inflation à 4% → taux réel = -1% (vous perdez du pouvoir d'achat)
- ETF actions à 8% avec inflation à 3% → taux réel = +5% (vous gagnez réellement)

**Les actifs qui protègent de l'inflation**

• **Actions** : les entreprises répercutent la hausse des prix sur leurs clients, leurs bénéfices suivent l'inflation
• **Immobilier** : les loyers et les prix augmentent généralement avec l'inflation
• **Or** : valeur refuge historique contre l'inflation
• **Obligations indexées sur l'inflation** (OATi en France) : le capital et les intérêts sont ajustés à l'inflation
• **Matières premières** : pétrole, métaux, agricole — souvent à l'origine de l'inflation

**Les actifs qui souffrent de l'inflation**

• **Liquidités et livrets** : perdent du pouvoir d'achat si le taux est inférieur à l'inflation
• **Obligations à taux fixe** : leur valeur baisse quand l'inflation monte (les taux d'intérêt augmentent)

**L'hyperinflation : cas extrêmes**

L'Allemagne en 1923, le Zimbabwe en 2008, l'Argentine aujourd'hui : quand l'inflation dépasse 50% par mois, la monnaie perd toute valeur. Les investisseurs qui avaient des actifs réels (immobilier, or, actions) ont préservé leur patrimoine.""",
            "example": "En 2022, l'inflation en France a atteint 5,2%. Un livret A à 2% (taux de l'époque) offrait un taux réel de -3,2%. 10 000€ sur livret A ont perdu 320€ de pouvoir d'achat en un an. En parallèle, TotalEnergies a progressé de +20% car le groupe a bénéficié de la hausse des prix de l'énergie. L'inflation a enrichi les actionnaires de TotalEnergies et appauvri les épargnants en livret A.",
            "estimated_minutes": 12,
            "xp_reward": 15,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Si votre livret rapporte 2% et que l'inflation est à 5%, quel est votre taux réel ?",
                    "choices": ["-3%", "+3%", "+7%", "0%"],
                    "correct_answer": "-3%",
                    "explanation": "Taux réel = taux nominal - inflation = 2% - 5% = -3%. Vous perdez 3% de pouvoir d'achat chaque année malgré les intérêts."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Quel actif protège généralement le mieux contre l'inflation ?",
                    "choices": ["Compte courant", "Obligations à taux fixe", "Actions d'entreprises", "Bons du Trésor à court terme"],
                    "correct_answer": "Actions d'entreprises",
                    "explanation": "Les entreprises peuvent répercuter la hausse des prix sur leurs clients, préservant leurs marges. Historiquement, les actions surperforment l'inflation sur le long terme."
                },
                {
                    "type": "true_false",
                    "prompt": "L'inflation n'affecte pas l'argent placé sur un livret d'épargne.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. L'inflation érode le pouvoir d'achat de toute épargne dont le rendement est inférieur à l'inflation, y compris les livrets. Seul le montant nominal reste stable."
                }
            ]
        },
        {
            "title": "Les intérêts composés : la 8e merveille du monde",
            "content": """Albert Einstein aurait dit que les intérêts composés sont la huitième merveille du monde. Que ce soit vrai ou non, ce concept est fondamental pour comprendre pourquoi investir tôt fait une différence colossale.

**Intérêts simples vs intérêts composés**

• **Intérêts simples** : vous gagnez des intérêts uniquement sur votre capital initial.
  100€ à 10%/an → 10€ par an → 200€ après 10 ans

• **Intérêts composés** : vous gagnez des intérêts sur votre capital ET sur les intérêts déjà accumulés.
  100€ à 10%/an → 259€ après 10 ans (et non 200€)

La différence semble faible à court terme, mais elle devient énorme sur le long terme.

**La formule des intérêts composés**

Capital final = Capital initial × (1 + taux)^années

Exemples avec 1 000€ à 7%/an :
- Après 10 ans : 1 967€
- Après 20 ans : 3 870€
- Après 30 ans : 7 612€
- Après 40 ans : 14 974€

Votre argent se multiplie par 15 en 40 ans sans rien faire !

**L'effet du temps : commencer tôt est crucial**

Comparaison entre Alice et Bob, tous deux investissent 200€/mois à 7%/an :
- Alice commence à 25 ans et s'arrête à 35 ans (10 ans, 24 000€ investis)
- Bob commence à 35 ans et continue jusqu'à 65 ans (30 ans, 72 000€ investis)

À 65 ans :
- Alice : 263 000€ (malgré seulement 24 000€ investis !)
- Bob : 243 000€ (malgré 72 000€ investis !)

Alice a investi 3 fois moins mais a plus d'argent. C'est la magie des intérêts composés sur une longue période.

**La fréquence de capitalisation**

Plus les intérêts sont capitalisés fréquemment, plus l'effet est puissant :
- Annuelle : 1 000€ à 10% → 1 100€
- Mensuelle : 1 000€ à 10% → 1 104,71€
- Quotidienne : 1 000€ à 10% → 1 105,16€

**Comment maximiser les intérêts composés**

1. Commencer le plus tôt possible
2. Réinvestir tous les dividendes (ETF capitalisant)
3. Ne jamais retirer le capital prématurément
4. Maintenir un taux de rendement élevé (actions > obligations > livrets)
5. Investir régulièrement (DCA) pour augmenter la base de capitalisation""",
            "example": "Deux amis : Léa investit 5 000€ à 20 ans dans un ETF World et ne touche plus jamais à cet argent. Marc attend d'avoir 'assez d'argent' et investit 5 000€ à 40 ans. À 65 ans, avec un rendement de 7%/an : Léa a 67 000€, Marc a 27 000€. Ces 20 ans de différence ont multiplié le capital de Léa par 2,5. Le meilleur moment pour investir était il y a 20 ans. Le deuxième meilleur moment, c'est maintenant.",
            "estimated_minutes": 10,
            "xp_reward": 15,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Quelle est la différence principale entre intérêts simples et composés ?",
                    "choices": [
                        "Le taux d'intérêt appliqué",
                        "Les intérêts composés génèrent des intérêts sur les intérêts déjà accumulés",
                        "La durée minimale de placement",
                        "Le type d'actif concerné"
                    ],
                    "correct_answer": "Les intérêts composés génèrent des intérêts sur les intérêts déjà accumulés",
                    "explanation": "Avec les intérêts composés, chaque période vous gagnez des intérêts sur votre capital initial ET sur tous les intérêts précédemment accumulés. C'est cet effet 'boule de neige' qui crée une croissance exponentielle."
                },
                {
                    "type": "true_false",
                    "prompt": "Commencer à investir 10 ans plus tôt peut compenser un capital investi 3 fois plus faible.",
                    "choices": None,
                    "correct_answer": "true",
                    "explanation": "Vrai, comme le montre l'exemple d'Alice et Bob. Le temps est plus puissant que le montant investi grâce aux intérêts composés. C'est pourquoi il faut commencer le plus tôt possible."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Combien vaut 1 000€ investis à 7%/an après 30 ans (intérêts composés) ?",
                    "choices": ["3 100€", "7 612€", "4 500€", "2 100€"],
                    "correct_answer": "7 612€",
                    "explanation": "1 000 × (1,07)^30 = 7 612€. En 30 ans, votre capital est multiplié par 7,6 grâce aux intérêts composés. C'est bien plus que les 3 100€ qu'on obtiendrait avec des intérêts simples (1 000 + 30×70)."
                }
            ]
        }
    ],
    "Comprendre les actions": [
        {
            "title": "Lire et analyser les résultats d'une entreprise",
            "content": """Pour investir intelligemment en actions, il faut savoir lire les états financiers d'une entreprise. Pas besoin d'être comptable — quelques indicateurs clés suffisent.

**Les trois documents financiers essentiels**

**1. Le compte de résultat (P&L)**
Il montre si l'entreprise est rentable sur une période donnée.
- Chiffre d'affaires (CA) : total des ventes
- EBITDA : bénéfice avant intérêts, impôts, dépréciation et amortissement
- Résultat net : le bénéfice final après tout

**2. Le bilan**
Photographie du patrimoine de l'entreprise à un instant T.
- Actif : ce que possède l'entreprise (usines, stocks, trésorerie...)
- Passif : ce qu'elle doit (dettes, capitaux propres...)

**3. Le tableau des flux de trésorerie**
Montre les entrées et sorties d'argent réelles.
- Free Cash Flow (FCF) : argent réellement généré après investissements

**Les ratios d'évaluation clés**

• **PER (Price Earnings Ratio)** = Prix / Bénéfice par action
  Un PER de 15 signifie que vous payez 15€ pour 1€ de bénéfice annuel.
  PER < 15 : potentiellement sous-évalué
  PER > 25 : potentiellement surévalué (ou forte croissance attendue)

• **PEG (Price Earnings Growth)** = PER / Taux de croissance des bénéfices
  PEG < 1 : action potentiellement bon marché par rapport à sa croissance

• **P/B (Price to Book)** = Prix / Valeur comptable par action
  Mesure si l'action est chère par rapport aux actifs de l'entreprise

• **EV/EBITDA** = Valeur d'entreprise / EBITDA
  Permet de comparer des entreprises avec des structures de capital différentes

**Les indicateurs de santé financière**

• **Ratio d'endettement** = Dette nette / EBITDA
  < 2 : sain, > 4 : attention
• **Marge nette** = Résultat net / CA
  Mesure la rentabilité réelle
• **ROE (Return on Equity)** = Résultat net / Capitaux propres
  Mesure l'efficacité du capital investi par les actionnaires

**Où trouver ces informations ?**

- Site de l'entreprise (section Investisseurs)
- AMF (Autorité des Marchés Financiers)
- Boursorama, Zonebourse, MarketScreener
- Yahoo Finance, Morningstar""",
            "example": "LVMH en 2023 : CA de 86 milliards €, résultat net de 15 milliards €, PER de 22. Cela signifie que pour chaque euro de bénéfice LVMH, les investisseurs paient 22€. C'est 'cher' par rapport à la moyenne historique (PER ~15), mais justifié par la croissance régulière (+15%/an) et le pricing power exceptionnel des marques de luxe. Un investisseur value dirait 'trop cher', un investisseur growth dirait 'justifié'.",
            "estimated_minutes": 15,
            "xp_reward": 20,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Qu'est-ce que le PER (Price Earnings Ratio) ?",
                    "choices": [
                        "Le pourcentage de dividendes versés",
                        "Le rapport entre le prix de l'action et le bénéfice par action",
                        "Le taux de croissance annuel de l'entreprise",
                        "La dette totale divisée par les capitaux propres"
                    ],
                    "correct_answer": "Le rapport entre le prix de l'action et le bénéfice par action",
                    "explanation": "PER = Prix de l'action / Bénéfice par action. Il indique combien les investisseurs paient pour 1€ de bénéfice. Un PER de 20 signifie qu'ils paient 20€ pour 1€ de bénéfice annuel."
                },
                {
                    "type": "true_false",
                    "prompt": "Un PER très élevé signifie toujours que l'action est surévaluée.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. Un PER élevé peut être justifié par une forte croissance attendue. Amazon avait un PER de 100+ pendant des années, mais sa croissance explosive a justifié cette valorisation. Il faut toujours contextualiser le PER."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Quel document financier montre les entrées et sorties d'argent réelles d'une entreprise ?",
                    "choices": ["Le compte de résultat", "Le bilan", "Le tableau des flux de trésorerie", "Le rapport annuel"],
                    "correct_answer": "Le tableau des flux de trésorerie",
                    "explanation": "Le tableau des flux de trésorerie (cash flow statement) montre les mouvements réels d'argent. Le Free Cash Flow (FCF) est particulièrement important : c'est l'argent réellement disponible après investissements."
                }
            ]
        },
        {
            "title": "Les secteurs boursiers : investir par thématique",
            "content": """La bourse est divisée en secteurs économiques. Comprendre ces secteurs permet de diversifier intelligemment et de profiter des cycles économiques.

**La classification GICS (11 secteurs)**

**1. Technologie de l'information**
Apple, Microsoft, NVIDIA, ASML, Capgemini
Caractéristiques : forte croissance, valorisations élevées, sensible aux taux d'intérêt

**2. Santé**
Sanofi, Pfizer, Johnson & Johnson, Novo Nordisk
Caractéristiques : défensif, croissance régulière, protégé des récessions

**3. Finance**
BNP Paribas, JPMorgan, AXA, Visa
Caractéristiques : profite de la hausse des taux, sensible aux crises bancaires

**4. Consommation discrétionnaire**
LVMH, Tesla, Amazon, Airbus
Caractéristiques : cyclique, souffre en récession, profite de la croissance économique

**5. Consommation de base**
Nestlé, L'Oréal, Danone, Unilever
Caractéristiques : très défensif, dividendes stables, résiste aux récessions

**6. Énergie**
TotalEnergies, Shell, ExxonMobil
Caractéristiques : cyclique, corrélé au prix du pétrole, dividendes élevés

**7. Industrie**
Airbus, Schneider Electric, Siemens, Vinci
Caractéristiques : cyclique, profite de la croissance économique

**8. Matériaux**
ArcelorMittal, Air Liquide, Saint-Gobain
Caractéristiques : très cyclique, corrélé aux matières premières

**9. Immobilier (REITs)**
Unibail-Rodamco, Klepierre
Caractéristiques : revenus réguliers, sensible aux taux d'intérêt

**10. Services aux collectivités (Utilities)**
Engie, EDF, Veolia
Caractéristiques : très défensif, dividendes stables, peu de croissance

**11. Télécommunications**
Orange, Bouygues, Deutsche Telekom
Caractéristiques : défensif, dividendes élevés, faible croissance

**La rotation sectorielle**

Les secteurs performent différemment selon la phase du cycle économique :
- **Expansion** : technologie, consommation discrétionnaire, industrie
- **Récession** : santé, consommation de base, utilities
- **Reprise** : finance, énergie, matériaux

**Stratégie sectorielle pour débutant**

Pour un débutant, un ETF World couvre automatiquement tous les secteurs dans les bonnes proportions. Pas besoin de choisir !""",
            "example": "En 2022 : récession crainte + hausse des taux. Résultat : technologie -33% (NASDAQ), immobilier -25%, mais énergie +40% (TotalEnergies), santé +5%. Un portefeuille 100% tech a souffert. Un portefeuille diversifié par secteurs a bien mieux résisté. En 2023 : reprise de la tech +40%. Ceux qui avaient paniqué et vendu en 2022 ont raté la remontée.",
            "estimated_minutes": 12,
            "xp_reward": 15,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Quel secteur est considéré comme le plus défensif en période de récession ?",
                    "choices": ["Technologie", "Consommation de base (Nestlé, Danone)", "Énergie", "Finance"],
                    "correct_answer": "Consommation de base (Nestlé, Danone)",
                    "explanation": "La consommation de base (alimentation, hygiène, produits ménagers) est défensive car les gens continuent d'acheter ces produits même en récession. Ces entreprises ont des revenus stables et versent des dividendes réguliers."
                },
                {
                    "type": "true_false",
                    "prompt": "Un ETF MSCI World couvre automatiquement tous les secteurs boursiers.",
                    "choices": None,
                    "correct_answer": "true",
                    "explanation": "Vrai. Un ETF MSCI World inclut ~1500 entreprises de 23 pays couvrant tous les secteurs dans leurs proportions naturelles. C'est la diversification sectorielle automatique."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Quel secteur profite généralement le plus d'une hausse des taux d'intérêt ?",
                    "choices": ["Technologie", "Immobilier", "Finance (banques)", "Consommation discrétionnaire"],
                    "correct_answer": "Finance (banques)",
                    "explanation": "Les banques profitent de la hausse des taux car elles prêtent à des taux plus élevés tout en rémunérant peu les dépôts. Leur marge d'intérêt nette s'améliore. À l'inverse, l'immobilier et la tech souffrent des taux élevés."
                }
            ]
        }
    ],
    "Les ETF : investir simplement": [
        {
            "title": "Comment choisir et acheter son premier ETF",
            "content": """Vous savez ce qu'est un ETF. Maintenant, comment passer à l'action concrètement ? Voici le guide pratique pour choisir et acheter votre premier ETF.

**Étape 1 : Choisir l'indice à répliquer**

Pour un débutant, trois choix s'imposent :

• **MSCI World** : 1 500 entreprises de 23 pays développés. La diversification maximale. Idéal comme cœur de portefeuille (60-80% du portefeuille).

• **S&P 500** : 500 grandes entreprises américaines. Les USA représentent 60% de la capitalisation mondiale. Performance historique excellente.

• **CAC 40 / Euro Stoxx 600** : si vous voulez une exposition européenne (éligible PEA sans ETF synthétique).

**Étape 2 : Comparer les ETF qui répliquent cet indice**

Pour le MSCI World, plusieurs ETF existent :
- Amundi MSCI World (CW8) : TER 0,38%, encours 8 milliards €
- iShares Core MSCI World (IWDA) : TER 0,20%, encours 60 milliards €
- Lyxor MSCI World (LYWD) : TER 0,30%

Critères de sélection :
1. **TER (Total Expense Ratio)** : plus c'est bas, mieux c'est
2. **Encours** : > 100M€ pour garantir la liquidité
3. **Tracking error** : écart entre la performance de l'ETF et son indice (doit être faible)
4. **Capitalisant vs distribuant** : capitalisant = dividendes réinvestis automatiquement (idéal pour la croissance)
5. **Éligibilité PEA** : si vous utilisez un PEA

**Étape 3 : Choisir son courtier**

Pour un PEA :
- Boursorama : 0€ de frais de garde, 1,99€ par ordre
- Fortuneo : 0€ de frais de garde, 1,95€ par ordre
- Bourse Direct : frais très bas pour les gros volumes

Pour un CTO :
- Trade Republic : 1€ par ordre, interface simple
- Degiro : frais très bas, large choix

**Étape 4 : Passer son premier ordre**

Types d'ordres :
- **Ordre au marché** : achat immédiat au prix du moment (simple mais prix non garanti)
- **Ordre à cours limité** : vous fixez le prix maximum d'achat (recommandé pour les ETF peu liquides)

**Étape 5 : Mettre en place le DCA automatique**

La plupart des courtiers permettent de programmer des achats automatiques mensuels. C'est la meilleure façon d'investir régulièrement sans y penser.""",
            "example": "Paul, 30 ans, veut investir 200€/mois. Il ouvre un PEA chez Boursorama (gratuit). Il choisit l'ETF Amundi MSCI World (CW8) éligible PEA. Il programme un virement automatique de 200€ le 5 de chaque mois et un ordre d'achat automatique. Frais : 1,99€/mois soit 0,99% de commission. En 10 ans, il aura investi 24 000€ et avec un rendement de 7%/an, son capital sera d'environ 34 000€.",
            "estimated_minutes": 15,
            "xp_reward": 20,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Que signifie TER pour un ETF ?",
                    "choices": ["Taux d'Épargne Recommandé", "Total Expense Ratio (frais totaux annuels)", "Taux d'Échange Réel", "Titre d'Épargne Réglementé"],
                    "correct_answer": "Total Expense Ratio (frais totaux annuels)",
                    "explanation": "Le TER (Total Expense Ratio) représente les frais annuels totaux prélevés par l'ETF. Un TER de 0,20% signifie que vous payez 2€ par an pour 1 000€ investis. Plus c'est bas, mieux c'est."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Qu'est-ce qu'un ETF 'capitalisant' ?",
                    "choices": [
                        "Un ETF qui investit uniquement dans des grandes capitalisations",
                        "Un ETF qui réinvestit automatiquement les dividendes",
                        "Un ETF avec un capital garanti",
                        "Un ETF réservé aux investisseurs institutionnels"
                    ],
                    "correct_answer": "Un ETF qui réinvestit automatiquement les dividendes",
                    "explanation": "Un ETF capitalisant réinvestit automatiquement les dividendes reçus des entreprises, ce qui maximise l'effet des intérêts composés. À l'inverse, un ETF distribuant verse les dividendes en cash sur votre compte."
                },
                {
                    "type": "true_false",
                    "prompt": "Il faut attendre d'avoir plusieurs milliers d'euros pour acheter son premier ETF.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. Certains ETF sont accessibles dès quelques dizaines d'euros. Trade Republic permet même d'acheter des fractions d'ETF. L'important est de commencer, même avec de petites sommes."
                }
            ]
        },
        {
            "title": "ETF thématiques : opportunités et pièges",
            "content": """Au-delà des ETF larges (MSCI World, S&P500), il existe des ETF thématiques qui ciblent des secteurs ou tendances spécifiques. Opportunité ou piège ? Les deux, selon comment on les utilise.

**Qu'est-ce qu'un ETF thématique ?**

Un ETF thématique investit dans un thème d'investissement spécifique :
- Robotique et Automisation
- Énergies renouvelables et transition énergétique
- Cybersécurité
- Biotechnologie et génomique
- Eau et ressources naturelles
- Immobilier mondial (REITs)
- Marchés émergents (Chine, Inde, Brésil...)

**Les avantages des ETF thématiques**

• Exposition ciblée à une tendance de long terme
• Diversification au sein du thème (pas de risque sur une seule entreprise)
• Accessibilité à des secteurs complexes (biotech, cybersécurité)
• Frais inférieurs aux fonds actifs thématiques

**Les risques spécifiques**

• **Concentration** : moins diversifié qu'un ETF World
• **Valorisations élevées** : les thèmes populaires sont souvent déjà chers
• **Timing difficile** : les thèmes peuvent mettre des années à se concrétiser
• **Frais plus élevés** : TER souvent 0,5% à 0,75% vs 0,2% pour un ETF World
• **Risque de mode** : certains thèmes disparaissent (ETF cannabis, ETF SPAC...)

**Exemples concrets de performances**

ETF Énergies renouvelables (iShares Global Clean Energy) :
- 2020 : +140% (euphorie verte)
- 2021-2023 : -60% (hausse des taux, problèmes de chaîne d'approvisionnement)

ETF Secteur Technologique :
- 2023 : +50% (boom ChatGPT)
- Valorisations très élevées, risque de correction

**Comment intégrer les ETF thématiques ?**

Règle d'or : les ETF thématiques ne doivent représenter qu'une petite partie du portefeuille (10-20% maximum). Le cœur du portefeuille doit rester un ETF large et diversifié.

Structure recommandée :
- 70-80% : ETF MSCI World ou S&P500 (cœur)
- 10-20% : ETF thématiques (satellites)
- 0-10% : actions individuelles (si vous aimez l'analyse)

**Les ETF factoriels (Smart Beta)**

Une catégorie intermédiaire entre ETF passifs et actifs :
- **Value** : actions sous-évaluées
- **Momentum** : actions en tendance haussière
- **Quality** : entreprises rentables et stables
- **Low Volatility** : actions peu volatiles
- **Small Cap** : petites capitalisations""",
            "example": "En 2020, les ETF cannabis ont explosé (+200%) suite à la légalisation au Canada. Des milliers d'investisseurs ont acheté au sommet. En 2023, ces ETF ont perdu 80-90% de leur valeur. À l'inverse, un investisseur qui avait 80% en ETF World et 20% en ETF cannabis a limité sa perte globale à 20% et a profité de la hausse du World. La leçon : les thèmes sont des satellites, jamais le cœur du portefeuille.",
            "estimated_minutes": 12,
            "xp_reward": 15,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Quelle proportion maximale du portefeuille devrait représenter les ETF thématiques ?",
                    "choices": ["50-60%", "30-40%", "10-20%", "80-90%"],
                    "correct_answer": "10-20%",
                    "explanation": "Les ETF thématiques sont plus risqués et concentrés. Ils ne doivent représenter qu'une petite partie (10-20%) du portefeuille, le reste étant investi dans des ETF larges et diversifiés comme le MSCI World."
                },
                {
                    "type": "true_false",
                    "prompt": "Les ETF thématiques ont généralement des frais plus bas que les ETF larges comme le MSCI World.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. Les ETF thématiques ont généralement des TER plus élevés (0,5-0,75%) que les ETF larges (0,2-0,4%). La gestion d'un indice thématique est plus complexe et coûteuse."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Qu'est-ce qu'un ETF 'Smart Beta' ou factoriel ?",
                    "choices": [
                        "Un ETF géré par un algorithme propriétaire",
                        "Un ETF qui cible des facteurs spécifiques comme la valeur ou le momentum",
                        "Un ETF avec un rendement garanti",
                        "Un ETF réservé aux investisseurs professionnels"
                    ],
                    "correct_answer": "Un ETF qui cible des facteurs spécifiques comme la valeur ou le momentum",
                    "explanation": "Les ETF Smart Beta (ou factoriels) suivent des indices construits selon des critères spécifiques : valeur (actions sous-évaluées), momentum (tendance), qualité (rentabilité), etc. Ils sont entre la gestion passive et active."
                }
            ]
        }
    ],
    "Diversifier pour réduire le risque": [
        {
            "title": "Construire son portefeuille : les modèles éprouvés",
            "content": """Il existe plusieurs modèles de portefeuille éprouvés par des décennies de données. Voici les plus populaires et comment les adapter à votre situation.

**Le portefeuille 60/40 (classique)**

60% actions + 40% obligations
- Rendement historique : ~7% par an
- Volatilité modérée
- Idéal pour : investisseur modéré, horizon 10-15 ans

**Le portefeuille 3 fonds (Three-Fund Portfolio)**

Popularisé par Vanguard :
1. ETF actions monde développé (ex: MSCI World) : 60%
2. ETF actions marchés émergents : 20%
3. ETF obligations monde : 20%

Simple, diversifié, peu coûteux. Convient à 90% des investisseurs.

**Le portefeuille All Weather (Ray Dalio)**

Conçu pour performer dans toutes les conditions économiques :
- 30% actions
- 40% obligations long terme
- 15% obligations moyen terme
- 7,5% or
- 7,5% matières premières

Très défensif, faible volatilité, mais rendement plus modeste.

**Le portefeuille permanent (Harry Browne)**

4 classes d'actifs à 25% chacune :
- 25% actions
- 25% obligations long terme
- 25% or
- 25% liquidités

Extrêmement stable, protège contre tous les scénarios économiques.

**Le portefeuille 100% actions (pour les jeunes)**

Pour un horizon > 20 ans et une tolérance au risque élevée :
- 80% ETF MSCI World
- 20% ETF marchés émergents

Rendement historique le plus élevé (~9-10%/an) mais volatilité importante.

**Adapter son portefeuille à son âge**

Règle classique : % d'obligations = votre âge
- 25 ans : 25% obligations, 75% actions
- 45 ans : 45% obligations, 55% actions
- 65 ans : 65% obligations, 35% actions

Règle moderne (espérance de vie plus longue) : % obligations = âge - 20

**Le rééquilibrage**

Votre allocation dérive avec le temps. Si les actions montent, elles représentent plus que prévu. Il faut rééquilibrer 1 à 2 fois par an en vendant ce qui a monté et en achetant ce qui a baissé. C'est contre-intuitif mais efficace.""",
            "example": "Sophie, 35 ans, choisit un portefeuille 80/20 : 80% ETF MSCI World + 20% ETF obligations. En 2022, les actions baissent de 18% et les obligations de 12% (hausse des taux). Son portefeuille perd 17%. Elle rééquilibre en janvier 2023 en achetant plus d'obligations (qui ont baissé). En 2023, les actions remontent de 20%, les obligations de 5%. Son portefeuille gagne 17%. Le rééquilibrage lui a permis d'acheter bas et de profiter de la remontée.",
            "estimated_minutes": 15,
            "xp_reward": 20,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Que signifie 'rééquilibrer' son portefeuille ?",
                    "choices": [
                        "Vendre toutes ses positions et recommencer",
                        "Ramener son allocation à la répartition cible initiale",
                        "Ajouter de nouvelles classes d'actifs",
                        "Changer de courtier"
                    ],
                    "correct_answer": "Ramener son allocation à la répartition cible initiale",
                    "explanation": "Le rééquilibrage consiste à vendre les actifs qui ont surperformé (et représentent trop) et acheter ceux qui ont sous-performé pour revenir à l'allocation cible. C'est une façon disciplinée d'acheter bas et vendre haut."
                },
                {
                    "type": "true_false",
                    "prompt": "Un portefeuille 100% actions est recommandé pour tous les investisseurs.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. Un portefeuille 100% actions convient uniquement aux investisseurs avec un horizon très long (>20 ans) et une forte tolérance au risque. Pour la plupart des gens, une diversification avec des obligations réduit la volatilité sans sacrifier trop de rendement."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Selon la règle classique, quel pourcentage d'obligations devrait avoir un investisseur de 40 ans ?",
                    "choices": ["20%", "40%", "60%", "80%"],
                    "correct_answer": "40%",
                    "explanation": "La règle classique dit : % obligations = votre âge. À 40 ans, 40% en obligations et 60% en actions. Cette règle est parfois ajustée à l'ère moderne (espérance de vie plus longue) : % obligations = âge - 20, soit 20% à 40 ans."
                }
            ]
        }
    ],
    "Psychologie de l'investisseur": [
        {
            "title": "Développer une discipline d'investissement à long terme",
            "content": """La connaissance des marchés ne suffit pas. Ce qui distingue les investisseurs qui réussissent, c'est leur discipline et leur capacité à s'en tenir à leur plan sur le long terme.

**Pourquoi la discipline est plus importante que l'intelligence**

Des études montrent que les investisseurs particuliers sous-performent systématiquement les marchés de 2 à 4% par an. Pas parce qu'ils choisissent de mauvais actifs, mais parce qu'ils achètent et vendent au mauvais moment, guidés par leurs émotions.

**Les principes d'une discipline d'investissement**

**1. Avoir un plan écrit**
Définissez à l'avance :
- Votre objectif (retraite, achat immobilier, liberté financière)
- Votre horizon de placement
- Votre allocation cible (ex: 80% actions, 20% obligations)
- Vos règles de rééquilibrage
- Votre stratégie en cas de crise (-20%, -40%, -50%)

**2. Automatiser pour éviter les décisions émotionnelles**
- Virement automatique mensuel vers votre compte d'investissement
- Ordre d'achat automatique d'ETF
- Rééquilibrage automatique si disponible

**3. Limiter la surveillance du portefeuille**
Regarder son portefeuille tous les jours amplifie les émotions et pousse à agir. Règle : regardez votre portefeuille maximum 1 fois par mois, idéalement 1 fois par trimestre.

**4. Tenir un journal d'investissement**
Notez vos décisions et vos raisonnements. Cela vous aide à :
- Identifier vos biais récurrents
- Éviter de répéter les mêmes erreurs
- Rester rationnel face aux événements

**5. S'éduquer en continu**
Lisez des livres de référence :
- "L'Investisseur Intelligent" - Benjamin Graham
- "Un Marché pour Gagner" - Burton Malkiel
- "Père Riche, Père Pauvre" - Robert Kiyosaki
- "The Psychology of Money" - Morgan Housel

**6. Ignorer le bruit médiatique**
Les médias financiers vivent de l'anxiété et du sensationnalisme. "La bourse va s'effondrer" ou "Achetez maintenant avant qu'il soit trop tard" sont des titres conçus pour vous faire réagir, pas pour vous aider à investir.

**Le test de la nuit**
Avant chaque décision d'investissement importante, dormez dessus. Si vous voulez toujours faire la même chose le lendemain matin, c'est probablement une bonne décision. Si vous avez changé d'avis, c'était de l'émotion.

**La règle des 5%**
Ne prenez jamais une décision qui représente plus de 5% de votre portefeuille sans avoir dormi dessus et consulté votre plan écrit.""",
            "example": "Warren Buffett a dit : 'La bourse est un dispositif pour transférer l'argent des impatients vers les patients.' En 2008-2009, la crise financière a fait chuter les marchés de 50%. Les investisseurs disciplinés qui ont maintenu leurs positions ont récupéré tout en 3 ans et multiplié leur capital par 4 en 10 ans. Ceux qui ont vendu en panique ont cristallisé une perte de 50% et raté la remontée. La discipline a littéralement doublé la performance.",
            "estimated_minutes": 12,
            "xp_reward": 15,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Pourquoi les investisseurs particuliers sous-performent-ils généralement les marchés ?",
                    "choices": [
                        "Parce qu'ils n'ont pas accès aux mêmes informations que les professionnels",
                        "Parce qu'ils achètent et vendent au mauvais moment, guidés par leurs émotions",
                        "Parce que les frais de courtage sont trop élevés",
                        "Parce qu'ils investissent dans de mauvaises entreprises"
                    ],
                    "correct_answer": "Parce qu'ils achètent et vendent au mauvais moment, guidés par leurs émotions",
                    "explanation": "Les études DALBAR montrent que les investisseurs particuliers sous-performent les indices de 2-4%/an, principalement à cause du mauvais timing (acheter après une hausse, vendre après une baisse). La discipline bat l'intelligence en investissement."
                },
                {
                    "type": "true_false",
                    "prompt": "Il est recommandé de surveiller son portefeuille plusieurs fois par jour pour réagir rapidement aux opportunités.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. Surveiller son portefeuille trop fréquemment amplifie les émotions et pousse à des décisions irrationnelles. Les meilleurs investisseurs regardent leur portefeuille rarement (mensuel ou trimestriel) et s'en tiennent à leur plan."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Qu'est-ce que 'le test de la nuit' en investissement ?",
                    "choices": [
                        "Analyser les marchés asiatiques pendant la nuit",
                        "Dormir sur une décision importante avant de l'exécuter",
                        "Investir uniquement le soir pour éviter la volatilité",
                        "Vérifier son portefeuille avant de dormir"
                    ],
                    "correct_answer": "Dormir sur une décision importante avant de l'exécuter",
                    "explanation": "Le test de la nuit consiste à attendre le lendemain avant d'exécuter une décision importante. Si vous voulez toujours faire la même chose le matin, c'est probablement rationnel. Si vous avez changé d'avis, c'était de l'émotion."
                }
            ]
        }
    ],
    "Investissement responsable (ESG)": [
        {
            "title": "Mesurer et réduire l'impact de son portefeuille",
            "content": """Au-delà de choisir des fonds ESG, il est possible de mesurer et d'optimiser concrètement l'impact environnemental et social de votre portefeuille.

**Les outils de mesure d'impact**

**1. L'empreinte carbone du portefeuille**
Exprimée en tonnes de CO2 équivalent par million d'euros investis (tCO2e/M€).
- Portefeuille classique MSCI World : ~150 tCO2e/M€
- Portefeuille MSCI World ESG Leaders : ~90 tCO2e/M€ (-40%)
- Portefeuille bas carbone : ~50 tCO2e/M€ (-67%)

Outils : Morningstar Sustainability Rating, MSCI ESG Ratings, Sustainalytics

**2. Le score ESG**
Note de 0 à 100 attribuée à chaque entreprise selon ses pratiques E, S et G.
- AAA-AA : leaders ESG
- A-BBB : bonne pratique
- BB-B : pratique moyenne
- CCC : retardataires ESG

**3. L'alignement avec les Accords de Paris**
Certains fonds publient leur "température implicite" : de combien de degrés la Terre se réchaufferait si toutes les entreprises avaient le même profil carbone que le fonds.
- Fonds classique : 3,5°C
- Fonds ESG : 2,5°C
- Fonds bas carbone : 1,8°C

**Les stratégies d'investissement à impact**

**1. L'exclusion sectorielle**
Exclure les secteurs les plus controversés :
- Charbon thermique (> 25% du CA)
- Armement controversé (mines antipersonnel, bombes à sous-munitions)
- Tabac
- Jeux d'argent

**2. L'engagement actionnarial**
En tant qu'actionnaire, vous pouvez voter lors des assemblées générales sur les résolutions climatiques et sociales. Les grands fonds (BlackRock, Amundi) exercent une pression croissante sur les entreprises.

**3. L'investissement à impact direct**
- **Obligations vertes (Green Bonds)** : financement de projets environnementaux
- **Obligations sociales** : financement de projets sociaux
- **Crowdfunding d'énergies renouvelables** : financement direct de projets solaires ou éoliens

**4. La finance solidaire**
- Livret de développement durable et solidaire (LDDS) : une partie finance des projets ESG
- Fonds 90/10 : 90% investissement classique + 10% entreprises solidaires

**Les labels à connaître**

• **Label ISR** : investissement socialement responsable (France)
• **Label Greenfin** : fonds verts (France)
• **Article 8 SFDR** : fonds qui promeuvent des caractéristiques ESG (Europe)
• **Article 9 SFDR** : fonds avec un objectif d'investissement durable (Europe)
• **B Corp** : certification pour les entreprises à impact positif""",
            "example": "Camille décide de 'verdir' son portefeuille. Elle remplace son ETF MSCI World classique par un ETF MSCI World ESG Leaders (même performance historique, frais légèrement plus élevés +0,1%). Elle ajoute 10% d'obligations vertes (Green Bonds) de la BEI (Banque Européenne d'Investissement). Résultat : son empreinte carbone baisse de 40%, son portefeuille finance des projets d'énergies renouvelables, et sa performance reste similaire. Elle peut mesurer son impact via l'application Morningstar.",
            "estimated_minutes": 12,
            "xp_reward": 15,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Qu'est-ce qu'une obligation verte (Green Bond) ?",
                    "choices": [
                        "Une obligation émise par des entreprises agricoles",
                        "Une obligation dont les fonds financent des projets environnementaux",
                        "Une obligation avec un taux d'intérêt lié à la performance ESG",
                        "Une obligation garantie par l'État"
                    ],
                    "correct_answer": "Une obligation dont les fonds financent des projets environnementaux",
                    "explanation": "Les Green Bonds (obligations vertes) sont des obligations dont les fonds levés sont exclusivement utilisés pour financer des projets environnementaux : énergies renouvelables, efficacité énergétique, transport propre, etc."
                },
                {
                    "type": "true_false",
                    "prompt": "L'empreinte carbone d'un portefeuille ESG est toujours identique à celle d'un portefeuille classique.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux. Un portefeuille ESG Leaders a généralement une empreinte carbone 30-50% inférieure à un portefeuille classique, car il exclut ou sous-pondère les entreprises les plus émettrices de CO2."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Que signifie 'Article 9 SFDR' pour un fonds d'investissement ?",
                    "choices": [
                        "Un fonds qui exclut les entreprises controversées",
                        "Un fonds avec un objectif d'investissement durable mesurable",
                        "Un fonds géré par des femmes",
                        "Un fonds réservé aux investisseurs institutionnels"
                    ],
                    "correct_answer": "Un fonds avec un objectif d'investissement durable mesurable",
                    "explanation": "L'Article 9 SFDR (Sustainable Finance Disclosure Regulation) désigne les fonds avec un objectif d'investissement durable explicite et mesurable. C'est la catégorie la plus exigeante, au-dessus de l'Article 8 (qui promeut des caractéristiques ESG)."
                }
            ]
        }
    ],
    "Passer à l'action": [
        {
            "title": "Construire son plan financier personnel",
            "content": """Avant d'investir, il faut avoir une vision claire de sa situation financière et de ses objectifs. Un plan financier personnel est la boussole qui guide toutes vos décisions.

**Étape 1 : Faire le bilan**

Actif :
- Épargne de précaution (livret A, LDDS)
- Investissements existants (PEA, assurance-vie, CTO)
- Immobilier (valeur du bien - crédit restant)
- Autres actifs (voiture, objets de valeur...)

Passif :
- Crédits en cours (immobilier, consommation, auto)
- Dettes diverses

Patrimoine net = Actif total - Passif total

**Étape 2 : Analyser ses revenus et dépenses**

Revenus mensuels nets :
- Salaire, revenus locatifs, dividendes...

Dépenses fixes :
- Loyer/crédit, charges, abonnements, assurances...

Dépenses variables :
- Alimentation, loisirs, transport, vêtements...

Capacité d'épargne = Revenus - Dépenses

**Étape 3 : Constituer l'épargne de précaution**

Avant d'investir, vous devez avoir une épargne de précaution équivalente à 3 à 6 mois de dépenses. Cette épargne doit être :
- Disponible immédiatement (pas bloquée)
- Sécurisée (livret A, LDDS, compte courant)
- Suffisante pour faire face aux imprévus (perte d'emploi, réparation voiture, santé...)

**Étape 4 : Définir ses objectifs**

Objectifs à court terme (< 3 ans) :
→ Épargne sécurisée (livret, fonds euros)

Objectifs à moyen terme (3-10 ans) :
→ Mix actions/obligations selon l'horizon

Objectifs à long terme (> 10 ans) :
→ Actions, ETF, immobilier

**Étape 5 : Choisir son allocation**

Profil défensif : 30% actions, 70% obligations/fonds euros
Profil équilibré : 60% actions, 40% obligations
Profil dynamique : 80% actions, 20% obligations
Profil offensif : 100% actions (horizon > 15 ans)

**Étape 6 : Mettre en place et automatiser**

1. Ouvrir les comptes adaptés (PEA, assurance-vie, CTO)
2. Définir le montant mensuel à investir
3. Automatiser les virements et les achats
4. Planifier un bilan annuel

**La règle des 50/30/20**

Une règle simple pour gérer son budget :
- 50% des revenus pour les besoins essentiels
- 30% pour les loisirs et envies
- 20% pour l'épargne et l'investissement""",
            "example": "Thomas, 32 ans, salaire net 2 800€/mois. Bilan : 8 000€ sur livret A (épargne de précaution OK), pas d'investissements, crédit voiture 150€/mois. Dépenses : 2 200€/mois. Capacité d'épargne : 600€/mois. Plan : 200€/mois en ETF MSCI World via PEA (ouvert immédiatement pour faire tourner le compteur des 5 ans), 200€/mois en assurance-vie fonds euros, 200€ en épargne complémentaire. En 20 ans à 7%/an, ses 200€/mois en ETF deviendront 104 000€.",
            "estimated_minutes": 15,
            "xp_reward": 20,
            "questions": [
                {
                    "type": "multiple_choice",
                    "prompt": "Quelle est la première étape avant de commencer à investir ?",
                    "choices": [
                        "Ouvrir un PEA",
                        "Constituer une épargne de précaution de 3 à 6 mois de dépenses",
                        "Acheter des actions individuelles",
                        "Consulter un conseiller financier"
                    ],
                    "correct_answer": "Constituer une épargne de précaution de 3 à 6 mois de dépenses",
                    "explanation": "Avant d'investir, il faut avoir un matelas de sécurité de 3 à 6 mois de dépenses sur un compte liquide et sécurisé. Sans cette épargne de précaution, vous risquez d'être forcé de vendre vos investissements au mauvais moment en cas d'imprévu."
                },
                {
                    "type": "multiple_choice",
                    "prompt": "Selon la règle 50/30/20, quel pourcentage des revenus devrait aller à l'épargne et l'investissement ?",
                    "choices": ["10%", "20%", "30%", "50%"],
                    "correct_answer": "20%",
                    "explanation": "La règle 50/30/20 recommande : 50% pour les besoins essentiels (loyer, nourriture, transport), 30% pour les loisirs et envies, et 20% pour l'épargne et l'investissement."
                },
                {
                    "type": "true_false",
                    "prompt": "Il faut attendre d'avoir remboursé tous ses crédits avant de commencer à investir.",
                    "choices": None,
                    "correct_answer": "false",
                    "explanation": "Faux (en général). Si le taux de votre crédit est inférieur au rendement attendu de vos investissements, il peut être judicieux d'investir en parallèle. Exception : les crédits à la consommation à taux élevé (>5%) doivent être remboursés en priorité."
                }
            ]
        }
    ]
}


def seed_more_lessons():
    session = Session()

    print("📚 Ajout de nouvelles leçons aux modules existants...")
    total_added = 0
    total_questions = 0

    for module_title, new_lessons in EXTRA_LESSONS.items():
        module = session.query(Module).filter(Module.title == module_title).first()
        if not module:
            print(f"⚠️  Module '{module_title}' non trouvé, ignoré.")
            continue

        # Get current max order
        existing_lessons = session.query(Lesson).filter(Lesson.module_id == module.id).all()
        max_order = max((l.order for l in existing_lessons), default=0)

        for lesson_data in new_lessons:
            max_order += 1
            lesson = Lesson(
                module_id=module.id,
                title=lesson_data["title"],
                content=lesson_data["content"],
                example=lesson_data["example"],
                order=max_order,
                estimated_minutes=lesson_data["estimated_minutes"],
                xp_reward=lesson_data["xp_reward"]
            )
            session.add(lesson)
            session.flush()
            total_added += 1

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

        print(f"  ✅ {len(new_lessons)} leçon(s) ajoutée(s) à '{module_title}'")

    session.commit()

    total_lessons = session.query(Lesson).count()
    total_modules = session.query(Module).count()
    print(f"\n🎉 Terminé !")
    print(f"   +{total_added} nouvelles leçons ajoutées")
    print(f"   +{total_questions} nouvelles questions ajoutées")
    print(f"   Total : {total_modules} modules, {total_lessons} leçons")
    session.close()


if __name__ == "__main__":
    seed_more_lessons()
