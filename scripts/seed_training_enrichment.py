"""
Enriching Modules 7-12 with new lessons for a longer daily experience.
Each module will now have 3 lessons.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def enrich_curriculum():
    session = Session()
    
    # Module 7: Add Lesson 3
    m7 = session.query(Module).filter(Module.order == 7).first()
    if m7:
        add_lesson(session, m7.id, 3, "Excès de confiance et Overtrading", 
            "L'excès de confiance pousse l'investisseur à croire qu'il peut battre le marché systématiquement. Cela mène souvent à l'overtrading : multiplier les achats et ventes inutiles. Chaque transaction génère des frais et des taxes qui grignotent votre performance. La patience est la vertu numéro 1 : moins on touche à son portefeuille, plus on laisse les intérêts composés travailler sereinement.", 
            "Vendre une action parce qu'elle a baissé de 2% pour racheter une autre qui vient de monter de 5%.", 6, 12, [
            ("multiple_choice", "Qu'est-ce que l'overtrading ?", ["Vendre tout", "Multiplier les transactions inutiles", "Acheter une seule action", "Ne rien faire"], "Multiplier les transactions inutiles", "C'est l'ennemi de la performance à long terme."),
            ("true_false", "Multiplier les ordres augmente les frais et les taxes ?", None, "true", "Vrai, chaque clic coûte de l'argent."),
            ("multiple_choice", "Quelle est la principale vertu de l'investisseur ?", ["La rapidité", "Le flair", "La patience", "L'agressivité"], "La patience", "Le temps est l'ingrédient principal."),
            ("true_false", "Un investisseur qui ne touche à rien pendant 10 ans bat souvent les traders actifs ?", None, "true", "Vrai, dans la grande majorité des cas.")
        ])

    # Module 9: Add Lesson 3
    m9 = session.query(Module).filter(Module.order == 9).first()
    if m9:
        add_lesson(session, m9.id, 3, "Corrélation entre actifs", 
            "La corrélation mesure si deux actifs bougent ensemble. Si vous n'avez que des actions Tech US, votre corrélation est de 1 : tout baisse ou monte en même temps. Pour se protéger, on cherche des actifs décorrélés : quand les actions baissent, l'or ou les obligations d'État ont tendance à monter ou à rester stables. Une bonne diversification est le seul 'déjeuner gratuit' en finance.", 
            "Avoir du S&P 500 et de l'Or : ils ne bougent pas de la même façon.", 5, 12, [
            ("multiple_choice", "Si deux actifs ont une corrélation de 1, ils :", ["Bougent en sens inverse", "Bougent exactement de la même façon", "Sont indépendants", "Ne bougent pas"], "Bougent exactement de la même façon", "Aucune protection en cas de chute."),
            ("true_false", "L'or est souvent décorrélé des actions ?", None, "true", "Vrai, c'est une valeur refuge en cas de crise."),
            ("multiple_choice", "Le but de chercher la décorrélation est de :", ["Gagner 200%", "Lisser la courbe de gains et réduire le risque", "Payer moins d'impôts", "Avoir plus d'actifs"], "Lisser la courbe de gains et réduire le risque", "On évite les chutes brutales de tout le portefeuille."),
            ("true_false", "Diversifier est considéré comme le seul 'déjeuner gratuit' en finance ?", None, "true", "Vrai (citation célèbre de Markowitz).")
        ])

    # Module 10: Add Lesson 3
    m10 = session.query(Module).filter(Module.order == 10).first()
    if m10:
        add_lesson(session, m10.id, 3, "Succession et Assurance-Vie", 
            "L'Assurance-Vie n'est pas qu'un placement, c'est un outil de transmission exceptionnel. Hors succession, elle permet de transmettre jusqu'à 152 500€ par bénéficiaire sans aucun droit de mutation (pour les versements avant 70 ans). C'est le complément parfait du PEA pour le long terme et la protection de ses proches. On peut y loger des fonds en euros (garantis) ou des unités de compte (risquées).", 
            "Transmettre 150k€ à son enfant sans que l'État ne prenne de frais de succession.", 7, 15, [
            ("multiple_choice", "Abattement successoral par bénéficiaire (avant 70 ans) ?", ["15 250€", "152 500€", "No limit", "50 000€"], "152 500€", "Un avantage majeur en France."),
            ("true_false", "L'assurance-vie permet de transmettre hors succession ?", None, "true", "Vrai, c'est son utilité civique première."),
            ("multiple_choice", "Que peut-on mettre dans une assurance-vie ?", ["Uniquement du cash", "Fonds euros et Unités de Compte (indices, actions...)", "De l'immobilier physique", "Rien"], "Fonds euros et Unités de Compte (indices, actions...)", "Grande flexibilité."),
            ("true_false", "L'avantage fiscal est maximal après 8 ans ?", None, "true", "Vrai.")
        ])

    # Module 11: Add Lesson 3
    m11 = session.query(Module).filter(Module.order == 11).first()
    if m11:
        add_lesson(session, m11.id, 3, "L'importance du Cash en réserve", 
            "Ne soyez jamais investi à 100% avec vos derniers centimes. Garder une 'poche de cash' (5 à 10% du portefeuille) permet deux choses : avoir l'esprit serein en cas de besoin imprévu, et surtout pouvoir RE-INVESTIR quand les marchés sont en solde pendant un krach. Sans cash, vous êtes spectateur de la baisse. Avec du cash, vous en tirez profit.", 
            "Avoir 2000€ de côté prêts àêtre injectés si le CAC 40 perd 15%.", 6, 12, [
            ("multiple_choice", "Pourquoi garder du cash dans son portefeuille ?", ["Pour perdre de l'argent avec l'inflation", "Pour pouvoir racheter des actions en solde lors d'un krach", "Parce qu'on n'a pas trouvé d'action", "C'est obligatoire"], "Pour pouvoir racheter des actions en solde lors d'un krach", "Le cash est une 'option' sur le futur."),
            ("true_false", "Être investi à 100% est le plus sûr ?", None, "false", "Faux, on est vulnérable au moindre besoin de liquidité."),
            ("multiple_choice", "Pourcentage de cash recommandé en réserve ?", ["0%", "5 à 15%", "90%", "50%"], "5 à 15%", "Un bon équilibre entre rendement et opportunisme."),
            ("true_false", "Le cash permet de garder son calme pendant une crise ?", None, "true", "Vrai, on se sent 'acheteur' plutôt que 'victime'.")
        ])

    # Module 12: Add Lesson 3
    m12 = session.query(Module).filter(Module.order == 12).first()
    if m12:
        add_lesson(session, m12.id, 3, "Investir en période de crise", 
            "Les pires moments pour l'actualité sont souvent les meilleurs moments pour l'investisseur. Acheter quand 'le sang coule dans les rues' (selon Rothschild) nécessite du courage mais offre les meilleurs rendements historiques. Évitez de regarder les informations télévisées qui cherchent le clic par la peur. Fiez-vous aux fondamentaux et à votre plan long terme. Les crises sont des transferts de richesse des impatients vers les patients.", 
            "Acheter des actions en mars 2020 au plus fort de la panique COVID.", 7, 15, [
            ("multiple_choice", "En période de crise, l'investisseur rationnel doit :", ["Tout vendre", "Suivre son plan et si possible investir plus", "Cesser de lire", "Changer de métier"], "Suivre son plan et si possible investir plus", "C'est là que se font les gains de demain."),
            ("true_false", "Les crises sont des opportunités de transfert de richesse ?", None, "true", "Vrai."),
            ("multiple_choice", "Qui a dit 'Achetez quand le sang coule dans les rues' ?", ["Elon Musk", "Rothschild", "Warren Buffett", "Steve Jobs"], "Rothschild", "Une maxime célèbre de la finance."),
            ("true_false", "Il faut regarder les infos 24h/24 pendant un krach ?", None, "false", "Faux, cela ne fera que nourrir votre panique inutilement.")
        ])

    session.commit()
    print(f"✅ Curriculum enriched with longer modules (3 lessons each).")

def add_lesson(session, module_id, order, title, content, example, minutes, xp, questions):
    lesson = Lesson(module_id=module_id, order=order, title=title, content=content, example=example, estimated_minutes=minutes, xp_reward=xp)
    session.add(lesson); session.flush()
    for idx, q in enumerate(questions, 1):
        q_type, prompt, choices, answer, explanation = q
        session.add(Question(lesson_id=lesson.id, order=idx, type=q_type, prompt=prompt, choices=choices, correct_answer=answer, explanation=explanation))

if __name__ == "__main__":
    enrich_curriculum()
