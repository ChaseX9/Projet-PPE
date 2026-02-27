"""
Final Professional Curriculum for CapInvest Academy.
33 Lessons, 130+ Questions.
Focus: Stocks and ETFs.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed_complete_curriculum():
    session = Session()
    session.query(Question).delete()
    session.query(Lesson).delete()
    session.query(Module).delete()

    # --- MODULE 1: LES BASES (4 leçons) ---
    m1 = Module(title="Les bases de l'investissement", description="Fondamentaux pour bien débuter", level="beginner", order=1, icon="🎯")
    session.add(m1); session.flush()
    add_lesson(session, m1.id, 1, "Qu'est-ce qu'investir ?", 
        "Investir consiste à mettre votre argent au travail pour générer des revenus ou faire fructifier votre capital sur le long terme. Contrairement à l'épargne (qui dort), l'investissement cherche à battre l'inflation pour préserver et augmenter votre pouvoir d'achat.", 
        "Placer 1000€ sur un livret à 3% alors que l'inflation est à 5% vous fait perdre de l'argent 'réel'.", 5, 10, [
        ("multiple_choice", "Quelle est la différence majeure entre épargne et investissement ?", ["Le montant minimum", "Le risque et le potentiel de gain", "La banque utilisée", "La couleur de la carte"], "Le risque et le potentiel de gain", "L'investissement comporte un risque mais offre un rendement supérieur."),
        ("true_false", "Investir aide à lutter contre l'inflation ?", None, "true", "Vrai, c'est l'un des objectifs principaux."),
        ("multiple_choice", "Quelles sont les deux composantes du rendement ?", ["Le CA et la dette", "Les dividendes et les impôts", "La plus-value et les revenus (intérêts/dividendes)", "Le capital et le staff"], "La plus-value et les revenus (intérêts/dividendes)", "Le rendement total est la somme des deux."),
        ("true_false", "Peut-on devenir riche sans prendre aucun risque ?", None, "false", "Faux, le rendement est la rémunération du risque.")
    ])
    add_lesson(session, m1.id, 2, "Risque / Rendement", 
        "Il n'existe pas de rendement élevé sans risque élevé. C'est la loi fondamentale de la finance. Le risque se manifeste souvent par la volatilité (le prix qui bouge). Pour accepter ce risque, l'investisseur demande une 'prime de rendement'.", 
        "Les actions sont plus risquées que les obligations, donc elles rapportent historiquement plus.", 6, 10, [
        ("multiple_choice", "Lequel de ces actifs est statistiquement le moins risqué ?", ["Actions technologiques", "Obligations d'État stables", "Cryptomonnaies", "Immobilier commercial"], "Obligations d'État stables", "C'est la base de la sécurité en finance."),
        ("true_false", "Prendre plus de risque garantit un rendement plus élevé ?", None, "false", "Faux, cela augmente seulement le potentiel, pas la certitude."),
        ("multiple_choice", "Pourquoi un actif risqué doit-il rapporter plus ?", ["Pour payer les impôts", "Pour compenser l'incertitude (prime de risque)", "Parce que c'est la loi", "Pour payer les brokers"], "Pour compenser l'incertitude (prime de risque)", "C'est l'incitation à investir."),
        ("true_false", "La volatilité (le prix qui bouge) est une forme de risque ?", None, "true", "Vrai, c'est le risque de timing.")
    ])
    add_lesson(session, m1.id, 3, "Horizon de placement", 
        "Le temps est votre meilleur allié. Plus vous investissez sur le long terme, plus vous lissez les hauts et les bas des marchés. Un horizon de 5 à 10 ans est souvent recommandé pour les actions afin de laisser passer les crises passagères.", 
        "Un investisseur qui a tenu ses positions pendant la crise de 2008 a récupéré tout son capital et plus encore en quelques années.", 5, 10, [
        ("multiple_choice", "Quel est l'horizon recommandé pour investir en actions ?", ["Quelques mois", "1 à 2 ans", "Minimum 5 à 10 ans", "Un weekend"], "Minimum 5 à 10 ans", "Pour lisser la volatilité des marchés."),
        ("true_false", "Un jeune actif peut prendre plus de risques qu'un futur retraité ?", None, "true", "Vrai, car il a le temps de se refaire."),
        ("multiple_choice", "Que se passe-t-il si vous devez retirer votre argent pendant une baisse ?", ["Vous gagnez un bonus", "Vous matérialisez votre perte", "La banque vous rembourse", "Rien"], "Vous matérialisez votre perte", "La perte devient réelle au moment de la vente."),
        ("true_false", "Investir pour 20 ans garantit un risque zéro ?", None, "false", "Faux, le risque existe toujours, il est juste mieux géré.")
    ])
    add_lesson(session, m1.id, 4, "Intérêts composés", 
        "Albert Einstein les appelait la 'huitième merveille du monde'. Le principe est simple : vos gains génèrent eux-mêmes des gains. Sur une longue période, l'effet devient exponentiel. C'est le secret de la fortune sur le long terme.", 
        "Investir 100€ par mois à 7% pendant 30 ans transforme 36 000€ en plus de 120 000€.", 7, 15, [
        ("multiple_choice", "Qu'est-ce que l'effet 'boule de neige' ?", ["Le froid en bourse", "Le réinvestissement des gains qui génèrent de nouveaux gains", "L'accumulation de dettes", "La diversification"], "Le réinvestissement des gains qui génèrent de nouveaux gains", "C'est le moteur des intérêts composés."),
        ("true_false", "Il vaut mieux commencer tôt avec peu que tard avec beaucoup ?", None, "true", "Vrai, car la durée est le facteur le plus puissant."),
        ("multiple_choice", "Quel est le facteur le plus déterminant sur 30 ans ?", ["Le montant du premier versement", "La banque choisie", "La durée totale de l'investissement", "La météo"], "La durée totale de l'investissement", "La croissance est exponentielle avec le temps."),
        ("true_false", "Les intérêts composés fonctionnent aussi pour les dettes ?", None, "true", "Vrai, d'où l'importance de les rembourser vite.")
    ])

    # --- MODULE 2: COMPRENDRE LES ACTIONS (3 leçons) ---
    m2 = Module(title="Comprendre les actions", description="Maîtrisez les actions et leur rôle", level="beginner", order=2, icon="📈")
    session.add(m2); session.flush()
    add_lesson(session, m2.id, 1, "C'est quoi une action ?", 
        "Une action est une part du capital d'une entreprise. En devenant actionnaire, vous devenez copropriétaire. Vous avez droit à une partie des bénéfices (dividendes) et vous pouvez voter lors des assemblées générales.", 
        "Acheter une action L'Oréal, c'est posséder une petite partie de leurs usines et de leurs marques.", 5, 10, [
        ("multiple_choice", "Que possédez-vous concrètement avec une action ?", ["Un prêt à l'entreprise", "Un titre de propriété (une part du capital)", "Une garantie bancaire", "Un produit gratuit"], "Un titre de propriété (une part du capital)", "C'est de l'equity (fonds propres)."),
        ("true_false", "Toutes les entreprises versent obligatoirement des dividendes ?", None, "false", "Faux, c'est une décision de l'entreprise."),
        ("multiple_choice", "Où s'échangent les actions ?", ["À la banque centrale", "À la Bourse", "Dans un magasin", "Sur LeBonCoin"], "À la Bourse", "C'est le marché secondaire."),
        ("true_false", "En cas de faillite, l'actionnaire est remboursé en premier ?", None, "false", "Faux, il est remboursé en dernier.")
    ])
    add_lesson(session, m2.id, 2, "Dividendes vs Croissance", 
        "Il y a deux façons de gagner : soit le prix de l'action monte (Croissance), soit l'entreprise vous reverse du cash (Dividende). Les entreprises 'Growth' réinvestissent tout pour grandir, tandis que les entreprises 'Value/Matures' chouchoutent leurs actionnaires avec du cash.", 
        "Amazon a longtemps été une action de croissance pure, tandis que Coca-Cola est une action à dividende.", 6, 12, [
        ("multiple_choice", "Quelle est la caractéristique d'une action 'Growth' ?", ["Elle verse un gros dividende", "Elle réinvestit ses profits pour croître davantage", "Elle appartient au gouvernement", "Son prix est fixe"], "Elle réinvestit ses profits pour croître davantage", "On mise sur la plus-value future."),
        ("true_false", "Une entreprise qui ne verse pas de dividende est forcément mauvaise ?", None, "false", "Faux, elle peut créer plus de valeur en réinvestissant."),
        ("multiple_choice", "Pourquoi une entreprise mûre verse-t-elle des dividendes ?", ["Elle n'a plus de relais de croissance massive", "C'est illégal de garder le cash", "Pour faire baisser son cours", "Pour punir les actionnaires"], "Elle n'a plus de relais de croissance massive", "Elle partage la richesse générée."),
        ("true_false", "Les 'Aristocrates du dividende' les augmentent depuis des décennies ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m2.id, 3, "Risques spécifique/marché", 
        "Il y a deux types de risques : le risque spécifique (lié à une seule entreprise, ex: une grève) et le risque de marché (lié à l'économie globale, ex: une épidémie). La diversification permet d'éliminer le premier, pas le second.", 
        "Si vous n'avez que du Air France et que le COVID arrive, vous perdez tout. Si vous avez 500 actions, l'impact est limité.", 5, 12, [
        ("multiple_choice", "Pourquoi ne faut-il pas tout mettre sur une seule action ?", ["Pour payer plus de frais", "Pour diversifier et réduire le risque spécifique", "Pour faire du trading", "Pour parier plus"], "Pour diversifier et réduire le risque spécifique", "C'est la protection de base."),
        ("true_false", "Posséder 10 actions du même secteur est une bonne diversification ?", None, "false", "Faux, elles risquent de chuter ensemble."),
        ("multiple_choice", "Qu'est-ce qu'un risque de marché ?", ["Une panne informatique chez Amazon", "Une hausse généralisée de l'inflation", "Un bug sur l'iPhone", "Le départ du PDG de Total"], "Une hausse généralisée de l'inflation", "Cela touche tout le monde."),
        ("true_false", "La diversification supprime-t-elle le risque de krach boursier ?", None, "false", "Faux, le risque systémique reste.")
    ])

    # --- MODULE 3: LES ETF (3 leçons) ---
    m3 = Module(title="Les ETF : investir simplement", description="Fonds indiciels", level="beginner", order=3, icon="📊")
    session.add(m3); session.flush()
    add_lesson(session, m3.id, 1, "Qu'est-ce qu'un ETF ?", 
        "Un ETF (Exchange Traded Fund) ou tracker est un fonds qui suit un indice (comme le CAC 40). En achetant une part d'ETF, vous achetez d'un coup des centaines d'actions. Les frais sont minuscules car c'est un ordinateur qui gère le fonds.", 
        "L'ETF MSCI World vous permet de posséder les 1500 plus grandes entreprises mondiales en un clic.", 5, 12, [
        ("multiple_choice", "Pourquoi les frais des ETF sont-ils si bas ?", ["Ils sont faits en papier", "Ils copient juste un indice (gestion passive)", "Ils sont réservés aux riches", "Ils ne paient pas d'impôts"], "Ils copient juste un indice (gestion passive)", "Pas de gérants d'étoiles à payer."),
        ("true_false", "Un ETF s'achète et se vend aussi facilement qu'une action ?", None, "true", "Vrai, en quelques secondes sur votre appli."),
        ("multiple_choice", "Quel est l'objectif d'un ETF indiciel ?", ["Battre le marché", "Copier exactement la performance de son indice", "Ignorer les baisses", "Supprimer les dividendes"], "Copier exactement la performance de son indice", "C'est la réplication."),
        ("true_false", "Un ETF est plus risqué qu'une seule action ?", None, "false", "Faux, la diversification réduit le risque.")
    ])
    add_lesson(session, m3.id, 2, "Physique vs Synthétique", 
        "Il y a deux façons pour un ETF de copier l'indice : soit il achète vraiment les actions (Physique), soit il utilise un contrat financier avec une banque (Synthétique). Le synthétique est souvent utilisé pour accéder à des marchés étrangers via un PEA.", 
        "Un ETF S&P 500 synthétique permet d'avoir des actions US dans son PEA français.", 6, 15, [
        ("multiple_choice", "Quelle méthode est la plus transparente ?", ["La réplication synthétique", "La réplication physique", "La réplication imaginaire", "Le trading spéculatif"], "La réplication physique", "On possède réellement les titres."),
        ("true_false", "Les ETF synthétiques permettent d'avoir du US en PEA ?", None, "true", "Vrai, c'est leur grand avantage fiscal."),
        ("multiple_choice", "Quel est le petit risque supplémentaire du synthétique ?", ["Le risque d'entreprise", "Le risque de contrepartie (faillite du partenaire)", "Le risque de vol", "Le risque météo"], "Le risque de contrepartie (faillite du partenaire)", "Très surveillé et limité."),
        ("true_false", "La réplication physique a souvent plus de frais internes de transaction ?", None, "true", "Vrai, car elle doit acheter/vendre les vrais titres.")
    ])
    add_lesson(session, m3.id, 3, "Acc vs Dist", 
        "Le choix crucial : soit l'ETF vous verse les dividendes sur votre compte (Dist), soit il les réinvestit automatiquement dans le fonds (Acc). Pour faire grossir votre capital vite, le mode Accumulation est le plus puissant.", 
        "Un ETF World Acc transformera vos dividendes en nouvelles parts sans que vous n'ayez rien à faire.", 5, 12, [
        ("multiple_choice", "Que fait un ETF de type 'Acc' ?", ["Il distribue le cash", "Il réinvestit automatiquement les dividendes", "Il garde l'argent pour lui", "C'est une assurance"], "Il réinvestit automatiquement les dividendes", "Idéal pour capitaliser."),
        ("true_false", "L'ETF distribuant est plus efficace fiscalement pour capitaliser ?", None, "false", "Faux, car chaque versement peut être taxé."),
        ("multiple_choice", "Quel suffixe indique qu'un ETF reverse les dividendes ?", ["Acc", "Dist", "Ret", "Grow"], "Dist", "Pour Distribuant."),
        ("true_false", "Les intérêts composés sont maximisés avec un ETF Acc ?", None, "true", "Vrai.")
    ])

    # --- MODULE 4: INDICES (3 leçons) ---
    m4 = Module(title="Les Indices Boursiers", description="Comprendre les baromètres du marché", level="beginner", order=4, icon="🏎️")
    session.add(m4); session.flush()
    add_lesson(session, m4.id, 1, "Les grands indices mondiaux", 
        "Un indice est un panier d'actions représentatif d'une économie. Le CAC 40 mesure la France, le S&P 500 les USA, et le MSCI World les pays développés. Ils servent de thermomètre pour savoir si 'la bourse' monte ou descend.", 
        "Si le S&P 500 monte de 2%, c'est que les 500 plus grosses boîtes US ont globalement progressé.", 5, 10, [
        ("multiple_choice", "Quel indice regroupe les 500 plus grosses entreprises américaines ?", ["CAC 40", "S&P 500", "DAX", "Nikkei"], "S&P 500", "Standard & Poor's 500."),
        ("true_false", "Le CAC 40 représente toute l'économie française ?", None, "false", "Faux, il ne contient que les 40 plus grandes capitalisations."),
        ("multiple_choice", "Quel indice est fortement orienté vers la Technologie ?", ["S&P 500", "NASDAQ", "Dow Jones", "CAC 40"], "NASDAQ", "Le temple de la Tech US."),
        ("true_false", "La composition d'un indice change régulièrement ?", None, "true", "Vrai, on sort les perdants et on rentre les nouveaux champions.")
    ])
    add_lesson(session, m4.id, 2, "Poids et Capitalisation", 
        "Les indices ne traitent pas toutes les entreprises pareil. Plus une entreprise est grosse (capitalisation boursière élevée), plus elle pèse lourd dans l'indice. Si Apple baisse de 2%, le S&P 500 bougera beaucoup plus que si une petite entreprise baisse de 10%.", 
        "Apple et Microsoft pèsent à elles seules près de 15% du S&P 500.", 6, 10, [
        ("multiple_choice", "Que signifie un poids par capitalisation ?", ["Toutes les entreprises sont à égalité", "Les plus grosses entreprises ont plus d'impact", "Les plus petites ont plus de poids", "C'est par ordre alphabétique"], "Les plus grosses entreprises ont plus d'impact", "C'est la méthode standard."),
        ("true_false", "Une chute de la plus grosse action impacte fortement l'indice ?", None, "true", "Vrai, c'est l'effet de concentration."),
        ("multiple_choice", "Qu'est-ce qu'un indice 'Equi-Weighted' ?", ["Même poids pour chaque action", "Poids par prix de l'action", "Poids par âge de la boîte", "Pas de poids"], "Même poids pour chaque action", "Chaque entreprise compte pour le même pourcentage (ex: 2% pour 50 actions)."),
        ("true_false", "La capitalisation = prix x nombre d'actions ?", None, "true", "Vrai, c'est la valeur de marché totale.")
    ])
    add_lesson(session, m4.id, 3, "Indices vs Gestion Active", 
        "La gestion passive (ETF) consiste à copier l'indice. La gestion active consiste à essayer de le battre en choisissant des titres. Statistiquement, sur 10 ans, plus de 80% des gérants actifs ne parviennent pas à battre leur indice de référence à cause des frais et des erreurs de jugement.", 
        "Les statistiques SPIVA montrent la difficulté de battre durablement le marché.", 5, 12, [
        ("multiple_choice", "Pourquoi la gestion passive gagne-t-elle souvent sur le long terme ?", ["Parce qu'elle a plus de chance", "Grâce aux frais très bas et à la discipline", "Parce que l'informatique est magique", "Elle ne gagne jamais"], "Grâce aux frais très bas et à la discipline", "Les frais mangent la performance."),
        ("true_false", "Les frais de gestion expliquent la sous-performance des gérants ?", None, "true", "Vrai, c'est un vent contraire permanent."),
        ("multiple_choice", "Qu'est-ce que la 'Tracking Error' ?", ["Une erreur de la bourse", "L'écart entre la performance de l'ETF et son indice", "Une panne informatique", "Une erreur fiscale"], "L'écart entre la performance de l'ETF et son indice", "On cherche la Tracking Error la plus faible possible."),
        ("true_false", "L'indice fait toujours les meilleurs choix ?", None, "false", "Faux, il ne choisit pas, il suit une règle mécanique.")
    ])

    # --- MODULE 5: ANALYSE FONDAMENTALE (3 leçons) ---
    m5 = Module(title="Analyse Fondamentale", description="Déchiffrer la santé des entreprises", level="intermediate", order=5, icon="🔍")
    session.add(m5); session.flush()
    add_lesson(session, m5.id, 1, "Le Compte de Résultat", 
        "C'est le film de l'année pour l'entreprise. Il montre son Chiffre d'Affaires (ce qu'elle vend), ses charges (ce qu'elle dépense) et son Bénéfice Net (ce qui reste). C'est là qu'on voit si une entreprise est réellement rentable.", 
        "Amazon a longtemps eu un CA géant mais peu de bénéfice car il réinvestissait tout.", 7, 15, [
        ("multiple_choice", "Qu'est-ce que le Chiffre d'Affaires (CA) ?", ["Le gain final", "Le montant total des ventes", "La dette", "Le stock"], "Le montant total des ventes", "C'est la 'Top Line'."),
        ("true_false", "Une entreprise peut avoir un CA record mais faire des pertes ?", None, "true", "Vrai, si ses dépenses sont supérieures à ses ventes."),
        ("multiple_choice", "D'où provient l'argent des dividendes ?", ["Du CA", "Du Bénéfice Net (ou des réserves)", "Des impôts", "Des salaires"], "Du Bénéfice Net (ou des réserves)", "C'est la part du profit partagée."),
        ("true_false", "L'EBITDA permet de comparer la rentabilité opérationnelle ?", None, "true", "Vrai, avant intérêts et impôts.")
    ])
    add_lesson(session, m5.id, 2, "Ratios : P/E et Yield", 
        "Comment savoir si une action est chère ? Le P/E (Price-to-Earnings) compare le prix au bénéfice. Un P/E de 20 signifie que vous payez l'équivalent de 20 ans de bénéfices. Le Yield est le rendement du dividende par rapport au prix actuel.", 
        "Une action à 100€ qui gagne 5€/an a un P/E de 20.", 6, 15, [
        ("multiple_choice", "Que signifie un P/E de 15 ?", ["Le titre a perdu 15%", "Vous payez 15 fois le bénéfice annuel", "Le dividende est de 15%", "Il y a 15 actionnaires"], "Vous payez 15 fois le bénéfice annuel", "C'est le multiple de valorisation."),
        ("true_false", "Un Yield de 15% est toujours signe de bonne santé ?", None, "false", "Faux, c'est souvent le signe que le marché anticipe une baisse du dividende."),
        ("multiple_choice", "Pourquoi les boîtes Tech ont souvent un P/E élevé ?", ["À cause de fautes de calcul", "Parce qu'on attend une forte croissance future", "Elles n'ont pas de concurrents", "Grâce aux robots"], "Parce qu'on attend une forte croissance future", "Le marché paie pour le futur."),
        ("true_false", "Le P/E moyen historique se situe souvent entre 15 et 20 ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m5.id, 3, "Dette et Cash-Flow", 
        "Les profits sont une opinion, le cash est une réalité. Le Free Cash Flow est l'argent qui reste vraiment dans les caisses après avoir payé les investissements. Une entreprise avec beaucoup de cash peut survivre aux crises et racheter ses concurrents.", 
        "Certaines entreprises font faillite alors qu'elles affichent des 'profits' comptables, faute de cash.", 5, 15, [
        ("multiple_choice", "Qu'est-ce qui mesure l'argent réel généré par l'activité ?", ["Chiffre d'Affaires", "Free Cash Flow (Flux de trésorerie)", "Nombre de clients", "Prix du logo"], "Free Cash Flow (Flux de trésorerie)", "C'est l'indicateur de survie ultime."),
        ("true_false", "On peut afficher des profits sans avoir de cash en caisse ?", None, "true", "Vrai, à cause des règles comptables."),
        ("multiple_choice", "Pourquoi surveiller la dette d'une entreprise ?", ["Pour éviter la faillite en cas de crise", "Pour devenir riche", "Pour faire plaisir aux banques", "C'est facultatif"], "Pour éviter la faillite en cas de crise", "La dette est un poids quand les taux montent."),
        ("true_false", "Brûler son cash indéfiniment mène à la faillite ?", None, "true", "Vrai, sauf nouvelle levée de fonds.")
    ])

    # --- MODULE 6: ECONOMIE (3 leçons) ---
    m6 = Module(title="Bourse et Économie", description="L'environnement macro", level="intermediate", order=6, icon="🌍")
    session.add(m6); session.flush()
    add_lesson(session, m6.id, 1, "Inflation et Bourse", 
        "L'inflation est la hausse généralisée des prix. Elle réduit votre pouvoir d'achat. Les entreprises de qualité peuvent souvent augmenter leurs prix (Pricing Power), ce qui protège vos investissements contre la dévaluation de la monnaie.", 
        "Si le pain monte de 10%, l'action qui possède les boulangeries doit aussi monter.", 5, 12, [
        ("multiple_choice", "L'inflation excessive est généralement :", ["Bonne pour les actions", "Mauvaise pour les obligations", "Neutre", "Supprime les bourses"], "Mauvaise pour les obligations", "Car leur rendement fixe perd de sa valeur."),
        ("true_false", "Les actions offrent une protection contre l'inflation ?", None, "true", "Vrai, car les entreprises montent leurs prix de vente."),
        ("multiple_choice", "Qu'est-ce que la stagflation ?", ["Inflation + Croissance", "Inflation + Stagnation économique", "Pas d'inflation", "Bourse qui monte"], "Inflation + Stagnation économique", "L'un des pires scénarios économiques."),
        ("true_false", "L'objectif d'inflation des banques centrales est souvent de 2% ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m6.id, 2, "Les Taux d'intérêt", 
        "C'est le 'prix de l'argent'. Quand la Banque Centrale (FED ou BCE) monte les taux, emprunter coûte plus cher. Cela ralentit l'économie et fait souvent baisser la bourse, car les investisseurs préfèrent alors les placements sans risque.", 
        "Quand les taux passent de 0% à 4%, les entreprises technologiques corrigent souvent.", 6, 12, [
        ("multiple_choice", "Généralement, une hausse brutale des taux fait :", ["Monter les actions", "Baisser les actions", "Fermer les banques", "Rien"], "Baisser les actions", "L'argent devient plus cher et rare."),
        ("true_false", "La FED est la banque centrale européenne ?", None, "false", "Faux, c'est la banque centrale américaine."),
        ("multiple_choice", "Des taux bas favorisent :", ["L'épargne sur livrets", "L'investissement et l'emprunt", "L'inflation nulle", "La vente de toutes les actions"], "L'investissement et l'emprunt", "Cela stimule l'économie."),
        ("true_false", "Les actions de croissance souffrent plus de la hausse des taux ?", None, "true", "Vrai, car le coût de leurs futurs profits augmente.")
    ])
    add_lesson(session, m6.id, 3, "Cycles Économiques", 
        "L'économie n'est pas une ligne droite, c'est un cycle de booms et de récessions. La bourse anticipe souvent ces cycles : elle chute avant la crise et remonte avant que l'économie ne se rétablisse. C'est le 'marché anticipateur'.", 
        "La bourse a commencé à remonter en 2009 alors que le chômage continuait de monter.", 5, 12, [
        ("multiple_choice", "Quelle est la définition technique d'une récession ?", ["Une baisse de la bourse", "2 trimestres consécutifs de baisse du PIB", "Départ d'un PDG", "Inflation nulle"], "2 trimestres consécutifs de baisse du PIB", "C'est le critère standard."),
        ("true_false", "La bourse remonte souvent AVANT la fin de la récession ?", None, "true", "Vrai, elle anticipe la reprise."),
        ("multiple_choice", "Quel secteur est considéré comme 'Défensif' ?", ["Le luxe", "La Santé et la Consommation de base", "La Technologie", "L'automobile"], "La Santé et la Consommation de base", "On a toujours besoin de se soigner et de manger."),
        ("true_false", "L'économie mondiale croît-elle sans jamais faire de pause ?", None, "false", "Faux, il y a des cycles de purges nécessaires.")
    ])

    # --- MODULE 7: PSYCHOLOGIE (2 leçons) ---
    m7 = Module(title="Psychologie de l'investisseur", description="Éviter les pièges", level="intermediate", order=7, icon="🧠")
    session.add(m7); session.flush()
    add_lesson(session, m7.id, 1, "Biais et Émotions", "Peur et Cupidité...", "Panique COVID", 7, 15, [
        ("multiple_choice", "Biais de confirmation ?", ["Vérifier sources", "Chercher infos qui vont dans notre sens", "Oublier infos", "Avoir raison"], "Chercher infos qui vont dans notre sens", "Piège dangereux."),
        ("true_false", "FOMO = Peur de rater une opportunité ?", None, "true", "Vrai."),
        ("multiple_choice", "Aversion à la perte ?", ["Aimer perdre", "Douleur perte > Joie gain", "Perdre peu", "Gagner beaucoup"], "Douleur perte > Joie gain", "Biais humain."),
        ("true_false", "Un bon investisseur est un robot sans émotions ?", None, "true", "Idéalement.")
    ])
    add_lesson(session, m7.id, 2, "Discipline : DCA", "Dollar Cost Averaging...", "Investir chaque mois", 6, 15, [
        ("multiple_choice", "DCA consiste à ?", ["Timer marché", "Investir fixe régulièrement", "Vendre tout", "Acheter au plus bas"], "Investir fixe régulièrement", "Lissage."),
        ("true_false", "Le DCA réduit le risque lié au mauvais timing ?", None, "true", "Vrai."),
        ("multiple_choice", "Meilleur moment investissement ?", ["Demain", "Aujourd'hui", "Hier", "Jamais"], "Aujourd'hui", "Time in the market."),
        ("true_false", "Le DCA garantit de ne JAMAIS perdre ?", None, "false", "Faux.")
    ])

    # --- MODULE 8: STRATEGIES (3 leçons) ---
    m8 = Module(title="Stratégies Actions", description="Value, Growth, Quality", level="intermediate", order=8, icon="🏹")
    session.add(m8); session.flush()
    add_lesson(session, m8.id, 1, "Value vs Growth", "Buffett vs Tesla...", "Cycles", 6, 12, [
        ("multiple_choice", "Value ?", ["Tendance", "Décote vs Valeur réelle", "Introduit hier", "Plus cher"], "Décote vs Valeur réelle", "Soldes."),
        ("true_false", "Buffett est Value ?", None, "true", "Vrai."),
        ("multiple_choice", "Secteur Growth ?", ["Pétrole", "Tech Logiciels", "Ciment", "Electricité"], "Tech Logiciels", "Scalable."),
        ("true_false", "Cycles s'alternent ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m8.id, 2, "Dividendes", "Rente boursière...", "Aristocrats", 6, 15, [
        ("multiple_choice", "Aristocrat ?", ["Roi", "+25 ans hausse dividende", "Banque suisse", "Pas impôts"], "+25 ans hausse dividende", "Titre."),
        ("true_false", "Dividende = part bénéfice ?", None, "true", "Vrai."),
        ("multiple_choice", "Danger Yield 12% ?", ["Trop argent", "Non maintenable/Coupure", "Confiscation", "Super affaire"], "Non maintenable/Coupure", "Yield Trap."),
        ("true_false", "Réinvestir accélère composés ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m8.id, 3, "Quality", "Moat et Pricing Power...", "LVMH, Apple", 5, 12, [
        ("multiple_choice", "Moat ?", ["Eau", "Avantages durables", "Dette", "Logo"], "Avantages durables", "Fossé."),
        ("true_false", "Luxe = Qualité ?", None, "true", "Vrai."),
        ("multiple_choice", "Ignorer inflation car ?", ["Paie pas", "Augmente prix sans perdre clients", "Gouvernement", "Pas argent"], "Augmente prix sans perdre clients", "Pricing Power."),
        ("true_false", "Actions cycliques = Qualité constante ?", None, "false", "Faux.")
    ])

    # --- MODULE 9: RISQUES (2 leçons) ---
    m9 = Module(title="Risques et Volatilité", description="Gérer les tempêtes", level="intermediate", order=9, icon="🌊")
    session.add(m9); session.flush()
    add_lesson(session, m9.id, 1, "Comprendre la Volatilité", "Prix qui bouge...", "Bourse vs Immo", 5, 10, [
        ("multiple_choice", "Volatilité élevée ?", ["Sûr", "Incertain/Bouge fort", "Ennuyeux", "Cher"], "Incertain/Bouge fort", "Mouvement."),
        ("true_false", "La volatilité est la même chose que la perte ?", None, "false", "Faux. C'est juste le mouvement."),
        ("multiple_choice", "Indice de la peur ?", ["VIX", "CAC", "S&P", "FBI"], "VIX", "Volatility Index."),
        ("true_false", "Un horizon long réduit l'impact de la volatilité ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m9.id, 2, "Drawdown et Récupération", "Chute et Remontée...", "Chute 50% = besoin +100%", 6, 10, [
        ("multiple_choice", "Chute 50%, hausse pour revenir ?", ["50%", "100%", "25%", "0%"], "100%", "Mathématiques pertes."),
        ("true_false", "Le 'Drawdown' est la chute depuis le plus haut ?", None, "true", "Vrai."),
        ("multiple_choice", "Limiter drawdown via ?", ["Tout vendre", "Diversification actifs", "Parier", "Attendre"], "Diversification actifs", "Coussin."),
        ("true_false", "La bourse finit toujours par remonter sur le très long terme ?", None, "true", "Historiquement vrai.")
    ])

    # --- MODULE 10: FISCALITE (2 leçons) ---
    m10 = Module(title="Fiscalité", description="Optimisez vos gains", level="intermediate", order=10, icon="🏛️")
    session.add(m10); session.flush()
    add_lesson(session, m10.id, 1, "Le PEA", "Paradis français...", "17.2% vs 30%", 6, 15, [
        ("multiple_choice", "Avantage après 5 ans ?", ["Nul", "17.2% au lieu de 30%", "100€ offerts", "Aucun"], "17.2% au lieu de 30%", "Economie."),
        ("true_false", "Retrait précoce = clôture ?", None, "true", "Vrai."),
        ("multiple_choice", "Google en direct ?", ["Oui", "Non (pas UE)", "Mardi", "Jeune"], "Non (pas UE)", "Limites."),
        ("true_false", "Ouvrir avec 10€ suffit ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m10.id, 2, "CTO et Flat Tax", "Liberté vs 30%...", "Actions US", 5, 12, [
        ("multiple_choice", "Surnom 30% ?", ["High", "Flat", "Small", "Eco"], "Flat", "Taux unique."),
        ("true_false", "Plafond CTO ?", None, "false", "Faux."),
        ("multiple_choice", "Décomposition Flat Tax ?", ["15+15", "12.8+17.2", "30 seul", "20+10"], "12.8+17.2", "Calcul."),
        ("true_false", "Option barème possible ?", None, "true", "Vrai.")
    ])

    # --- MODULE 11: CONSTRUCTION (2 leçons) ---
    m11 = Module(title="Construction Portefeuille", description="Core-Satellite", level="intermediate", order=11, icon="🎨")
    session.add(m11); session.flush()
    add_lesson(session, m11.id, 1, "Core-Satellite", "Sécurité + Passion...", "80/20", 7, 15, [
        ("multiple_choice", "Objectif Core ?", ["Risque max", "Socle solide", "Cryptos", "Rien"], "Socle solide", "Fondation."),
        ("true_false", "Majeur partie en Satellites ?", None, "false", "Faux."),
        ("multiple_choice", "MSCI World candidat ?", ["Satellite", "Core", "Erreur", "Pari"], "Core", "Global."),
        ("true_false", "Satisfaire convictions sans danger ?", None, "true", "Vrai.")
    ])
    add_lesson(session, m11.id, 2, "Rééquilibrage", "Gérer dérive poids...", "Vendre haut/Acheter bas", 6, 12, [
        ("multiple_choice", "Qu'est-ce ?", ["Supprimer", "Ajuster poids", "Baisser tarifs", "Changer courtier"], "Ajuster poids", "Discipline."),
        ("true_false", "Vendre ce qui a performé ?", None, "true", "Vrai."),
        ("multiple_choice", "Fréquence ?", ["Jours", "Heures", "1-2 fois/an", "Jamais"], "1-2 fois/an", "Efficacité."),
        ("true_false", "Garantit meilleur rendement annuel ?", None, "false", "Faux.")
    ])

    # --- MODULE 12: PASSAGE ACTION (2 leçons) ---
    m12 = Module(title="Passer à l'action", description="Étapes concrètes", level="beginner", order=12, icon="🚀")
    session.add(m12); session.flush()
    add_lesson(session, m12.id, 1, "Ouvrir son compte", "PEA, CTO, AV...", "Courtier", 6, 10, [
        ("multiple_choice", "Fiscalité douce après 8 ans ?", ["CTO", "PEA", "Assurance-Vie", "Livret"], "Assurance-Vie", "Spécificité."),
        ("true_false", "On peut cumuler PEA et CTO ?", None, "true", "Vrai."),
        ("multiple_choice", "Frais de courtage ?", ["Frais de garde", "Coût par ordre", "Impôts", "Assurance"], "Coût par ordre", "Transaction."),
        ("true_false", "Choisir un courtier agréé AMF ?", None, "true", "Essentiel.")
    ])
    add_lesson(session, m12.id, 2, "Premier investissement", "Le premier pas...", "ETF World", 7, 15, [
        ("multiple_choice", "Priorité début ?", ["Timer", "World et Tenir", "100 actions", "Influenceurs"], "World et Tenir", "Succès."),
        ("true_false", "Commencer avec 50€ est utile ?", None, "true", "Vrai."),
        ("multiple_choice", "S'informer ?", ["Journal télé", "Rapports annuels/Academy", "Rumeurs", "Rien"], "Rapports annuels/Academy", "Sérieux."),
        ("true_false", "Le meilleur moment était hier ?", None, "true", "Vrai.")
    ])

    session.commit()
    print(f"🚀 MISSION ACCOMPLIE !\n✅ Modules : {session.query(Module).count()}\n✅ Leçons  : {session.query(Lesson).count()}\n✅ Questions: {session.query(Question).count()}")

def add_lesson(session, module_id, order, title, content, example, minutes, xp, questions):
    lesson = Lesson(module_id=module_id, order=order, title=title, content=content, example=example, estimated_minutes=minutes, xp_reward=xp)
    session.add(lesson); session.flush()
    for idx, q in enumerate(questions, 1):
        q_type, prompt, choices, answer, explanation = q
        session.add(Question(lesson_id=lesson.id, order=idx, type=q_type, prompt=prompt, choices=choices, correct_answer=answer, explanation=explanation))

if __name__ == "__main__":
    seed_complete_curriculum()
