"""Utility for seeding the CapInvest Academy curriculum."""
from sqlalchemy.orm import Session
from .models import Module, Lesson, Question

def auto_seed_if_empty(db: Session):
    """Seed the curriculum only if no modules exist."""
    if db.query(Module).count() > 0:
        return False
        
    print("🌱 Database empty. Seeding full curriculum...")
    
    def add_lesson(module_id, order, title, content, example, minutes, xp, questions):
        lesson = Lesson(
            module_id=module_id, 
            order=order, 
            title=title, 
            content=content, 
            example=example, 
            estimated_minutes=minutes, 
            xp_reward=xp
        )
        db.add(lesson)
        db.flush()
        for idx, q in enumerate(questions, 1):
            q_type, prompt, choices, answer, explanation = q
            db.add(Question(
                lesson_id=lesson.id, 
                order=idx, 
                type=q_type, 
                prompt=prompt, 
                choices=choices, 
                correct_answer=answer, 
                explanation=explanation
            ))

    # --- MODULE 1: LES BASES ---
    m1 = Module(title="Les bases de l'investissement", description="Fondamentaux pour bien débuter", level="beginner", order=1, icon="🎯")
    db.add(m1); db.flush()
    add_lesson(m1.id, 1, "Qu'est-ce qu'investir ?", 
        "Investir consiste à placer votre capital dans des actifs (actions, obligations, immobilier) dans l'espoir de générer un rendement futur. La principale différence avec l'épargne classique (comme un livret) est que l'investissement comporte un risque de perte en capital : votre argent n'est pas garanti. En échange de ce risque, l'investissement offre un potentiel de gain supérieur et permet de lutter efficacement contre l'inflation, qui réduit sinon votre pouvoir d'achat. Le rendement total d'un investissement se compose généralement de la plus-value (hausse du prix) et des revenus versés (comme les dividendes).", 
        "1000€ à 3% (Épargne) vs 1000€ avec risque de perte mais 8% potentiel (Investissement).", 5, 10, [
        ("multiple_choice", "Quelle est la principale différence entre épargner et investir ?", ["Le montant", "Le risque de perte en capital", "La banque", "La durée"], "Le risque de perte en capital", "L'investissement n'est jamais garanti, contrairement au livret A."),
        ("true_false", "Investir permet de lutter contre l'inflation ?", None, "true", "Vrai, car les rendements visés sont supérieurs à la hausse des prix."),
        ("multiple_choice", "Le rendement total se compose de :", ["La plus-value seule", "Les dividendes seuls", "La plus-value + les revenus (ex: dividendes)", "Le capital initial"], "La plus-value + les revenus (ex: dividendes)", "C'est la somme de la croissance et des revenus."),
        ("true_false", "Investir via une application moderne supprime tout risque ?", None, "false", "Faux, le support ne change pas la nature risquée de l'actif.")
    ])
    add_lesson(m1.id, 2, "Le couple Risque / Rendement", 
        "En finance, le rendement est toujours lié au risque : vous ne pouvez pas espérer un gain élevé sans accepter une probabilité de perte importante. Les obligations d'État de pays stables sont considérées comme les actifs les moins risqués, tandis que les actions technologiques ou les cryptomonnaies sont bien plus volatiles. La volatilité mesure précisément l'ampleur et la fréquence des variations de prix d'un actif. Pour compenser un risque élevé, les investisseurs exigent systématiquement un rendement attendu plus important (la prime de risque).", 
        "Un livret offre 3% sûr. Une action peut faire +30% ou -30%, ce mouvement est la volatilité.", 6, 10, [
        ("multiple_choice", "Quel actif est généralement le moins risqué ?", ["Actions Tech", "Obligations d'État stables", "Cryptomonnaies", "Immobilier"], "Obligations d'État stables", "Un État a peu de chances de faire faillite."),
        ("true_false", "Prendre un risque élevé garantit un rendement élevé ?", None, "false", "Faux, c'est une probabilité, on peut aussi tout perdre."),
        ("multiple_choice", "Que mesure la volatilité ?", ["Le profit final", "L'ampleur des variations de prix", "La taxe", "Le nombre d'investisseurs"], "L'ampleur des variations de prix", "Plus le prix oscille, plus c'est volatil."),
        ("true_false", "Il est possible d'avoir un risque nul en bourse ?", None, "false", "Faux, il y a toujours un risque de marché.")
    ])
    add_lesson(m1.id, 3, "L'horizon de placement", 
        "L'horizon de placement est la durée prévue de votre investissement. Le temps est votre meilleur allié : investir sur le long terme (plus de 5 à 10 ans) permet de lisser la volatilité et de réduire l'impact des crises. Pour un retraité qui a besoin de son capital, on recommande de prendre moins de risque que pour un jeune qui a 30 ans devant lui. Si vous vendez vos titres pendant un krach, vous 'matérialisez' votre perte, elle devient réelle au lieu d'être une simple baisse temporaire.", 
        "Le krach de 2008 a duré 1 an, mais ceux qui sont restés 10 ans ont triplé leur mise.", 5, 10, [
        ("multiple_choice", "Quel horizon est recommandé pour investir majoritairement en actions ?", ["Quelques mois", "1 à 2 ans", "Au moins 5 à 10 ans", "Le temps d'un weekend"], "Au moins 5 à 10 ans", "Le temps efface les fluctuations de court terme."),
        ("true_false", "Un retraité devrait prendre plus de risque qu'un jeune actif ?", None, "false", "Faux, il a un horizon plus court et moins de temps pour se refaire."),
        ("multiple_choice", "Vendre pendant une baisse massive s'appelle :", ["Moyenner", "Matérialiser sa perte", "Gagner du temps", "Assurer son gain"], "Matérialiser sa perte", "La perte n'est réelle qu'au moment de la transaction."),
        ("true_false", "Le risque diminue avec le temps sur un marché diversifié ?", None, "true", "Vrai, la probabilité de perte sur 20 ans est historiquement proche de zéro.")
    ])
    add_lesson(m1.id, 4, "La magie des intérêts composés", 
        "Les intérêts composés consistent à réinvestir vos gains pour qu'ils produisent à leur tour de nouveaux intérêts. C'est l'effet boule de neige. À long terme, le facteur temps est bien plus puissant que le montant initial : il vaut mieux commencer tôt avec de petites sommes que tard avec de gros montants. Dans la formule mathématique, le temps est le facteur exponentiel.", 
        "100€ à 10% : An 1 = 110€. An 2 = 121€ (le 1€ en plus vient du réinvestissement).", 7, 15, [
        ("multiple_choice", "Qu'est-ce que l'effet boule de neige ?", ["La chute des prix", "Le réinvestissement des gains générant de nouveaux gains", "La dette", "La diversification"], "Le réinvestissement des gains générant de nouveaux gains", "C'est la définition de la capitalisation."),
        ("true_false", "Mieux vaut commencer à 20 ans avec 50€ que 40 ans avec 150€ ?", None, "true", "Vrai, grâce au temps qui démultiplie les gains."),
        ("multiple_choice", "Quel est le facteur exponentiel dans les intérêts composés ?", ["Le versement", "La banque", "Le temps", "La devise"], "Le temps", "C'est lui qui fait décoller la courbe à la fin."),
        ("true_false", "Les dettes subissent aussi les intérêts composés ?", None, "true", "Vrai, elles peuvent devenir incontrôlables.")
    ])

    # --- MODULE 2: COMPRENDRE LES ACTIONS ---
    m2 = Module(title="Comprendre les actions", description="Maîtrisez les actions et leur rôle", level="beginner", order=2, icon="📈")
    db.add(m2); db.flush()
    add_lesson(m2.id, 1, "C'est quoi une action ?", 
        "Une action est un titre de propriété qui représente une part du capital d'une entreprise. En tant qu'actionnaire, vous possédez une portion de la société et avez droit à une part de ses bénéfices, appelée dividende. En cas de faillite complète de l'entreprise, l'actionnaire peut perdre la totalité de son capital investi (mais pas plus). Pour acheter ou vendre ces titres, on passe par la Bourse.", 
        "Si vous avez 100 actions d'une boîte qui en a 1000, vous possédez 10% de l'entreprise.", 5, 10, [
        ("multiple_choice", "Une action est un titre de :", ["Créance", "Propriété", "Assurance", "Garantie"], "Propriété", "Vous êtes co-propriétaire."),
        ("true_false", "On peut perdre plus que son investissement initial avec une action ?", None, "false", "Faux, au pire l'action vaut zéro."),
        ("multiple_choice", "Comment s'appelle la part du bénéfice versée aux actionnaires ?", ["L'impôt", "Le dividende", "Le coupon", "La commission"], "Le dividende", "C'est votre rémunération."),
        ("true_false", "La Bourse est le lieu principal d'échange des actions ?", None, "true", "Vrai.")
    ])
    add_lesson(m2.id, 2, "Dividendes vs Croissance", 
        "Il existe deux grandes approches : les actions de 'Croissance' (Growth) qui réinvestissent tous leurs profits pour se développer et les actions de 'Rendement' qui versent des dividendes réguliers. Une entreprise mature, qui a moins besoin de cash pour grandir, verse plus souvent des dividendes. Lors du versement d'un dividende, le prix de l'action baisse mécaniquement du montant versé.", 
        "Amazon a longtemps été 100% Croissance sans dividende. McDonald's est une action de Rendement.", 6, 12, [
        ("multiple_choice", "Une action de croissance privilégie :", ["Le dividende élevé", "Le réinvestissement des profits pour grandir", "La réduction du personnel", "Le sponsoring"], "Le réinvestissement des profits pour grandir", "Le but est la plus-value future."),
        ("true_false", "Une action sans dividende est forcément un mauvais placement ?", None, "false", "Faux, sa valeur peut exploser par ailleurs."),
        ("multiple_choice", "Pourquoi une entreprise mature verse-t-elle des dividendes ?", ["Elle est obligée", "Elle génère plus de cash qu'elle ne peut en réinvestir", "Pour faire baisser ses impôts", "Par erreur"], "Elle génère plus de cash qu'elle ne peut en réinvestir", "C'est signe de stabilité."),
        ("true_false", "Le prix de l'action baisse lors du versement du dividende ?", None, "true", "Vrai, c'est un ajustement comptable automatique.")
    ])
    add_lesson(m2.id, 3, "Risques spécifique vs marché", 
        "Le risque spécifique est propre à une seule entreprise. Le risque de marché (ou systémique) touche tout le monde, comme une hausse globale des prix (inflation). Pour se protéger du risque spécifique, la seule solution est la diversification : posséder de nombreuses actions de secteurs différents. Acheter un indice (via un ETF) est une méthode naturelle pour éliminer presque tout le risque spécifique.", 
        "Risque spécifique : Scandale chez Volkswagen. Risque marché : Crise financière de 2008.", 5, 12, [
        ("multiple_choice", "Comment réduire radicalement le risque spécifique ?", ["En pariant gros", "Par la diversification", "En vendant tout avant 17h", "En choisissant une banque rouge"], "Par la diversification", "Ne pas mettre tous ses œufs dans le même panier."),
        ("true_false", "On peut annuler le risque de marché en diversifiant bien ?", None, "false", "Faux, une récession touche tout le monde."),
        ("multiple_choice", "Lequel est un risque spécifique ?", ["Une hausse de l'inflation", "Un défaut technique sur un produit d'une marque", "Une guerre mondiale", "Une hausse des taux d'intérêt"], "Un défaut technique sur un produit d'une marque", "Cela ne touche que cette entreprise."),
        ("true_false", "Un ETF (indice) permet d'éliminer le risque spécifique ?", None, "true", "Vrai, car il contient des centaines d'entreprises.")
    ])

    # --- MODULE 3: LES ETF ---
    m3 = Module(title="Les ETF : investir simplement", description="Fonds indiciels", level="beginner", order=3, icon="📊")
    db.add(m3); db.flush()
    add_lesson(m3.id, 1, "Qu'est-ce qu'un ETF ?", 
        "Un ETF (Exchange Traded Fund) est un fonds qui recopie (réplique) la performance d'un indice boursier. L'avantage majeur est le coût : les frais de gestion passive sont bien plus bas que ceux des fonds classiques. Un ETF se vend et s'achète en bourse aussi simplement qu'une action individuelle. En un seul achat, vous obtenez une diversification immédiate.", 
        "Au lieu de choisir 40 actions françaises, vous achetez 1 ETF CAC 40.", 5, 12, [
        ("multiple_choice", "Pourquoi les frais d'un ETF sont-ils bas ?", ["Ils sont gérés par des bénévoles", "Moins de frais car c'est de la gestion passive (copie)", "C'est subventionné", "Ils ne paient pas de taxes"], "Moins de frais car c'est de la gestion passive (copie)", "On ne cherche pas à battre le marché."),
        ("true_false", "Un ETF peut s'acheter comme une simple action ?", None, "true", "Vrai, c'est l'un de ses grands avantages."),
        ("multiple_choice", "Que signifie 'répliquer' pour un ETF ?", ["Détruire l'indice", "Copier le plus fidèlement possible l'indice", "Vendre à découvert", "Doubler les gains"], "Copier le plus fidèlement possible l'indice", "C' mission."),
        ("true_false", "Un ETF est forcément moins diversifié qu'une action ?", None, "false", "Faux, il est par définition bien plus diversifié.")
    ])
    add_lesson(m3.id, 2, "Physique vs Synthétique", 
        "La réplication physique consiste à acheter réellement les actions de l'indice. La réplication synthétique utilise un contrat financier (swap) avec une banque. Cette technique comporte un léger risque de contrepartie, mais elle permet des avantages comme l'éligibilité au PEA pour des indices américains (S&P 500).", 
        "ETF Physique : Je possède vraiment l'action. ETF Synthétique : J'ai une promesse de gain via swap.", 6, 15, [
        ("multiple_choice", "La méthode la plus transparente est la réplication :", ["Imaginaire", "Physique", "Synthétique", "Spéculative"], "Physique", "Le fonds détient les vrais titres."),
        ("true_false", "Le synthétique permet d'avoir du S&P 500 (USA) en PEA ?", None, "true", "Vrai, c'est l'astuce légale principale."),
        ("multiple_choice", "Le risque propre au synthétique est le risque de :", ["Vol", "Contrepartie", "Péremption", "Logiciel"], "Contrepartie", "Lié au partenaire financier du contrat."),
        ("true_false", "Le physique a souvent un peu plus de frais internes de transaction ?", None, "true", "Vrai, car le fonds doit acheter/vendre réellement les titres.")
    ])
    add_lesson(m3.id, 3, "Acc vs Dist", 
        "Il existe deux versions d'ETF : Accumulation (Acc) et Distribution (Dist). L'ETF 'Acc' réinvestit automatiquement les dividendes reçus dans le fonds, ce qui maximise les intérêts composés. L'ETF 'Dist' vous verse le cash sur votre compte, ce qui est utile pour se créer une rente régulière.", 
        "Dist : Reçu 10€ de dividende. Acc : Mon ETF a monté de 10€ car il a tout racheté.", 5, 12, [
        ("multiple_choice", "Que signifie 'Acc' ?", ["Acceptation", "Accumulation (ou Capitalisation)", "Accord", "Actionnaire"], "Accumulation (ou Capitalisation)", "Le gain est accumulé."),
        ("true_false", "Un ETF 'Dist' est préférable pour une stratégie de rente ?", None, "true", "Vrai, car il vous donne du cash régulier."),
        ("multiple_choice", "Lequel maximise l'effet boule de neige ?", ["Dist", "Acc", "C'est pareil", "Aucun"], "Acc", "Grâce au réinvestissement automatique immédiat."),
        ("true_false", "Le passage Acc vers Dist est gratuit ?", None, "false", "Non, c'est une opération d'achat/vente classique.")
    ])

    # --- MODULE 4: LES INDICES ---
    m4 = Module(title="Les Indices Boursiers", description="Baromètres du marché", level="beginner", order=4, icon="🏎️")
    db.add(m4); db.flush()
    add_lesson(m4.id, 1, "Les grands indices mondiaux", 
        "Un indice est un point de repère qui mesure la performance d'un groupe d'actions. Le CAC 40 mesure les 40 plus grandes capitalisations françaises. Le S&P 500 suit les 500 plus grosses sociétés américaines. Le NASDAQ regroupe principalement les géants de la Technologie.", 
        "Le S&P 500 est le 'roi' des indices mondiaux.", 5, 10, [
        ("multiple_choice", "Combien d'entreprises contient le CAC 40 ?", ["10", "40", "100", "400"], "40", "C'est dans le nom !"),
        ("true_false", "Le NASDAQ est spécialisé dans le secteur technologique ?", None, "true", "Vrai, c'est là qu'on trouve la Tech US."),
        ("multiple_choice", "Quel est l'indice majeur au Japon ?", ["DAX 40", "S&P 500", "Nikkei 225", "FTSE 100"], "Nikkei 225", "L'indice de Tokyo."),
        ("true_false", "La liste des actions d'un indice peut changer avec le temps ?", None, "true", "Vrai, on fait du tri régulièrement.")
    ])
    add_lesson(m4.id, 2, "Poids et Capitalisation", 
        "La capitalisation boursière se calcule en multipliant le prix de l'action par le nombre total d'actions. Dans la plupart des indices, le poids d'une entreprise dépend de sa taille boursière. On utilise souvent la capitalisation 'flottante', qui exclut les actions non-échangeables.", 
        "Si Apple pèse 7%, une baisse de 10% d'Apple fait baisser l'indice de 0.7% à elle seule.", 6, 10, [
        ("multiple_choice", "Comment calcule-t-on la capitalisation boursière ?", ["Ventes * 10", "Prix action * Nombre actions", "Dette + Profit", "Nombre de salariés"], "Prix action * Nombre actions", "C'est la valeur de l'entreprise au marché."),
        ("true_false", "Une petite société peut facilement faire bouger le CAC 40 ?", None, "false", "Faux, son poids est minime par rapport aux géants."),
        ("multiple_choice", "Indice 'Equi-Weighted' signifie :", ["Poids par capitalisation", "Même poids pour toutes", "Poids par prix", "Poids par âge"], "Même poids pour toutes", "Chacune compte pareil."),
        ("true_false", "Le flottant exclut les actions détenues par les fondateurs ?", None, "true", "Vrai, on ne compte que ce qui circule sur le marché.")
    ])
    add_lesson(m4.id, 3, "Indices vs Gestion Active", 
        "L'indice suit son algorithme. La gestion active (un humain qui choisit les actions) est souvent battue par l'indice sur 10 ans car les frais de gestion mangent la performance. On mesure la fidélité d'un ETF via le 'Tracking Error'.", 
        "La gestion passive (ETF) gagne du terrain car elle est plus fiable et moins chère.", 5, 12, [
        ("multiple_choice", "Pourquoi est-il difficile de battre l'indice sur 10 ans ?", ["C'est interdit", "Les frais de gestion consomment les gains", "Les gérants sont malhonnêtes", "L'indice a des robots"], "Les frais de gestion consomment les gains", "Le gérant doit performer 2% de plus juste pour payer ses frais."),
        ("true_false", "Le Tracking Error mesure l'écart entre l'ETF et l'indice ?", None, "true", "Vrai, c'est l'erreur de suivi."),
        ("multiple_choice", "Les performances passées sont :", ["Un gage de sécurité future", "Une preuve de talent éternel", "Pas une garantie pour le futur", "Totalement inutiles"], "Pas une garantie pour le futur", "C'est l'avertissement standard en finance."),
        ("true_false", "L'indice ne fait jamais d'erreurs bêtes par rapport à un gérant ?", None, "false", "Faux, il peut suivre une bulle bêtement car sa règle est fixe.")
    ])

    # --- MODULE 5: ANALYSE FONDAMENTALE ---
    m5 = Module(title="Analyse Fondamentale", description="Santé des entreprises", level="intermediate", order=5, icon="🔍")
    db.add(m5); db.flush()
    add_lesson(m5.id, 1, "Le Compte de Résultat", 
        "Il résume l'activité économique. Le Chiffre d'Affaires (CA) est le montant total des ventes. L'EBITDA mesure la performance brute opérationnelle. Le Bénéfice Net est ce qu'il reste à la fin, après tout.", 
        "CA = 1M€. Charges = 800k€. Bénéfice = 200k€.", 7, 15, [
        ("multiple_choice", "Le Chiffre d'Affaires représente :", ["Le profit final", "Le total des ventes avant dépenses", "Le montant des impôts", "La dette"], "Le total des ventes avant dépenses", "Appelé aussi 'Top Line'."),
        ("true_false", "L'EBITDA permet de comparer la rentabilité opérationnelle ?", None, "true", "Vrai, en ignorant les différences de dettes et d'impôts."),
        ("multiple_choice", "Une entreprise avec un bénéfice net négatif est en :", ["Croissance", "Perte", "Richesse", "Sûreté"], "Perte", "Elle brûle son capital."),
        ("true_false", "Les dividendes sont payés à partir du bénéfice net ?", None, "true", "Vrai.")
    ])
    add_lesson(m5.id, 2, "Ratios : P/E et Yield", 
        "Le P/E (Price to Earnings) compare le prix au bénéfice annuel. Un P/E de 15 signifie qu'on paie 15 ans de profits. Le rendement (Yield) est le dividende divisé par le prix de l'action.", 
        "Action à 100€, gain de 5€ -> P/E de 20. Dividende 4€ -> Yield 4%.", 6, 15, [
        ("multiple_choice", "Que signifie un P/E de 10 ?", ["Le prix a baissé de 10%", "On paie l'action 10 fois son bénéfice annuel", "L'impôt est de 10%", "Le dividende est de 10%"], "On paie l'action 10 fois son bénéfice annuel", "Multiple de valorisation."),
        ("true_false", "Un P/E de 60 est typique d'une société à forte croissance ?", None, "true", "Vrai, on paie cher car on attend des profits futurs."),
        ("multiple_choice", "Un rendement (Yield) de 15% est généralement :", ["Un excellent signe sûr", "Un piège potentiel (Yield Trap)", "Impossible", "Réglé par la loi"], "Un piège potentiel (Yield Trap)", "Souvent l'action est en train de s'effondrer."),
        ("true_false", "Le P/E moyen historique est autour de 15-18 ?", None, "true", "Vrai.")
    ])
    add_lesson(m5.id, 3, "Dette et Cash-Flow", 
        "Le Free Cash Flow (FCF) est l'argent réel restant en caisse après charges et investissements. L'indicateur Dette Nette / EBITDA mesure la capacité de remboursement.", 
        "Une boîte peut annoncer 1M€ de profit mais avoir un cash-flow négatif si les clients n'ont pas encore payé.", 5, 15, [
        ("multiple_choice", "Qu'est-ce que le Free Cash Flow ?", ["L'argent distribué gratuitement", "L'argent réel restant après activités et investissements", "Le chiffre d'affaires", "La dette brute"], "L'argent réel restant après activités et investissements", "C'est la vraie richesse disponible."),
        ("true_false", "Une entreprise peut faire faillite en ayant des bénéfices comptables ?", None, "true", "Vrai, par crise de liquidité."),
        ("multiple_choice", "Le ratio Dette Nette / EBITDA permet d'évaluer :", ["Le nombre d'employés", "La solvabilité (capacité de remboursement)", "Le prix de l'action", "Le logo"], "La solvabilité (capacité de remboursement)", "Vital en période de crise."),
        ("true_false", "Racheter ses propres actions (Buyback) dote souvent le cours ?", None, "true", "Vrai, car cela réduit l'offre d'actions.")
    ])

    # --- MODULE 6: ECONOMIE ---
    m6 = Module(title="Bourse et Économie", description="L'environnement macro", level="intermediate", order=6, icon="🌍")
    db.add(m6); db.flush()
    add_lesson(m6.id, 1, "Inflation et Bourse", 
        "L'inflation est la hausse généralisée des prix. Les banques centrales la combattent en augmentant les taux d'intérêt. La stagflation est une inflation élevée avec une croissance négative. L'objectif standard est de 2%.", 
        "Si l'inflation est de 5%, votre billet de 100€ permet d'acheter 5% de choses en moins.", 5, 12, [
        ("multiple_choice", "L'inflation désigne la hausse de :", ["La richesse", "Des prix et la baisse du pouvoir d'achat", "Des impôts uniquement", "Des actions"], "Des prix et la baisse du pouvoir d'achat", "Dévaluation de la monnaie."),
        ("true_false", "L'inflation est néfaste pour les dettes à taux fixe (obligations) ?", None, "true", "Vrai, car le revenu futur vaudra moins cher."),
        ("multiple_choice", "Contre l'inflation, les banques centrales :", ["Offrent de l'argent", "Augmentent les taux directeurs", "Baissent les taux", "Ferment la Bourse"], "Augmentent les taux directeurs", "Pour 'refroidir' la machine économique."),
        ("true_false", "L'objectif d'inflation des banques centrales est de 2% ?", None, "true", "Vrai.")
    ])
    add_lesson(m6.id, 2, "Les Taux d'intérêt", 
        "Le taux d'intérêt est le prix de l'argent. Une hausse des taux rend l'emprunt plus cher et fait généralement baisser les actions. Le prix des obligations baisse quand les taux montent.", 
        "Taux hauts = Crédit immo cher -> Immobilier en baisse.", 6, 12, [
        ("multiple_choice", "Quelle banque gère le dollar ?", ["BCE", "FED", "ONU", "Banque Mondiale"], "FED", "La Federal Reserve US."),
        ("true_false", "Une hausse des taux stimule généralement la Bourse ?", None, "false", "Faux, elle l'inquiète car l'argent devient rare et cher."),
        ("multiple_choice", "Baisse des taux favorise généralement :", ["L'épargne", "L'emprunt et l'investissement", "La faillite", "Rien"], "L'emprunt et l'investissement", "Relance de la machine."),
        ("true_false", "Prix des obligations et taux d'intérêt évoluent en sens inverse ?", None, "true", "Vrai, c'est mécanique.")
    ])
    add_lesson(m6.id, 3, "Cycles Économiques", 
        "L'économie alterne entre expansion et récession (2 trimestres de baisse du PIB). On distingue les secteurs Défensifs (Santé) et Cycliques (Automobile).", 
        "Cycles typiques de 5-10 ans d'expansion suivis d'une purge.", 5, 12, [
        ("multiple_choice", "Définition d'une récession :", ["Un krach boursier", "2 trimestres de baisse du PIB", "Une grève", "L'inflation"], "2 trimestres de baisse du PIB", "Définition économique standard."),
        ("true_false", "Le secteur Défensif résiste mieux aux crises ?", None, "true", "Vrai, car ce sont des besoins primaires essentiels."),
        ("multiple_choice", "Secteur typiquement cyclique :", ["L'Eau", "L'Automobile", "La Santé", "L'Électricité"], "L'Automobile", "On reporte l'achat si on est inquiet."),
        ("true_false", "La Bourse monte et descend toujours après l'économie réelle ?", None, "false", "Faux, elle est souvent un indicateur avancé.")
    ])

    # --- MODULE 7: PSYCHOLOGIE ---
    m7 = Module(title="Psychologie de l'investisseur", description="Éviter les pièges", level="intermediate", order=7, icon="🧠")
    db.add(m7); db.flush()
    add_lesson(m7.id, 1, "Biais et Émotions", 
        "La peur et la cupidité dictent trop souvent nos choix. Le FOMO (Fear Of Missing Out) est la peur de rater une opportunité. L'aversion à la perte rend la douleur d'une perte plus forte que la joie d'un gain.", 
        "Vendre ses actions en panique lors d'un krach.", 7, 15, [
        ("multiple_choice", "Qu'est-ce que le FOMO ?", ["Une nouvelle monnaie", "La peur de rater une opportunité", "Un type d'assurance", "Un indice boursier"], "La peur de rater une opportunité", "Fear Of Missing Out."),
        ("true_false", "La douleur d'une perte est plus forte que la joie d'un gain ?", None, "true", "Vrai, c'est l'aversion à la perte."),
        ("multiple_choice", "Le biais de confirmation consiste à :", ["Vérifier ses comptes", "Chercher uniquement des infos confortant notre avis", "Oublier de vendre", "Acheter au pif"], "Chercher uniquement des infos confortant notre avis", "On s'interdit de voir la réalité."),
        ("true_false", "La discipline est plus importante que l'instinct en bourse ?", None, "true", "Vrai.")
    ])
    add_lesson(m7.id, 2, "Discipline : DCA", 
        "Le DCA (Dollar Cost Averaging) consiste à investir une somme fixe à intervalles réguliers. Cela lisse le prix d'achat et élimine le stress du timing.", 
        "Investir 100€ chaque 1er du mois pendant 10 ans.", 6, 15, [
        ("multiple_choice", "Quel est l'avantage clé du DCA ?", ["Gagner 50% par an", "Lisser son prix de revient et supprimer le stress", "Ne pas payer d'impôts", "Devenir célèbre"], "Lisser son prix de revient et supprimer le stress", "Le timing n'est plus un sujet."),
        ("true_false", "Le DCA permet d'acheter au 'pire' moment ?", None, "false", "Faux, il permet d'éviter de mettre tout son capital au plus haut."),
        ("multiple_choice", "Que faire si la bourse baisse de 10% quand on fait du DCA ?", ["Tout vendre par peur", "Continuer son investissement régulier", "Attendre 3 ans", "Changer de banque"], "Continuer son investissement régulier", "C'est là qu'on accumule le plus."),
        ("true_false", "Même 50€ par mois sont utiles en investissement régulier ?", None, "true", "Vrai, la régularité est reine.")
    ])

    # --- MODULE 8: STRATEGIES ---
    m8 = Module(title="Stratégies Actions", description="Value, Growth, Quality", level="intermediate", order=8, icon="🏹")
    db.add(m8); db.flush()
    add_lesson(m8.id, 1, "Value vs Growth", 
        "L'investisseur Value cherche des actions décotées ( Warren Buffett). L'investisseur Growth mise sur les secteurs d'avenir (Tech).", 
        "Acheter une banque (Value) vs acheter du Cloud / IA (Growth).", 6, 12, [
        ("multiple_choice", "Que recherche l'investisseur Value ?", ["La boîte la plus à la mode", "Une action décotée par rapport à sa valeur réelle", "Une action très chère", "Des cryptos anonymes"], "Une action décotée par rapport à sa valeur réelle", "Il cherche des entreprises 'en soldes'."),
        ("true_false", "La Tech (logiciels, IA) est typiquement du 'Growth' ?", None, "true", "Vrai, on mise sur la croissance exponentielle."),
        ("multiple_choice", "En période d'inflation et de taux hauts, quel style résiste mieux ?", ["Growth", "Value", "Startup", "Spéculation"], "Value", "Les investisseurs reviennent vers les profits concrets."),
        ("true_false", "Value et Growth sont deux styles qui se complètent ?", None, "true", "Vrai, il est utile d'avoir les deux.")
    ])
    add_lesson(m8.id, 2, "Dividendes", 
        "Un 'Dividend Aristocrat' augmente son dividende depuis 25+ ans. Le Payout Ratio est la part du bénéfice reversée.", 
        "L'Oréal ou Sanofi sont des payeurs de dividendes réguliers.", 6, 15, [
        ("multiple_choice", "Qu'est-ce qu'un Dividend Aristocrat ?", ["Une banque suisse", "Une société augmentant son dividende depuis 25+ ans", "Une boîte appartenant à l'État", "Une société agricole"], "Une société augmentant son dividende depuis 25+ ans", "Preuve de santé long-terme."),
        ("true_false", "Le Payout Ratio de 150% est un bon signe ?", None, "false", "Faux, l'entreprise s'endette."),
        ("multiple_choice", "Un rendement anormalement élevé est souvent :", ["Une chance inouïe", "Un danger de coupure (Yield Trap)", "Regulé par l'État", "Le signe d'un don"], "Un danger de coupure (Yield Trap)", "Le prix baisse car le marché a peur."),
        ("true_false", "Réinvestir les dividendes booste la performance ?", None, "true", "Vrai, c'est l'accélérateur ultime.")
    ])
    add_lesson(m8.id, 3, "Quality", 
        "On cherche des entreprises avec un 'Moat' (rempart concurrentiel) et un 'Pricing Power'.", 
        "Moat d'Apple : Son écosystème fermé.", 5, 12, [
        ("multiple_choice", "Qu'est-ce qu'un 'Moat' ?", ["Un château fort", "Un avantage concurrentiel durable", "Une dette de banque", "Un type d'action"], "Un avantage concurrentiel durable", "Le rempart qui protège les profits."),
        ("true_false", "LVMH possède un fort Pricing Power ?", None, "true", "Vrai."),
        ("multiple_choice", "Un critère financier de 'Qualité' est :", ["Dette élevée", "Marges bénéficiaires fortes", "Plus de 1000 bureaux", "Ancienneté du PDG"], "Marges bénéficiaires fortes", "Preuve de valeur ajoutée."),
        ("true_false", "Investir en 'Qualité' signifie ignorer totalement le prix d'achat ?", None, "false", "Faux.")
    ])

    # --- MODULE 9: RISQUES ---
    m9 = Module(title="Risques et Volatilité", description="Gérer les tempêtes", level="intermediate", order=9, icon="🌊")
    db.add(m9); db.flush()
    add_lesson(m9.id, 1, "Comprendre la Volatilité", 
        "La volatilité mesure les variations rapides du prix. L'indice VIX (indice de la peur) la mesure.", 
        "Une action qui fait +2% puis -3% en 2 jours est volatile.", 5, 10, [
        ("multiple_choice", "Que mesure la volatilité ?", ["Le profit net", "L'ampleur des variations de prix", "La taxe d'achat", "L'âge du courtier"], "L'ampleur des variations de prix", "Indique si l'actif est 'nerveux'."),
        ("true_false", "La volatilité est synonyme de perte d'argent ?", None, "false", "Faux, tant qu'on n'a pas vendu."),
        ("multiple_choice", "Comment s'appelle l'indice mesurant la peur/volatilité ?", ["NASDAQ", "VIX", "S&P", "EURO"], "VIX", "Volatility Index."),
        ("true_false", "Le temps réduit l'impact psychologique de la volatilité ?", None, "true", "Vrai.")
    ])
    add_lesson(m9.id, 2, "Drawdown et Récupération", 
        "Le 'Drawdown' est la chute depuis le plus haut. Si vous perdez 50%, il faut +100% pour récupérer.", 
        "Chute de 50€ à 25€ (-50%). Pour remonter à 50€, il faut faire +100%.", 6, 10, [
        ("multiple_choice", "Pour compenser une perte de 50%, il faut gagner :", ["50%", "100%", "25%", "10%"], "100%", "Les mathématiques sont asymétriques."),
        ("true_false", "Un drawdown est la chute depuis le plus haut ?", None, "true", "Vrai."),
        ("multiple_choice", "Comment limiter son drawdown maximal ?", ["Parier sur 1 seule action", "Diversifier ses actifs", "Vendre dès que ça perd 1%", "Prier"], "Diversifier ses actifs", "En mélangeant des actifs."),
        ("true_false", "La Bourse a historiquement toujours récupéré ses drawdowns sur 20 ans ?", None, "true", "Vrai.")
    ])

    # --- MODULE 10: FISCALITE ---
    m10 = Module(title="Fiscalité", description="Optimisez vos gains", level="intermediate", order=10, icon="🏛️")
    db.add(m10); db.flush()
    add_lesson(m10.id, 1, "Le PEA", 
        "Exonération d'impôt sur le revenu après 5 ans (seuls les 17,2% de PS restent). Limité à 150 000€.", 
        "Gains de 1000€ -> Dans PEA (5 ans) vous gardez 828€.", 6, 15, [
        ("multiple_choice", "Quel est l'avantage du PEA après 5 ans ?", ["Gratuité totale", "Pas d'impôt sur le revenu (17,2% PS seuls)", "Bonus fixe", "Aucun"], "Pas d'impôt sur le revenu (17,2% PS seuls)", "Économie de 12,8%."),
        ("true_false", "On peut avoir 3 PEA ?", None, "false", "Faux, 1 seul."),
        ("multiple_choice", "Quelle est la limite de versements sur un PEA ?", ["10 000€", "150 000€", "500 000€", "Aucune"], "150 000€", "Plafond légal."),
        ("true_false", "Peut-on mettre des actions Google en direct dans le PEA ?", None, "false", "Faux, réservé aux titres européens.")
    ])
    add_lesson(m10.id, 2, "CTO et Flat Tax", 
        "Flat Tax (PFU) de 30% par défaut (12,8% IR + 17,2% PS). Liberté géographique totale.", 
        "Vendre Nvidia avec 1000€ de gain -> 300€ d'impôt.", 5, 12, [
        ("multiple_choice", "Quel est le montant de la Flat Tax en France ?", ["20%", "30%", "40%", "15%"], "30%", "Prélèvement forfaitaire unique."),
        ("true_false", "Le CTO permet d'acheter des actions sans limite géographique ?", None, "true", "Vrai."),
        ("multiple_choice", "Dans les 30%, quelle part revient aux prélèvements sociaux ?", ["10%", "17,2%", "12,8%", "5%"], "17,2%", "Base incompressible."),
        ("true_false", "On peut choisir le barème progressif si c'est avantageux ?", None, "true", "Vrai.")
    ])

    # --- MODULE 11: CONSTRUCTION ---
    m11 = Module(title="Construction Portefeuille", description="Core-Satellite", level="intermediate", order=11, icon="🎨")
    db.add(m11); db.flush()
    add_lesson(m11.id, 1, "Core-Satellite", 
        "80% dans un socle diversifié (Core) et 20% dans des paris thématiques (Satellites).", 
        "Core (ETF World) + Satellites (LVMH + Tesla).", 7, 15, [
        ("multiple_choice", "Quel est le rôle du 'Core' ?", ["La spéculation pure", "Le socle solide et diversifié", "Parier sur l'or", "Ne servir à rien"], "Le socle solide et diversifié", "Ancre du navire."),
        ("true_false", "La majorité du portefeuille devrait être dans les Satellites ?", None, "false", "Faux."),
        ("multiple_choice", "Lequel est un candidat idéal pour le 'Core' ?", ["Une crypto montante", "Un ETF MSCI World", "Une action de start-up", "Une option"], "Un ETF MSCI World", "Couverture large."),
        ("true_false", "Cette méthode mélange sécurité et convictions ?", None, "true", "Vrai.")
    ])
    add_lesson(m11.id, 2, "Rééquilibrage", 
        "Ajuster les poids pour revenir à l'allocation cible (vendre haut, acheter bas).", 
        "Vendre des actions pour racheter des obligations.", 6, 12, [
        ("multiple_choice", "Pourquoi rééquilibrer un portefeuille ?", ["Pour payer plus de frais", "Pour maintenir son profil de risque cible", "Pour tout recommencer", "Parce que c'est la loi"], "Pour maintenir son profil de risque cible", "Discipline saine."),
        ("true_false", "Rééquilibrer force souvent à vendre ses 'gagnants' ?", None, "true", "Vrai."),
        ("multiple_choice", "Fréquence recommandée ?", ["Tous les jours", "1 à 2 fois par an", "Tous les 10 ans", "Jamais"], "1 à 2 fois par an", "C'est suffisant."),
        ("true_false", "Le rééquilibrage est une méthode de discipline automatique ?", None, "true", "Vrai.")
    ])

    # --- MODULE 12: PASSER A L'ACTION ---
    m12 = Module(title="Passer à l'action", description="Étapes concrètes", level="beginner", order=12, icon="🚀")
    db.add(m12); db.flush()
    add_lesson(m12.id, 1, "Ouvrir son compte", 
        "Choisir entre PEA, CTO ou Assurance-Vie. Vérifier les frais et l'agrément AMF.", 
        "Choisir un courtier en ligne sérieux.", 6, 10, [
        ("multiple_choice", "Quelle enveloppe offre des avantages après 8 ans ?", ["Livret A", "Assurance-Vie", "Compte Courant", "Carton"], "Assurance-Vie", "Fiscalité douce."),
        ("true_false", "On peut investir en bourse avec 50€ par mois ?", None, "true", "Vrai."),
        ("multiple_choice", "Que faut-il vérifier en priorité chez un courtier ?", ["La publicité", "Les frais et l'agrément AMF", "Le nom", "La météo"], "Les frais et l'agrément AMF", "Sécurité."),
        ("true_false", "On peut posséder à la fois un PEA et un CTO ?", None, "true", "Vrai.")
    ])
    add_lesson(m12.id, 2, "Premier investissement", 
        "Acheter un ETF diversifié et tenir. Le meilleur moment est aujourd'hui (Time in the market).", 
        "Acheter sa première part d'ETF World.", 7, 15, [
        ("multiple_choice", "Meilleure action pour débuter ?", ["Parier sur 1 startup", "Acheter un ETF diversifié et tenir", "Vendre tout", "Acheter au pif"], "Acheter un ETF diversifié et tenir", "Efficacité prouvée."),
        ("true_false", "L'investissement est un sprint ?", None, "false", "Faux, marathon."),
        ("multiple_choice", "Source d'information recommandée ?", ["Rumeurs de café", "Academy et sites officiels", "Influenceurs", "Rien"], "Academy et sites officiels", "Factuel."),
        ("true_false", "Commencer aujourd'hui est mieux que d'attendre demain ?", None, "true", "Vrai.")
    ])

    db.commit()
    print("✅ Full curriculum seeded successfully (12 modules).")
    return True
