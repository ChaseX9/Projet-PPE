"""
Part 1 of the Final Professional Curriculum for CapInvest Academy.
Modules 1 to 6 (Full Content).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed_curriculum_p1():
    session = Session()
    session.query(Question).delete()
    session.query(Lesson).delete()
    session.query(Module).delete()

    # --- MODULE 1: LES BASES (4 leçons) ---
    m1 = Module(title="Les bases de l'investissement", description="Fondamentaux pour bien débuter", level="beginner", order=1, icon="🎯")
    session.add(m1); session.flush()
    
    add_lesson(session, m1.id, 1, "Qu'est-ce qu'investir ?", 
        "Investir consiste à placer votre capital dans des actifs (actions, obligations, immobilier) pour générer un rendement futur. Contrairement à l'épargne classique, l'investissement comporte un risque de perte en capital mais offre un potentiel de gain bien supérieur sur le long terme.", 
        "1000€ sur un livret A (3%) vs 1000€ en bourse (8% potentiel).", 5, 10, [
        ("multiple_choice", "Quelle est la principale différence entre épargner et investir ?", ["Le montant", "Le risque", "La banque", "La durée"], "Le risque", "L'investissement n'est pas garanti."),
        ("true_false", "Investir permet de lutter contre l'inflation ?", None, "true", "Vrai, les rendements boursiers dépassent souvent l'inflation."),
        ("multiple_choice", "Le rendement total se compose de :", ["Plus-value", "Dividendes", "Plus-value + Dividendes", "Capital"], "Plus-value + Dividendes", "Gain en prix + revenu versé."),
        ("true_false", "Investir est sans risque si on utilise une application ?", None, "false", "Faux, le support ne change pas la nature de l'actif.")
    ])
    
    add_lesson(session, m1.id, 2, "Risque / Rendement", 
        "Il n'y a pas de rendement élevé sans risque élevé. C'est la règle d'or de la finance. Les actifs les plus sûrs ont les rendements les plus faibles (livrets), tandis que les plus risqués (actions, cryptos) peuvent rapporter beaucoup mais aussi chuter violemment.", 
        "Un livret A offre 3% garanti. Une action peut faire +20% ou -20% en un mois.", 6, 10, [
        ("multiple_choice", "Quel actif est le moins risqué ?", ["Actions Tech", "Obligations d'État", "Cryptos", "Immobilier"], "Obligations d'État", "Garanti par un pays stable."),
        ("true_false", "Prendre plus de risque garantit un gain élevé ?", None, "false", "Faux, c'est une probabilité, pas une certitude."),
        ("multiple_choice", "La volatilité mesure :", ["Le profit", "Les variations de prix", "La fiscalité", "Le nombre d'employés"], "Les variations de prix", "Plus ça bouge, plus c'est volatil."),
        ("true_false", "Le risque zéro existe en bourse ?", None, "false", "Faux.")
    ])
    
    add_lesson(session, m1.id, 3, "L'horizon de placement", 
        "Le temps est votre allié. Plus vous investissez sur le long terme (> 10 ans), plus vous lissez les crises passagères. Pour le court terme (< 3 ans), privilégiez la sécurité. Pour la retraite, les actions sont historiquement le meilleur moteur.", 
        "En 2008, la bourse a perdu 50%. En 10 ans, elle avait tout récupéré et triplé.", 5, 10, [
        ("multiple_choice", "Horizon recommandé pour les actions ?", ["6 mois", "2 ans", "Plus de 5-10 ans", "Peu importe"], "Plus de 5-10 ans", "Le temps réduit l'impact des krachs."),
        ("true_false", "Un retraité doit prendre moins de risque qu'un jeune ?", None, "true", "Vrai, car il a besoin de son capital à court terme."),
        ("multiple_choice", "Que se passe-t-il si vous vendez pendant un krach ?", ["Vous gagnez", "Vous matérialisez votre perte", "L'État vous rembourse", "Rien"], "Vous matérialisez votre perte", "La perte devient réelle au moment de la vente."),
        ("true_false", "Le risque diminue avec le temps ?", None, "true", "Vrai, historiquement les périodes de 20 ans en bourse sont positives.")
    ])
    
    add_lesson(session, m1.id, 4, "Les intérêts composés", 
        "Albert Einstein les appelait la 8ème merveille du monde. Vos intérêts génèrent eux-mêmes des intérêts. Sur 30 ans, cet effet boule de neige transforme de petits versements réguliers en une fortune considérable.", 
        "100€/mois à 7% sur 30 ans = 120 000€ (pour 36 000€ investis).", 7, 15, [
        ("multiple_choice", "Qu'est-ce que l'effet boule de neige ?", ["La baisse des prix", "Le rendement sur le rendement", "La dette", "La diversification"], "Le rendement sur le rendement", "C'est la capitalisation."),
        ("true_false", "Il vaut mieux commencer tôt avec peu que tard avec beaucoup ?", None, "true", "Vrai, le temps est le facteur le plus puissant."),
        ("multiple_choice", "Facteur exponentiel des intérêts composés ?", ["Le montant", "La banque", "Le temps", "La fiscalité"], "Le temps", "Il est la puissance dans la formule."),
        ("true_false", "Cela fonctionne aussi pour les dettes ?", None, "true", "Vrai, c'est pour cela que les dettes grossissent vite.")
    ])

    # --- MODULE 2: COMPRENDRE LES ACTIONS (3 leçons) ---
    m2 = Module(title="Comprendre les actions", description="Maîtrisez les actions et leur rôle", level="beginner", order=2, icon="📈")
    session.add(m2); session.flush()
    
    add_lesson(session, m2.id, 1, "C'est quoi une action ?", 
        "Une action est un titre de propriété. En achetant une action, vous devenez copropriétaire d'une entreprise. Vous avez droit à une partie des bénéfices (dividendes) et vous pouvez voter aux assemblées générales.", 
        "Posséder 10 actions Apple fait de vous un (petit) patron d'Apple.", 5, 10, [
        ("multiple_choice", "Une action est un titre de :", ["Créance", "Propriété", "Assurance", "Prêt"], "Propriété", "Vous possédez une part du capital."),
        ("true_false", "Une actionnaire peut tout perdre si la boîte fait faillite ?", None, "true", "Vrai, le risque est limité au capital investi."),
        ("multiple_choice", "Le dividende est :", ["Un impôt", "Une part du bénéfice", "Un frais de banque", "Un prêt"], "Une part du bénéfice", "Donné aux actionnaires."),
        ("true_false", "Toutes les actions versent des dividendes ?", None, "false", "Faux, certaines réinvestissent tout.")
    ])
    
    add_lesson(session, m2.id, 2, "Dividendes vs Croissance", 
        "Certaines entreprises (Growth) préfèrent réinvestir leurs profits pour grossir plus vite, ce qui fait monter le prix de l'action. D'autres (Rendement) versent régulièrement des dividendes pour attirer les investisseurs cherchant des revenus.", 
        "Amazon (Croissance) vs Coca-Cola (Rendement).", 6, 12, [
        ("multiple_choice", "Une action de 'Croissance' (Growth) mise sur :", ["Le dividende", "La hausse du prix", "La dette", "Le sponsoring"], "La hausse du prix", "On espère revendre plus cher."),
        ("true_false", "Une action sans dividende est forcément nulle ?", None, "false", "Faux, la plus-value peut être énorme."),
        ("multiple_choice", "Une entreprise mature verse souvent :", ["Plus d'actions", "Des dividendes", "Rien", "Des bons d'achat"], "Des dividendes", "Car elle a moins besoin de cash pour croître."),
        ("true_false", "Le dividende réduit le prix de l'action lors de son versement ?", None, "true", "Vrai, car la valeur sort de l'entreprise.")
    ])
    
    add_lesson(session, m2.id, 3, "Risques spécifique vs marché", 
        "Le risque spécifique est propre à une entreprise (ex: un scandale). Le risque de marché touche tout le monde (ex: une guerre, une récession). La diversification permet d'éliminer le spécifique, mais jamais totalement le marché.", 
        "Si vous n'avez que du Air France, une grève vous ruine. Si vous avez 50 actions, c'est anecdotique.", 5, 12, [
        ("multiple_choice", "Comment protéger son capital contre le risque spécifique ?", ["En pariant", "Par la diversification", "En vendant tout", "Par l'assurance"], "Par la diversification", "Plus on a d'actions différentes, moins on dépend d'une seule."),
        ("true_false", "Le risque de marché peut être annulé ?", None, "false", "Faux, on ne contrôle pas l'économie globale."),
        ("multiple_choice", "Un exemple de risque spécifique ?", ["Inflations", "Hausse des taux", "Faillite d'un fournisseur", "Guerre"], "Faillite d'un fournisseur", "Propre à la chaîne logistique de la boîte."),
        ("true_false", "Acheter un indice élimine le risque spécifique ?", None, "true", "Vrai, par nature l'indice contient beaucoup de titres.")
    ])

    # --- MODULE 3: LES ETF (3 leçons) ---
    m3 = Module(title="Les ETF : investir simplement", description="Fonds indiciels", level="beginner", order=3, icon="📊")
    session.add(m3); session.flush()
    
    add_lesson(session, m3.id, 1, "Qu'est-ce qu'un ETF ?", 
        "Un ETF (Exchange Traded Fund) est un panier d'actions qui recopie un indice (ex: CAC 40). Au lieu d'acheter 40 actions, vous achetez 1 seul titre qui les contient toutes. C'est simple, diversifié et très peu coûteux.", 
        "Un ETF World contient plus de 1500 entreprises mondiales pour 400€.", 5, 12, [
        ("multiple_choice", "Pourquoi un ETF est-il moins cher qu'un fonds classique ?", ["Car il est géré par des robots", "Moins de frais de gestion active", "Il est gratuit", "Pas de taxe"], "Moins de frais de gestion active", "C'est de la gestion passive."),
        ("true_false", "L'ETF suit exactement la performance de son indice ?", None, "true", "Vrai, c'est son unique but."),
        ("multiple_choice", "Que signifie 'répliquer un indice' ?", ["Le battre", "Le copier", "Le détruire", "Le vendre"], "Le copier", "Reproduire les poids des actions."),
        ("true_false", "On peut acheter un ETF à n'importe quel moment en bourse ?", None, "true", "Vrai, comme une action classique.")
    ])
    
    add_lesson(session, m3.id, 2, "Physique vs Synthétique", 
        "Certains ETF achètent réellement les titres (Physique). D'autres utilisent des contrats financiers (Synthétique) pour copier la performance. Le synthétique permet d'investir sur des marchés US via un PEA français.", 
        "Un ETF S&P 500 éligible PEA est forcément synthétique.", 6, 15, [
        ("multiple_choice", "La réplication physique consiste à :", ["Louer des titres", "Acheter réellement les actions", "Utiliser un swap", "Ne rien faire"], "Acheter réellement les actions", "C'est la plus transparente."),
        ("true_false", "Le synthétique comporte un risque de contrepartie ?", None, "true", "Vrai, lié à la banque qui garantit le swap."),
        ("multiple_choice", "Avantage du synthétique en France ?", ["Plus sûr", "Eligibilité PEA pour indices US", "Moins cher", "Plus connu"], "Eligibilité PEA pour indices US", "Grâce à la technique de réplication."),
        ("true_false", "La réplication physique est la norme en Europe ?", None, "true", "Vrai, c'est la plus populaire.")
    ])
    
    add_lesson(session, m3.id, 3, "Acc vs Dist", 
        "Les ETF 'Acc' réinvestissent automatiquement les dividendes reçus dans le fonds (capitalisation). Les ETF 'Dist' les versent sur votre compte espèces (distribution). Pour faire grossir son capital, l'Acc est idéal.", 
        "Sur 20 ans, les dividendes réinvestis représentent souvent 50% de la performance totale.", 5, 12, [
        ("multiple_choice", "Que signifie 'Acc' ?", ["Accélération", "Accumulation", "Accord", "Accessoire"], "Accumulation", "Le fonds garde tout."),
        ("true_false", "L'ETF Dist est meilleur pour la rente ?", None, "true", "Vrai, car il génère du cash régulier."),
        ("multiple_choice", "Quelle version maximise les intérêts composés ?", ["Dist", "Acc", "Les deux", "Aucun"], "Acc", "Car les dividendes retravaillent immédiatement."),
        ("true_false", "On peut changer un ETF Acc en Dist gratuitement ?", None, "false", "Non, il faut vendre et racheter.")
    ])

    # --- MODULE 4: INDICES (3 leçons) ---
    m4 = Module(title="Les Indices Boursiers", description="Baromètres du marché", level="beginner", order=4, icon="🏎️")
    session.add(m4); session.flush()
    
    add_lesson(session, m4.id, 1, "Les grands indices mondiaux", 
        "Chaque pays ou zone a son indice : le CAC 40 (France), le S&P 500 (plus grosses US), le NASDAQ (Tech) ou le MSCI World (monde développé). Ils servent de point de repère pour juger de la santé d'un marché.", 
        "Le S&P 500 est considéré comme l'indice le plus important au monde.", 5, 10, [
        ("multiple_choice", "Combien d'entreprises dans le CAC 40 ?", ["10", "40", "100", "500"], "40", "Les 40 plus grandes capitalisations françaises."),
        ("true_false", "Le NASDAQ est un indice surtout technologique ?", None, "true", "Vrai, il regroupe les géants du logiciel et du web."),
        ("multiple_choice", "L'indice de référence au Japon est :", ["Nikkei 225", "DAX", "FTSE 100", "IBEX"], "Nikkei 225", "L'indice phare de Tokyo."),
        ("true_false", "Un indice ne change jamais de composition ?", None, "false", "Faux, on remplace les sortants par les nouveaux champions.")
    ])
    
    add_lesson(session, m4.id, 2, "Poids et Capitalisation", 
        "Dans la plupart des indices, plus une entreprise vaut cher en bourse (capitalisation), plus elle pèse lourd dans l'indice. Une baisse d'Apple impactera plus le S&P 500 qu'une chute d'une petite banque régionale.", 
        "Apple et Microsoft pèsent souvent plus de 15% de l'indice NASDAQ à eux deux.", 6, 10, [
        ("multiple_choice", "Comment se calcule la capitalisation boursière ?", ["Nombre d'employés * CA", "Prix de l'action * nombre d'actions", "Bénéfice * 10", "Fixé par l'État"], "Prix de l'action * nombre d'actions", "C'est la valeur de marché."),
        ("true_false", "Une petite boîte peut faire bouger le CAC 40 ?", None, "false", "Faux, son poids est trop faible."),
        ("multiple_choice", "Un indice Equi-péré (Equally Weighted) :", ["Favorise les grosses", "Donne le même poids à toutes", "Est aléatoire", "Est réservé au Luxe"], "Donne le même poids à toutes", "Chaque action pèse le même %."),
        ("true_false", "La capitalisation flottante exclut les actions détenues par l'État ou les fondateurs ?", None, "true", "Vrai, on ne compte que ce qui s'échange réellement.")
    ])
    
    add_lesson(session, m4.id, 3, "Indices vs Gestion Active", 
        "Les statistiques SPIVA montrent que sur le long terme (10 ans), plus de 80% des gérants professionnels ne parviennent pas à battre leur indice de référence à cause des frais et des erreurs de choix.", 
        "Buffett a parié 1M$ que le S&P 500 battrait n'importe quel fonds spéculatif... et il a gagné.", 5, 12, [
        ("multiple_choice", "Pourquoi est-il dur de battre l'indice ?", ["Les ordinateurs sont plus intelligents", "Les frais de gestion mangent la performance", "C'est illégal", "L'indice ne fait pas d'erreurs"], "Les frais de gestion mangent la performance", "Un gérant à 2% doit performer 2% de plus chaque année."),
        ("true_false", "La gestion passive gagne du terrain ?", None, "true", "Vrai, de plus en plus de gens choisissent les ETF."),
        ("multiple_choice", "Le Tracking Error est :", ["Une erreur de l'indice", "L'écart entre l'ETF et son indice", "Une faillite de banque", "Un bug informatique"], "L'écart entre l'ETF et son indice", "Plus il est bas, plus l'ETF est fidèle."),
        ("true_false", "Il suffit de choisir le meilleur gérant de l'an dernier pour gagner ?", None, "false", "Faux, les performances passées ne préjugent pas des futures.")
    ])

    # --- MODULE 5: ANALYSE FONDAMENTALE (3 leçons) ---
    m5 = Module(title="Analyse Fondamentale", description="Santé des entreprises", level="intermediate", order=5, icon="🔍")
    session.add(m5); session.flush()
    
    add_lesson(session, m5.id, 1, "Le Compte de Résultat", 
        "Il retrace l'activité de l'année. On part des ventes (CA) pour arriver au profit final (Bénéfice net). Entre les deux, on déduit les coûts, les salaires et les impôts.", 
        "Faire 1M€ de CA ne sert à rien si on a 1.2M€ de charges.", 7, 15, [
        ("multiple_choice", "Le Chiffre d'Affaires est :", ["Le bénéfice", "Le total des ventes", "La dette", "Les impôts"], "Le total des ventes", "Ce qui rentre avant les dépenses."),
        ("true_false", "L'EBITDA mesure la performance opérationnelle brute ?", None, "true", "Vrai, avant intérêts, taxes et dépréciations."),
        ("multiple_choice", "Le bénéfice net négatif signifie :", ["Croissance", "Perte", "Richesse", "Impôts"], "Perte", "L'entreprise a perdu de l'argent."),
        ("true_false", "Le Dividende est payé avec le bénéfice ?", None, "true", "Vrai, normalement.")
    ])
    
    add_lesson(session, m5.id, 2, "Ratios : P/E et Yield", 
        "Le P/E (Price to Earnings) compare le prix au bénéfice. Un P/E de 15 signifie que vous payez l'action 15 fois son profit annuel. Le Yield est le rendement du dividende par rapport au prix de l'action.", 
        "Une action à 100€ qui gagne 5€/an a un P/E de 20.", 6, 15, [
        ("multiple_choice", "Un P/E élevé (50+) signifie souvent :", ["Action pas chère", "Fortes attentes de croissance", "Faillite proche", "Secteur bancaire"], "Fortes attentes de croissance", "Le marché paie pour le futur."),
        ("true_false", "Un Yield de 10% est toujours une aubaine ?", None, "false", "Faux, il peut signaler un danger de coupure du dividende."),
        ("multiple_choice", "Comment calculer le Yield ?", ["Prix / Dividende", "Dividende / Prix", "Bénéfice / Prix", "CA / Prix"], "Dividende / Prix", "Exprimé en %."),
        ("true_false", "Le P/E moyen historique est autour de 15-18 ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m5.id, 3, "Dette et Cash-Flow", 
        "Les bénéfices sont des comptables, le cash est une réalité. Le Free Cash Flow est l'argent restant dans la caisse après avoir payé tout le monde et investi dans les machines. C'est le nerf de la guerre.", 
        "Une boîte peut être 'rentable' sur le papier mais faire faillite si elle n'a plus de cash.", 5, 15, [
        ("multiple_choice", "Qu'est-ce que le Free Cash Flow ?", ["Le cash gratuit", "L'argent réel restant après investissements", "La dette brute", "Le CA"], "L'argent réel restant après investissements", "Indicateur de santé crucial."),
        ("true_false", "Une entreprise sans dette est plus solide en cas de crise ?", None, "true", "Vrai, elle ne dépend pas des banques."),
        ("multiple_choice", "Le ratio Dette Nette / EBITDA mesure :", ["Le profit", "La capacité à rembourser sa dette", "La taille du logo", "Le nombre d'employés"], "La capacité à rembourser sa dette", "Plus il est bas, mieux c'est."),
        ("true_false", "Le cash permet de racheter des actions pour doper le cours ?", None, "true", "Vrai, c'est le 'Buyback'.")
    ])

    # --- MODULE 6: ECONOMIE (3 leçons) ---
    m6 = Module(title="Bourse et Économie", description="L'environnement macro", level="intermediate", order=6, icon="🌍")
    session.add(m6); session.flush()
    
    add_lesson(session, m6.id, 1, "Inflation et Bourse", 
        "L'inflation est la hausse généralisée des prix. Elle érode le pouvoir d'achat. Les entreprises de qualité peuvent répercuter cette hausse sur leurs clients, les autres souffrent.", 
        "Si le prix du pain fait x2, la boulangerie doit doubler ses prix de vente pour survivre.", 5, 12, [
        ("multiple_choice", "L'inflation est la hausse des :", ["Salaires", "Prix", "Actions", "Dettes"], "Prix", "Baisse de valeur de la monnaie."),
        ("true_false", "Les obligations souffrent de l'inflation ?", None, "true", "Vrai, leur taux fixe devient moins attractif."),
        ("multiple_choice", "Que font les banques centrales contre l'inflation ?", ["Donnent de l'argent", "Augmentent les taux", "Baissent les taux", "Ferment la bourse"], "Augmentent les taux", "Pour ralentir l'économie et stabiliser les prix."),
        ("true_false", "L'hyperinflation rend les actions gratuites ?", None, "false", "Non, c'est le chaos économique.")
    ])
    
    add_lesson(session, m6.id, 2, "Les Taux d'intérêt", 
        "Le taux d'intérêt est le prix de l'argent. Quand il monte, emprunter coûte plus cher, la consommation baisse et la bourse stresse. Quand il baisse, l'argent coule à flot et les actions montent.", 
        "La FED (USA) et la BCE (Europe) fixent ces taux directeurs.", 6, 12, [
        ("multiple_choice", "Si les taux montent, le prix des obligations existantes :", ["Monte", "Baisse", "Reste stable", "Disparait"], "Baisse", "Relation inverse fondamentale."),
        ("true_false", "La FED gère l'euro ?", None, "false", "Faux, c'est le dollar."),
        ("multiple_choice", "Le taux directeur influence :", ["La météo", "Le coût des crédits immobiliers", "La couleur des billets", "Le prix du ticket de métro"], "Le coût des crédits immobiliers", "Impacte toute l'économie."),
        ("true_false", "Baisse des taux = Relance éco ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m6.id, 3, "Cycles Économiques", 
        "L'économie n'est pas linéaire. Elle alterne entre phases d'expansion (croissance, emploi) et de récession (baisse du PIB, chômage). La bourse anticipe souvent ces cycles avec 6 mois d'avance.", 
        "Une récession est définie par 2 trimestres consécutifs de baisse du PIB.", 5, 12, [
        ("multiple_choice", "La phase de croissance s'appelle :", ["Dépression", "Récession", "Expansion", "Stagnation"], "Expansion", "Hausse de la production et de la consommation."),
        ("true_false", "La bourse chute parfois AVANT le début d'une récession ?", None, "true", "Vrai, les investisseurs vendent dès qu'ils voient les nuages arriver."),
        ("multiple_choice", "Secteur cyclique par excellence :", ["Santé", "Luxe", "Automobile", "Eau"], "Automobile", "On achète une voiture quand tout va bien."),
        ("true_false", "Le secteur Défensif (Consommation de base) résiste mieux aux crises ?", None, "true", "Vrai, on achète toujours du savon ou du riz.")
    ])

    session.commit()
    print(f"✅ Part 1 Completed. Modules seedés.")

def add_lesson(session, module_id, order, title, content, example, minutes, xp, questions):
    lesson = Lesson(module_id=module_id, order=order, title=title, content=content, example=example, estimated_minutes=minutes, xp_reward=xp)
    session.add(lesson); session.flush()
    for idx, q in enumerate(questions, 1):
        q_type, prompt, choices, answer, explanation = q
        session.add(Question(lesson_id=lesson.id, order=idx, type=q_type, prompt=prompt, choices=choices, correct_answer=answer, explanation=explanation))

if __name__ == "__main__":
    seed_curriculum_p1()
