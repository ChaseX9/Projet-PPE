"""
Part 2 of the Final Professional Curriculum for CapInvest Academy.
Modules 7 to 12 (Full Content).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed_curriculum_p2():
    session = Session()
    
    # --- MODULE 7: PSYCHOLOGIE (2 leçons) ---
    m7 = Module(title="Psychologie de l'investisseur", description="Éviter les pièges", level="intermediate", order=7, icon="🧠")
    session.add(m7); session.flush()
    
    add_lesson(session, m7.id, 1, "Biais et Émotions", 
        "L'investisseur est son propre pire ennemi. La peur de perdre et l'appétit pour le gain rapide (cupidité) nous poussent à faire des erreurs irrationnelles. Apprendre à identifier ces émotions est la première étape pour gagner.", 
        "Pendant le COVID, beaucoup ont vendu au plus bas par peur, ratant la remontée fulgurante qui a suivi.", 7, 15, [
        ("multiple_choice", "Qu'est-ce que le FOMO ?", ["Une assurance", "La peur de rater une opportunité", "Un type de compte", "Un indice"], "La peur de rater une opportunité", "Fear Of Missing Out."),
        ("true_false", "La douleur d'une perte est plus forte que la joie d'un gain ?", None, "true", "Vrai, c'est l'aversion à la perte."),
        ("multiple_choice", "Le biais de confirmation consiste à :", ["Vérifier ses calculs", "Chercher uniquement des infos confortant notre avis", "Oublier son mot de passe", "Vendre"], "Chercher uniquement des infos confortant notre avis", "On ignore les signaux d'alerte."),
        ("true_false", "Un bon investisseur doit rester discipliné malgré ses émotions ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m7.id, 2, "Discipline : DCA", 
        "Le Dollar Cost Averaging consiste à investir la même somme chaque mois, peu importe le prix. Cela permet de moyenner votre prix d'achat et d'éliminer le stress du 'bon moment'. Le temps passé sur le marché bat le timing du marché.", 
        "Investir 200€ tous les 5 du mois, que la bourse soit en haut ou en bas.", 6, 15, [
        ("multiple_choice", "Avantage clé du DCA ?", ["Gagner 20% par mois", "Lisser son prix de revient", "Ne jamais payer d'impôts", "Avoir raison"], "Lisser son prix de revient", "On achète plus quand c'est bas et moins quand c'est haut."),
        ("true_false", "Le DCA évite de timer le marché ?", None, "true", "Vrai, on ne se pose plus de questions."),
        ("multiple_choice", "Que faire si la bourse chute de 10% en DCA ?", ["Tout vendre", "Continuer son virement mensuel", "Attendre 1 an", "Gémir"], "Continuer son virement mensuel", "C'est là qu'on achète des titres à prix cassé."),
        ("true_false", "Commencer avec 50€/mois est déjà très efficace ?", None, "true", "Vrai.")
    ])

    # --- MODULE 8: STRATEGIES (3 leçons) ---
    m8 = Module(title="Stratégies Actions", description="Value, Growth, Quality", level="intermediate", order=8, icon="🏹")
    session.add(m8); session.flush()
    
    add_lesson(session, m8.id, 1, "Value vs Growth", 
        "L'investisseur Value cherche des 'soldes' : des actions solides délaissées par le marché. L'investisseur Growth cherche les futurs géants de demain, acceptant de les payer cher aujourd'hui pour leur potentiel futur.", 
        "Warren Buffett (Value) vs ARK Invest (Growth).", 6, 12, [
        ("multiple_choice", "Que cherche un investisseur Value ?", ["La boîte la plus célèbre", "Une action décotée", "Une action très chère", "Des cryptos"], "Une action décotée", "Il veut un prix inférieur à la valeur réelle."),
        ("true_false", "Le secteur de la Tech est typiquement du Growth ?", None, "true", "Vrai, car on mise sur l'explosion des usages futurs."),
        ("multiple_choice", "La stratégie Value performe souvent en période de :", ["Argent gratuit/taux bas", "Inflation et taux hauts", "Crise totale", "Vacances"], "Inflation et taux hauts", "Les investisseurs reviennent vers les entreprises rentables."),
        ("true_false", "Alterner entre Value et Growth est impossible ?", None, "false", "Non, c'est même conseillé pour diversifier.")
    ])
    
    add_lesson(session, m8.id, 2, "Dividendes", 
        "Vivre de sa rente boursière est le rêve de beaucoup. Les entreprises matures qui versent des dividendes croissants (Aristocrates) offrent une stabilité psychologique et financière précieuse, surtout en période troublée.", 
        "Procter & Gamble augmente son dividende chaque année depuis plus de 60 ans.", 6, 15, [
        ("multiple_choice", "Un Dividend Aristocrat est une entreprise qui :", ["Appartient à la noblesse", "Augmente son dividende depuis 25+ ans", "Ne paie pas d'impôts", "Est en faillite"], "Augmente son dividende depuis 25+ ans", "Preuve de solidité exceptionnelle."),
        ("true_false", "Le rendement (Yield) est le seul indicateur à regarder ?", None, "false", "Faux, la pérennité du bénéfice est plus importante."),
        ("multiple_choice", "Le 'Payout Ratio' mesure :", ["Le prix de l'action", "La part des profits versée en dividende", "La dette", "Le CA"], "La part des profits versée en dividende", "S'il dépasse 100%, le dividende est en danger."),
        ("true_false", "Réinvestir ses dividendes booste la performance ?", None, "true", "Vrai, via les intérêts composés.")
    ])
    
    add_lesson(session, m8.id, 3, "Quality", 
        "L'investissement Qualité se base sur des entreprises avec un 'Moat' (un fossé concurrentiel). Ce sont des boîtes avec des marques fortes, peu de dettes et un pouvoir de fixation des prix (Pricing Power) qui les rend invincibles.", 
        "LVMH (Luxe) ou Microsoft (Logiciels) ont des marges que la concurrence ne peut pas attaquer.", 5, 12, [
        ("multiple_choice", "Qu'est-ce qu'un 'Moat' ?", ["Un château", "Un avantage concurrentiel durable", "Une dette", "Un type d'action"], "Un avantage concurrentiel durable", "Ce qui protège l'entreprise."),
        ("true_false", "Le 'Pricing Power' permet de monter les prix sans perdre de clients ?", None, "true", "Vrai, signe de force ultime."),
        ("multiple_choice", "Un critère de qualité financière est :", ["Grosse dette", "Fortes marges bénéficiaires", "Petit bureau", "Ancienneté du PDG"], "Fortes marges bénéficiaires", "Preuve que le produit est désiré et efficace."),
        ("true_false", "Une entreprise de qualité est toujours une affaire à n'importe quel prix ?", None, "false", "Faux, le prix d'achat reste important.")
    ])

    # --- MODULE 9: RISQUES (2 leçons) ---
    m9 = Module(title="Risques et Volatilité", description="Gérer les tempêtes", level="intermediate", order=9, icon="🌊")
    session.add(m9); session.flush()
    
    add_lesson(session, m9.id, 1, "Comprendre la Volatilité", 
        "La volatilité n'est pas votre ennemie, c'est le prix à payer pour des rendements élevés. Elle mesure simplement la vitesse et l'ampleur des variations de prix. Plus l'horizon est long, moins la volatilité quotidienne compte.", 
        "Une action qui bouge de 3% par jour est plus volatile qu'un livret fixe.", 5, 10, [
        ("multiple_choice", "La volatilité élevée signifie :", ["Sécurité", "Risque de fortes variations", "Profit garanti", "Ennui"], "Risque de fortes variations", "Ça bouge beaucoup."),
        ("true_false", "La volatilité est synonyme de perte ?", None, "false", "Faux, ce n'est qu'un mouvement temporaire."),
        ("multiple_choice", "L'indice VIX mesure :", ["La température", "La volatilité attendue (la peur)", "Le prix du pétrole", "La météo"], "La volatilité attendue (la peur)", "Surnommé l'indice de la peur."),
        ("true_false", "Le temps réduit l'impact de la volatilité ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m9.id, 2, "Drawdown et Récupération", 
        "Le drawdown est la perte maximale subie depuis un sommet. Attention à la psychologie des chiffres : si vous perdez 50%, vous devez faire +100% pour revenir au point de départ. La diversification limite ces chutes.", 
        "Pendant le Krach de 2000, le NASDAQ a perdu 80%. Il a fallu 15 ans pour s'en remettre.", 6, 10, [
        ("multiple_choice", "Besoin de hausse après une perte de 20% ?", ["20%", "25%", "50%", "100%"], "25%", "Les mathématiques des pertes sont cruelles."),
        ("true_false", "Un drawdown de -10% est courant en bourse ?", None, "true", "Vrai, cela arrive presque chaque année."),
        ("multiple_choice", "Comment réduire son drawdown ?", ["Parier gros", "Diversifier ses actifs", "Vendre dès que ça baisse", "Prier"], "Diversifier ses actifs", "Les obligations et l'or servent souvent d'amortisseurs."),
        ("true_false", "Attendre est souvent la meilleure stratégie en cas de baisse ?", None, "true", "Vrai, si les fondamentaux sont là.")
    ])

    # --- MODULE 10: FISCALITE (2 leçons) ---
    m10 = Module(title="Fiscalité", description="Optimisez vos gains", level="intermediate", order=10, icon="🏛️")
    session.add(m10); session.flush()
    
    add_lesson(session, m10.id, 1, "Le PEA", 
        "Le Plan d'Épargne en Actions est une enveloppe fiscale spécifique à la France. Après 5 ans, vos gains sont exonérés d'impôt sur le revenu (vous ne payez que les 17,2% de prélèvements sociaux). C'est le compte à ouvrir en priorité.", 
        "Idéal pour loger des ETF Monde ou des actions européennes.", 6, 15, [
        ("multiple_choice", "Avantage fiscal du PEA après 5 ans ?", ["Gratuité totale", "Pas d'impôt sur le revenu (17,2% PS seuls)", "Bonus de 500€", "Aucun"], "Pas d'impôt sur le revenu (17,2% PS seuls)", "Économie de 12,8% par rapport au CTO."),
        ("true_false", "Un retrait avant 5 ans peut entraîner la clôture ?", None, "true", "Vrai, soyez vigilant sur votre horizon."),
        ("multiple_choice", "Plafond du PEA ?", ["10 000€", "150 000€", "No limit", "50 000€"], "150 000€", "Versements au maximum."),
        ("true_false", "On peut avoir plusieurs PEA ?", None, "false", "Faux, 1 seul par adulte.")
    ])
    
    add_lesson(session, m10.id, 2, "CTO et Flat Tax", 
        "Le Compte Titres Ordinaire offre une liberté totale sur les actions mondiales (USA, Asie) mais est soumis à la Flat Tax de 30% (PFU). C'est le complément idéal du PEA pour investir sur Google, Tesla ou Nvidia.", 
        "Si vous gagnez 100€, vous en rendez 30 à l'État.", 5, 12, [
        ("multiple_choice", "Montant de la Flat Tax (PFU) ?", ["10%", "20%", "30%", "50%"], "30%", "Impôt unique forfaitaire."),
        ("true_false", "Le CTO permet d'acheter des actions US ?", None, "true", "Vrai, sans restrictions géographiques."),
        ("multiple_choice", "Composition des 30% ?", ["15+15", "12,8% IR + 17,2% PS", "30% social", "20+10"], "12,8% IR + 17,2% PS", "Structure du PFU."),
        ("true_false", "On peut opter pour le barème de l'IR ?", None, "true", "Vrai, si cela est plus avantageux pour vous.")
    ])

    # --- MODULE 11: CONSTRUCTION (2 leçons) ---
    m11 = Module(title="Construction Portefeuille", description="Core-Satellite", level="intermediate", order=11, icon="🎨")
    session.add(m11); session.flush()
    
    add_lesson(session, m11.id, 1, "Core-Satellite", 
        "Construisez un socle solide (Core) avec 80% d'ETF diversifiés (Monde, USA). Ajoutez 20% de paris thématiques ou individuels (Satellite) pour booster la performance ou suivre vos convictions (IA, Vert, etc).", 
        "80% MSCI World + 10% Semi-conducteurs + 10% Inde.", 7, 15, [
        ("multiple_choice", "Rôle du Core ?", ["Spéculation", "Socle solide et régulier", "Parier sur l'or", "Rien"], "Socle solide et régulier", "C'est la base de votre stratégie."),
        ("true_false", "Le satellite doit être minoritaire ?", None, "true", "Vrai, car plus volatil et risqué."),
        ("multiple_choice", "Un bon choix Core ?", ["Action d'une start-up", "ETF MSCI World", "Le bitcoin", "Une option"], "ETF MSCI World", "Diversification maximale."),
        ("true_false", "Cette méthode limite le risque total ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m11.id, 2, "Rééquilibrage", 
        "Si vos actions US ont trop monté, elles pèsent trop lourd. Rééquilibrer consiste à revendre un peu de ce qui a trop performé pour racheter ce qui est en retard. On maintient ainsi son profil de risque initial.", 
        "Revenir à une cible 50/50 si le marché a décalé à 60/40.", 6, 12, [
        ("multiple_choice", "Rééquilibrer permet de :", ["Gagner plus", "Maintenir son risque cible", "Ne rien faire", "Payer moins"], "Maintenir son risque cible", "Discipline avant tout."),
        ("true_false", "Il faut vendre ses gagnants pour rééquilibrer ?", None, "true", "Vrai, on vend haut pour acheter bas ailleurs."),
        ("multiple_choice", "Fréquence recommandée ?", ["Chaque jour", "Tous les 5 ans", "1 à 2 fois par an", "Jamais"], "1 à 2 fois par an", "Suffisant pour la plupart des gens."),
        ("true_false", "Cela force à une gestion disciplinée ?", None, "true", "Vrai.")
    ])

    # --- MODULE 12: PASSAGE ACTION (2 leçons) ---
    m12 = Module(title="Passer à l'action", description="Étapes concrètes", level="beginner", order=12, icon="🚀")
    session.add(m12); session.flush()
    
    add_lesson(session, m12.id, 1, "Ouvrir son compte", 
        "Choisissez un courtier en ligne (frais réduits) plutôt qu'une banque classique (frais élevés). Vérifiez l'agrément AMF, comparez les tarifs par ordre et l'offre d'ETF. Une fois ouvert, faites un premier virement, même petit.", 
        "Trade Republic, Boursorama ou Fortuneo sont des choix courants.", 6, 10, [
        ("multiple_choice", "Enveloppe pour fiscalité douce ?", ["Livret A", "Assurance-Vie", "Compte Courant", "Coffre-fort"], "Assurance-Vie", "Avantages successoraux et fiscaux."),
        ("true_false", "On peut investir avec 50€/mois ?", None, "true", "Vrai, grâce aux versements programmés."),
        ("multiple_choice", "Critère choix courtier ?", ["La publicité", "Les frais d'ordre et l'agrément AMF", "Le nom", "La météo"], "Les frais d'ordre et l'agrément AMF", "Protection et coût."),
        ("true_false", "Le PEA est limité à 150 000€ d'apports ?", None, "true", "Vrai.")
    ])
    
    add_lesson(session, m12.id, 2, "Premier investissement", 
        "Ne cherchez pas le 'coup du siècle'. Commencez par un ETF Monde ou S&P 500. Observez vos émotions face aux premières variations. Le but est de créer une habitude d'épargne investie chaque mois.", 
        "Achetez votre première part d'ETF World, oubliez-la 10 ans. Admirez.", 7, 15, [
        ("multiple_choice", "Action pour débutant ?", ["Trader sur marge", "Acheter un ETF diversifié et tenir", "Vendre à découvert", "Acheter au pif"], "Acheter un ETF diversifié et tenir", "Simplicité et efficacité."),
        ("true_false", "L'investissement est un marathon, pas un sprint ?", None, "true", "Vrai, le temps fait 90% du travail."),
        ("multiple_choice", "S'informer ?", ["Journal TV", "Academy et sites spécialisés", "Rumeurs bar", "Rien"], "Academy et sites spécialisés", "Sources sérieuses."),
        ("true_false", "Le meilleur moment pour investir c'était hier ?", None, "true", "Vrai, le deuxième meilleur moment est aujourd'hui.")
    ])

    session.commit()
    print(f"✅ Part 2 Completed. Modules seedés.")

def add_lesson(session, module_id, order, title, content, example, minutes, xp, questions):
    lesson = Lesson(module_id=module_id, order=order, title=title, content=content, example=example, estimated_minutes=minutes, xp_reward=xp)
    session.add(lesson); session.flush()
    for idx, q in enumerate(questions, 1):
        q_type, prompt, choices, answer, explanation = q
        session.add(Question(lesson_id=lesson.id, order=idx, type=q_type, prompt=prompt, choices=choices, correct_answer=answer, explanation=explanation))

if __name__ == "__main__":
    seed_curriculum_p2()
