"""Utility for seeding the CapInvest Academy curriculum."""
from sqlalchemy.orm import Session
from .models import Module, Lesson, Question

def auto_seed_if_empty(db: Session):
    """Seed the curriculum only if no modules exist."""
    if db.query(Module).count() > 0:
        return False
        
    print("🌱 Database empty. Seeding initial curriculum...")
    
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
    add_lesson(m1.id, 1, "Qu'est-ce qu'investir ?", "Investir, c'est utiliser votre argent pour acquérir des actifs (actions, obligations, immobilier) dans le but de générer un gain futur, soit par la prise de valeur, soit par le versement de revenus (dividendes, loyers). Contrairement au simple livret, l'investissement comporte un risque mais offre un potentiel de croissance crucial pour battre l'inflation.", "1000€ sur un livret à 3% vs 1000€ en bourse à 8% sur 20 ans.", 5, 10, [
        ("multiple_choice", "Quelle est la principale différence entre épargner et investir ?", ["Le montant initial", "L'exposition au risque", "La banque utilisée", "La couleur de la carte"], "L'exposition au risque", "L'investissement comporte un risque de perte en capital en échange d'un rendement potentiellement plus élevé."),
        ("true_false", "L'investissement est un outil efficace pour lutter contre l'inflation ?", None, "true", "Vrai. Les actifs comme les actions ont historiquement des rendements supérieurs à l'inflation."),
        ("multiple_choice", "Quelles sont les deux composantes du rendement d'un investissement ?", ["Le montant des frais et la taxe", "La plus-value et les revenus (dividendes/intérêts)", "Le dépôt initial et le retrait", "Le capital garanti et le bonus"], "La plus-value et les revenus (dividendes/intérêts)", "Le gain total est la somme de la hausse du prix et des revenus versés."),
        ("true_false", "Il est possible de s'enrichir rapidement sans prendre aucun risque ?", None, "false", "Faux. Le rendement est la rémunération du risque pris.")
    ])
    add_lesson(m1.id, 2, "Risque / Rendement", "C'est la règle d'or : plus le potentiel de gain est élevé, plus le risque de perte est important. Un livret A est très sûr mais rapporte peu. Une action de start-up peut rapporter 1000% ou valoir zéro demain. Un bon investisseur cherche à optimiser ce couple en fonction de ses besoins.", "Comparer la sécurité d'une obligation d'État à la volatilité du Bitcoin.", 6, 10, [
        ("multiple_choice", "Lequel de ces actifs est généralement considéré comme le moins risqué ?", ["Une action technologique", "Une obligation d'État bien noté", "Une cryptomonnaie", "Un investissement immobilier spéculatif"], "Une obligation d'État bien noté", "Les États sont historiquement les emprunteurs les plus fiables."),
        ("true_false", "Prendre plus de risque garantit un rendement plus élevé ?", None, "false", "Faux. Le risque augmente le potentiel, mais n'offre aucune certitude."),
        ("multiple_choice", "Pourquoi un investisseur accepte-t-il de prendre des risques ?", ["Parce qu'il aime jouer", "Pour obtenir une espérance de rendement supérieure", "Parce que c'est obligatoire pour ouvrir un compte", "Pour assurer son capital"], "Pour obtenir une espérance de rendement supérieure", "Le rendement est une 'prime de risque'."),
        ("true_false", "La volatilité (mouvement des prix) est une forme de risque ?", None, "true", "Vrai. Elle peut forcer à vendre à un mauvais moment.")
    ])

    # --- MODULE 2: COMPRENDRE LES ACTIONS ---
    m2 = Module(title="Comprendre les actions", description="Maîtrisez les actions et leur rôle", level="beginner", order=2, icon="📈")
    db.add(m2); db.flush()
    add_lesson(m2.id, 1, "C'est quoi une action ?", "Une action est un titre de propriété représentant une fraction du capital d'une entreprise. En tant qu'actionnaire, vous devenez copropriétaire de la société. Vous avez droit à une partie des bénéfices (dividendes) et vous pouvez voter lors des assemblées générales.", "Détenir 10 actions L'Oréal fait de vous un (petit) propriétaire de la marque.", 5, 10, [
        ("multiple_choice", "Que possédez-vous réellement en achetant une action ?", ["Une créance sur l'entreprise", "Un titre de propriété", "Une garantie contre la faillite", "Un droit d'usage des produits"], "Un titre de propriété", "Une action est une part du capital."),
        ("true_false", "Toutes les entreprises versent obligatoirement des dividendes ?", None, "false", "Faux. C'est une décision de l'entreprise selon ses bénéfices et besoins."),
        ("multiple_choice", "Où s'échangent la majorité des actions ?", ["À la banque centrale", "En Bourse (marché secondaire)", "Dans la boutique de l'entreprise", "Sur les sites de dons"], "En Bourse (marché secondaire)", "La bourse permet la liquidité des titres."),
        ("true_false", "En cas de faillite, l'actionnaire est remboursé en premier ?", None, "false", "Faux. Il est remboursé en dernier, après les créanciers.")
    ])

    # --- MODULE 3: LES ETF ---
    m3 = Module(title="Les ETF : investir simplement", description="Fonds indiciels", level="beginner", order=3, icon="📊")
    db.add(m3); db.flush()
    add_lesson(m3.id, 1, "Qu'est-ce qu'un ETF ?", "Un ETF (Exchange Traded Fund) est un fonds qui suit la performance d'un indice boursier (comme le CAC 40 ou le S&P 500). En achetant une part d'ETF, vous investissez instantanément dans des centaines d'entreprises. C'est le moyen le plus simple et le moins coûteux de se diversifier.", "Un ETF MSCI World contient plus de 1500 entreprises mondiales.", 5, 12, [
        ("multiple_choice", "Pourquoi les frais des ETF sont-ils généralement très bas ?", ["Parce qu'ils sont en papier", "Parce qu'ils se contentent de copier un indice automatiquement", "Parce qu'ils ne sont réservés qu'aux riches", "Parce qu'ils ne paient pas d'impôts"], "Parce qu'ils se contentent de copier un indice automatiquement", "C'est la gestion passive, sans gérant coûteux."),
        ("true_false", "Un ETF s'achète et se vend aussi facilement qu'une action en direct ?", None, "true", "Vrai. On les appelle aussi fonds cotés en bourse."),
        ("multiple_choice", "Que signifie 'répliquer un indice' ?", ["Essayer de faire mieux que le marché", "Copier exactement la performance du marché", "Ignorer les variations de prix", "Supprimer les actions qui baissent"], "Copier exactement la performance du marché", "L'objectif est d'être le miroir de l'indice."),
        ("true_false", "Investir dans un ETF est plus risqué que d'acheter une seule action ?", None, "false", "Faux. La diversification réduit le risque spécifique.")
    ])

    db.commit()
    print("✅ Initial curriculum seeded successfully.")
    return True
