"""
Refined Curriculum Part 2 (Modules 7-12).
Ensures all quiz answers are explicitly covered in the lesson text.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed_refined_p2():
    session = Session()
    
    # --- MODULE 7: PSYCHOLOGIE ---
    m7 = Module(title="Psychologie de l'investisseur", description="Éviter les pièges", level="intermediate", order=7, icon="🧠")
    session.add(m7); session.flush()
    
    add_lesson(session, m7.id, 1, "Biais et Émotions", 
        "L'investisseur est souvent son propre obstacle. La peur et la cupidité dictent trop souvent nos choix. Le FOMO (Fear Of Missing Out) est la peur irrationnelle de rater une opportunité que tout le monde semble saisir. À l'opposé, l'aversion à la perte est un biais humain où la douleur d'une perte de 100€ est psychologiquement bien plus forte que la joie d'un gain de 100€. Enfin, le biais de confirmation nous pousse à chercher uniquement des informations qui vont dans notre sens, ignorant les signaux d'alerte. Un bon investisseur doit apprendre à rester aussi discipliné qu'un robot malgré ses émotions.", 
        "Vendre ses actions en panique lors d'un krach, pour les voir remonter dès le lendemain.", 7, 15, [
        ("multiple_choice", "Qu'est-ce que le FOMO ?", ["Une nouvelle monnaie", "La peur de rater une opportunité", "Un type d'assurance", "Un indice boursier"], "La peur de rater une opportunité", "Fear Of Missing Out."),
        ("true_false", "La douleur d'une perte est plus forte que la joie d'un gain ?", None, "true", "Vrai, c'est l'aversion à la perte."),
        ("multiple_choice", "Le biais de confirmation consiste à :", ["Vérifier ses comptes", "Chercher uniquement des infos confortant notre avis", "Oublier de vendre", "Acheter au pif"], "Chercher uniquement des infos confortant notre avis", "On s'interdit de voir la réalité si elle nous déplaît."),
        ("true_false", "La discipline est plus importante que l'instinct en bourse ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m7.id, 2, "Discipline : DCA", 
        "Le DCA (Dollar Cost Averaging) est une stratégie consistant à investir une somme fixe à intervalles réguliers (ex: 200€ tous les mois), peu importe le prix de l'actif. Cela permet de moyenner (lisser) son prix d'achat dans le temps : on achète plus de titres quand c'est bas et moins quand c'est haut. Cette méthode élimine le stress de timer le marché (chercher le 'bon moment'). Si la bourse chute de 10% en plein DCA, c'est une opportunité car votre virement mensuel achètera plus de titres à prix cassé. Sachez que commencer avec seulement 50€ par mois est déjà très efficace grâce à la régularité.", 
        "Investir 100€ chaque 1er du mois pendant 10 ans.", 6, 15, [
        ("multiple_choice", "Quel est l'avantage clé du DCA ?", ["Gagner 50% par an", "Lisser son prix de revient et supprimer le stress", "Ne pas payer d'impôts", "Devenir célèbre"], "Lisser son prix de revient et supprimer le stress", "Le timing n'est plus un sujet de panique."),
        ("true_false", "Le DCA permet d'acheter au 'pire' moment ?", None, "false", "Faux, il permet justement d'éviter de mettre tout son capital au plus haut."),
        ("multiple_choice", "Que faire si la bourse baisse de 10% quand on fait du DCA ?", ["Tout vendre par peur", "Continuer son investissement régulier", "Attendre 3 ans", "Changer de banque"], "Continuer son investissement régulier", "C'est dans ces phases qu'on accumule le plus de titres."),
        ("true_false", "Même 50€ par mois sont utiles en investissement régulier ?", None, "true", "Vrai, la régularité est reine.")
    ])

    # --- MODULE 8: STRATEGIES ---
    m8 = Module(title="Stratégies Actions", description="Value, Growth, Quality", level="intermediate", order=8, icon="🏹")
    session.add(m8); session.flush()
    
    add_lesson(session, m8.id, 1, "Value vs Growth", 
        "L'investisseur Value cherche des 'soldes' : des entreprises solides dont le prix actuel en bourse est inférieur à leur valeur réelle intrinsèque. C'est l'école de Warren Buffett. L'investisseur Growth (Croissance), lui, mise sur les secteurs d'avenir (typiquement la Tech et les logiciels) et accepte de payer un prix élevé aujourd'hui car il attend une explosion des bénéfices futurs. Ces deux styles s'alternent souvent en tête des meilleures performances selon les cycles économiques. La stratégie Value performe souvent mieux en période d'inflation et de taux élevés.", 
        "Acheter une banque (Value) délaissée vs acheter du Cloud / IA (Growth).", 6, 12, [
        ("multiple_choice", "Que recherche l'investisseur Value ?", ["La boîte la plus à la mode", "Une action décotée par rapport à sa valeur réelle", "Une action très chère", "Des cryptos anonymes"], "Une action décotée par rapport à sa valeur réelle", "Il cherche des entreprises 'en soldes'."),
        ("true_false", "La Tech (logiciels, IA) est typiquement du 'Growth' ?", None, "true", "Vrai, on mise sur la croissance exponentielle."),
        ("multiple_choice", "En période d'inflation et de taux hauts, quel style résiste mieux ?", ["Growth", "Value", "Startup", "Spéculation"], "Value", "Les investisseurs reviennent vers les profits concrets et immédiats."),
        ("true_false", "Value et Growth sont deux styles qui se complètent ?", None, "true", "Vrai, il est utile d'avoir les deux.")
    ])
    
    add_lesson(session, m8.id, 2, "Dividendes", 
        "Certains investisseurs se créent une rente boursière via les dividendes. On appelle 'Dividend Aristocrat' une entreprise qui augmente son dividende chaque année depuis plus de 25 ans consécutifs. C'est un gage de solidité. On surveille le 'Payout Ratio' : c'est la part du bénéfice net reversée en dividende. S'il dépasse 100%, l'entreprise paie plus qu'elle ne gagne, ce qui est risqué. Attention au Yield Trap (piège au rendement) : un rendement de 10 ou 12% cache souvent une action qui s'effondre. Réinvestir ses dividendes est la clé pour accélérer drastiquement les intérêts composés.", 
        "L'Oréal ou Sanofi sont des payeurs de dividendes réguliers en France.", 6, 15, [
        ("multiple_choice", "Qu'est-ce qu'un Dividend Aristocrat ?", ["Une banque suisse", "Une société augmentant son dividende depuis 25+ ans", "Une boîte appartenant à l'État", "Une société agricole"], "Une société augmentant son dividende depuis 25+ ans", "Preuve de santé long-terme."),
        ("true_false", "Le Payout Ratio de 150% est un bon signe ?", None, "false", "Faux, l'entreprise s'endette pour payer ses actionnaires."),
        ("multiple_choice", "Un rendement (Yield) anormalement élevé (ex 12%) est souvent :", ["Une chance inouïe", "Un danger de coupure (Yield Trap)", "Regulé par l'État", "Le signe d'un don"], "Un danger de coupure (Yield Trap)", "Le prix de l'action baisse car le marché a peur."),
        ("true_false", "Réinvestir les dividendes booste la performance ?", None, "true", "Vrai, c'est l'accélérateur ultime.")
    ])
    
    add_lesson(session, m8.id, 3, "Quality", 
        "L'investissement 'Qualité' se focalise sur l'excellence opérationnelle. On cherche des entreprises avec un 'Moat' (un fossé, ou rempart concurrentiel) : une marque forte, des brevets ou une position dominante. Ces entreprises possèdent un 'Pricing Power' : elles peuvent monter leurs prix pour combattre l'inflation sans perdre leurs clients. Les critères financiers sont des marges bénéficiaires élevées et très peu de dettes. LVMH (Luxe) ou Apple sont des exemples de Qualité. Notez qu'une entreprise de qualité n'est pas forcément une affaire si vous la payez un prix délirant.", 
        "Moat d'Apple : Son écosystème fermé. Moat de Coca-Cola : Sa marque mondiale.", 5, 12, [
        ("multiple_choice", "Qu'est-ce qu'un 'Moat' ?", ["Un château fort", "Un avantage concurrentiel durable", "Une dette de banque", "Un type d'action"], "Un avantage concurrentiel durable", "Le rempart qui protège les profits."),
        ("true_false", "LVMH (Luxe) possède un fort Pricing Power ?", None, "true", "Vrai, ils montent leurs prix chaque année et vendent toujours plus."),
        ("multiple_choice", "Un critère financier de 'Qualité' est :", ["Dette élevée", "Marges bénéficiaires fortes", "Plus de 1000 bureaux", "Ancienneté du PDG"], "Marges bénéficiaires fortes", "Preuve que le produit a une grande valeur ajoutée."),
        ("true_false", "Investir en 'Qualité' signifie ignorer totalement le prix d'achat ?", None, "false", "Faux, même pour la qualité, le prix reste un sujet.")
    ])

    # --- MODULE 9: RISQUES ---
    m9 = Module(title="Risques et Volatilité", description="Gérer les tempêtes", level="intermediate", order=9, icon="🌊")
    session.add(m9); session.flush()
    
    add_lesson(session, m9.id, 1, "Comprendre la Volatilité", 
        "La volatilité mesure l'ampleur des variations rapides du prix. En bourse, elle est inévitable et n'est pas synonyme de perte tant qu'on ne vend pas. L'indice VIX (surnommé l'indice de la peur) mesure la volatilité attendue sur le marché américain. Plus votre horizon de placement est long, moins cette volatilité quotidienne a d'impact sur votre objectif final. C'est le prix à payer pour des rendements supérieurs au Livret A.", 
        "Une action qui fait +2% puis -3% en 2 jours est volatile.", 5, 10, [
        ("multiple_choice", "Que mesure la volatilité ?", ["Le profit net", "L'ampleur des variations de prix", "La taxe d'achat", "L'âge du courtier"], "L'ampleur des variations de prix", "Indique si l'actif est 'nerveux'."),
        ("true_false", "La volatilité est synonyme de perte d'argent ?", None, "false", "Faux, c'est juste un mouvement de prix tant qu'on n'a pas vendu."),
        ("multiple_choice", "Comment s'appelle l'indice mesurant la peur/volatilité ?", ["NASDAQ", "VIX", "S&P", "EURO"], "VIX", "Volatility Index."),
        ("true_false", "Le temps réduit l'impact psychologique de la volatilité ?", None, "true", "Vrai, on regarde moins les cours.")
    ])
    
    add_lesson(session, m9.id, 2, "Drawdown et Récupération", 
        "Le 'Drawdown' est la chute maximale d'un actif depuis son point le plus haut. Attention aux mathématiques : si vous subissez une perte de 20%, il vous faut une hausse de 25% pour revenir à zéro. Si vous perdez 50%, il faut faire +100% (doubler votre capital) juste pour récupérer votre mise. C'est pour cela qu'il faut limiter les chutes via la diversification d'actifs (obligations, or, etc.). Un drawdown de -10% arrive presque chaque année en bourse.", 
        "Chute de 50€ à 25€ (-50%). Pour remonter à 50€, il faut faire +100%.", 6, 10, [
        ("multiple_choice", "Pour compenser une perte de 50%, il faut gagner :", ["50%", "100%", "25%", "10%"], "100%", "Les mathématiques des pertes sont asymétriques."),
        ("true_false", "Un drawdown est la chute depuis le plus haut ?", None, "true", "Vrai, c'est la baisse du sommet au creux."),
        ("multiple_choice", "Comment limiter son drawdown maximal ?", ["Parier sur 1 seule action", "Diversifier ses actifs", "Vendre dès que ça perd 1%", "Prier"], "Diversifier ses actifs", "En mélangeant des actifs qui ne baissent pas en même temps."),
        ("true_false", "La Bourse a historiquement toujours récupéré ses drawdowns sur 15-20 ans ?", None, "true", "Vrai, sur les indices majeurs diversifiés.")
    ])

    # --- MODULE 10: FISCALITE ---
    m10 = Module(title="Fiscalité", description="Optimisez vos gains", level="intermediate", order=10, icon="🏛️")
    session.add(m10); session.flush()
    
    add_lesson(session, m10.id, 1, "Le PEA", 
        "Le Plan d'Épargne en Actions (PEA) est une enveloppe fiscale majeure en France. L'avantage fiscal se déclenche après 5 ans : vos gains sont exonérés d'impôt sur le revenu (vous ne payez que les 17,2% de prélèvements sociaux au lieu des 30% habituels). Le retrait avant 5 ans entraîne normalement la clôture du plan. Le PEA est limité aux actions européennes (sauf ETF synthétiques) et possède un plafond de versement de 150 000€. Pour ouvrir un PEA, un simple versement de 10€ suffit pour lancer le 'compteur' des 5 ans.", 
        "Gains de 1000€ -> Dans PEA (5 ans) vous gardez 828€. Dans un CTO environ 700€.", 6, 15, [
        ("multiple_choice", "Quel est l'avantage du PEA après 5 ans ?", ["Gratuité totale", "Pas d'impôt sur le revenu (17,2% PS seuls)", "Bonus fixe", "Aucun"], "Pas d'impôt sur le revenu (17,2% PS seuls)", "Économie de 12,8%."),
        ("true_false", "On peut avoir 3 PEA ?", None, "false", "Faux, 1 seul par personne physique."),
        ("multiple_choice", "Quelle est la limite (plafond) de versements sur un PEA ?", ["10 000€", "150 000€", "500 000€", "Aucune"], "150 000€", "On peut verser 150k€ maximum."),
        ("true_false", "Peut-on mettre des actions Google (USA) en direct dans le PEA ?", None, "false", "Faux, le PEA est réservé aux titres européens (en direct).")
    ])
    
    add_lesson(session, m10.id, 2, "CTO et Flat Tax", 
        "Le Compte Titres Ordinaire (CTO) offre une liberté totale (actions du monde entier, USA, Asie) mais sans avantage fiscal. La règle par défaut est la Flat Tax (ou PFU) de 30% sur chaque gain. Ces 30% se décomposent en 12,8% d'impôt sur le revenu et 17,2% de prélèvements sociaux. Contrairement au PEA, il n'y a aucun plafond de versement sur le CTO. Il est toutefois possible d'opter pour le barème progressif de l'impôt sur le revenu si cela est plus avantageux pour votre foyer (bas revenus).", 
        "Vendre Nvidia avec 1000€ de gain -> 300€ d'impôt (Flat Tax).", 5, 12, [
        ("multiple_choice", "Quel est le montant de la Flat Tax (PFU) en France ?", ["20%", "30%", "40%", "15%"], "30%", "Prélèvement forfaitaire unique."),
        ("true_false", "Le CTO permet d'acheter des actions sans aucune limite géographique ?", None, "true", "Vrai, c'est son grand point fort."),
        ("multiple_choice", "Dans les 30%, quelle part revient aux prélèvements sociaux ?", ["10%", "17,2%", "12,8%", "5%"], "17,2%", "C'est la base sociale incompressible."),
        ("true_false", "On peut choisir autre chose que les 30% si on gagne peu ?", None, "true", "Vrai, on peut demander l'application du barème classique de l'impôt.")
    ])

    # --- MODULE 11: CONSTRUCTION ---
    m11 = Module(title="Construction Portefeuille", description="Core-Satellite", level="intermediate", order=11, icon="🎨")
    session.add(m11); session.flush()
    
    add_lesson(session, m11.id, 1, "Core-Satellite", 
        "La méthode Core-Satellite consiste à construire un socle solide et régulier (le Core) représentant environ 80% du portefeuille, généralement composé d'un ETF diversifié mondial (MSCI World). Les 20% restants sont les 'Satellites' : des paris thématiques (IA, Santé) ou des actions individuelles par conviction. Le but est de satisfaire vos envies tout en protégeant l'essentiel de votre capital via le Core. Cette méthode permet de limiter le risque total tout en gardant une touche de passion.", 
        "Core (ETF World) + Satellites (LVMH + Tesla + ETF Eau).", 7, 15, [
        ("multiple_choice", "Quel est le rôle du 'Core' ?", ["La spéculation pure", "Le socle solide et diversifié", "Parier sur l'or", "Ne servir à rien"], "Le socle solide et diversifié", "C'est l'ancre du navire."),
        ("true_false", "La majorité du portefeuille devrait être dans les Satellites ?", None, "false", "Faux, ils sont trop risqués pour être dominants."),
        ("multiple_choice", "Lequel est un candidat idéal pour le 'Core' ?", ["Une crypto montante", "Un ETF MSCI World", "Une action de start-up", "Une option"], "Un ETF MSCI World", "Car il couvre des pays et secteurs variés."),
        ("true_false", "Cette méthode mélange sécurité et convictions personnelles ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m11.id, 2, "Rééquilibrage", 
        "Avec le temps, vos actifs montent à des vitesses différentes. Si vous aviez 50% actions et 50% obligations, vous risquez de vous retrouver avec 70% d'actions car elles ont explosé. Rééquilibrer consiste à ajuster les poids pour revenir à votre allocation cible. Cela force à une discipline saine : on vend un peu de ce qui a beaucoup monté (vendre haut) pour racheter ce qui est en retard (acheter bas). On conseille de le faire 1 à 2 fois par an pour maintenir son profil de risque d'origine.", 
        "Vendre 5% d'actions US pour racheter 5% d'obligations et revenir à 50/50.", 6, 12, [
        ("multiple_choice", "Pourquoi rééquilibrer un portefeuille ?", ["Pour payer plus de frais", "Pour maintenir son profil de risque cible", "Pour tout recommencer", "Parce que c'est la loi"], "Pour maintenir son profil de risque cible", "Sinon le portefeuille devient trop risqué avec le temps."),
        ("true_false", "Rééquilibrer force souvent à vendre ses 'gagnants' ?", None, "true", "Vrai, pour sécuriser une partie des bénéfices."),
        ("multiple_choice", "Fréquence recommandée pour le rééquilibrage ?", ["Tous les jours", "1 à 2 fois par an", "Tous les 10 ans", "Jamais"], "1 à 2 fois par an", "Cela suffit amplement."),
        ("true_false", "Le rééquilibrage est une méthode de discipline automatique ?", None, "true", "Vrai.")
    ])

    # --- MODULE 12: PASSAGE ACTION ---
    m12 = Module(title="Passer à l'action", description="Étapes concrètes", level="beginner", order=12, icon="🚀")
    session.add(m12); session.flush()
    
    add_lesson(session, m12.id, 1, "Ouvrir son compte", 
        "L'enveloppe fiscale est le cadre (PEA, CTO, Assurance-Vie). L'Assurance-Vie offre une fiscalité douce après 8 ans. Pour choisir un courtier, regardez les frais de courtage (coût par ordre), les frais de garde (qui devraient être nuls chez les bons acteurs) et vérifiez toujours l'agrément par l'Autorité des Marchés Financiers (AMF). L'investissement est un marathon : on peut et on doit commencer tôt, même avec seulement 50€ par mois via des versements programmés.", 
        "Choisir un courtier en ligne plutôt qu'une banque de réseau chargée de frais.", 6, 10, [
        ("multiple_choice", "Quelle enveloppe offre des avantages après 8 ans ?", ["Livret A", "Assurance-Vie", "Compte Courant", "Carton"], "Assurance-Vie", "Spécificité française."),
        ("true_false", "On peut investir en bourse avec 50€ par mois ?", None, "true", "Vrai, via les parts fractionnées ou les petits ordres."),
        ("multiple_choice", "Que faut-il vérifier en priorité chez un courtier ?", ["La publicité", "Les frais et l'agrément AMF", "Le nom", "La météo"], "Les frais et l'agrément AMF", "Sécurité et rendement."),
        ("true_false", "On peut posséder à la fois un PEA et un CTO ?", None, "true", "Vrai, c'est même conseillé.")
    ])
    
    add_lesson(session, m12.id, 2, "Premier investissement", 
        "Pour un débutant, la meilleure action est souvent d'acheter un ETF diversifié mondial et de tenir sur le long terme. Le plus dur est de faire le premier pas. Informez-vous via des sources sérieuses comme cette Academy ou des rapports annuels plutôt que sur les réseaux sociaux. Rappelez-vous : le meilleur moment pour investir était hier, le deuxième meilleur moment est aujourd'hui. L'important est la rigueur et le temps passé sur le marché (Time in the market).", 
        "Acheter sa première part d'ETF World.", 7, 15, [
        ("multiple_choice", "Meilleure action pour débuter ?", ["Parier sur 1 startup", "Acheter un ETF diversifié et tenir", "Vendre tout", "Acheter au pif"], "Acheter un ETF diversifié et tenir", "Simplicité et efficacité prouvée."),
        ("true_false", "L'investissement est un sprint ?", None, "false", "Faux, c'est un marathon de long terme."),
        ("multiple_choice", "Source d'information recommandée ?", ["Rumeurs de café", "Academy et sites officiels", "Influenceurs sans preuve", "Rien"], "Academy et sites officiels", "S'appuyer sur du factuel."),
        ("true_false", "Commencer aujourd'hui est mieux que d'attendre demain ?", None, "true", "Vrai, chaque jour compte pour les intérêts composés.")
    ])

    session.commit()
    print(f"✅ Refined Part 2 Completed.")

def add_lesson(session, module_id, order, title, content, example, minutes, xp, questions):
    lesson = Lesson(module_id=module_id, order=order, title=title, content=content, example=example, estimated_minutes=minutes, xp_reward=xp)
    session.add(lesson); session.flush()
    for idx, q in enumerate(questions, 1):
        q_type, prompt, choices, answer, explanation = q
        session.add(Question(lesson_id=lesson.id, order=idx, type=q_type, prompt=prompt, choices=choices, correct_answer=answer, explanation=explanation))

if __name__ == "__main__":
    seed_refined_p2()
