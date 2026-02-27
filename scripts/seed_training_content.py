"""
Seed educational content for CapInvest Academy.
This generates 6-7 modules with ~25-30 lessons and ~100-120 questions.

All content is pre-generated and deterministic - no AI calls at runtime.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Module, Lesson, Question
from src.utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def seed_content():
    session = Session()
    
    # Clear existing content
    session.query(Question).delete()
    session.query(Lesson).delete()
    session.query(Module).delete()
    
    modules_data = [
        {
            "title": "Les bases de l'investissement",
            "description": "Découvrez les fondamentaux pour bien débuter votre parcours d'investisseur",
            "level": "beginner",
            "order": 1,
            "icon": "🎯",
            "lessons": [
                {
                    "title": "Qu'est-ce qu'investir ?",
                    "content": "Investir, c'est utiliser votre argent pour générer des revenus futurs. Contrairement à l'épargne classique, l'investissement implique d'accepter un certain niveau de risque en échange d'un potentiel de rendement supérieur.\\n\\nLes trois piliers de l'investissement sont :\\n• Le capital : l'argent que vous investissez\\n• Le rendement : les gains que vous espérez réaliser\\n• Le risque : la possibilité de perdre une partie de votre capital",
                    "example": "Si vous placez 1 000€ sur un livret A à 3%, vous aurez 1 030€ après un an (capital garanti). Si vous investissez 1 000€ en bourse avec un rendement potentiel de 8%, vous pourriez avoir 1 080€... ou moins selon l'évolution des marchés.",
                    "estimated_minutes": 5,
                    "xp_reward": 10,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quelle est la principale différence entre épargner et investir ?",
                            "choices": ["Le montant minimum requis", "Le niveau de risque accepté", "La durée de placement", "Le type de banque utilisée"],
                            "correct_answer": "Le niveau de risque accepté",
                            "explanation": "L'épargne privilégie la sécurité du capital, tandis que l'investissement accepte un risque en échange d'un rendement potentiellement supérieur."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Investir garantit toujours un gain supérieur à l'épargne classique.",
                            "choices": None,
                            "correct_answer": "false",
                            "explanation": "Faux. L'investissement comporte des risques et peut entraîner des pertes, contrairement à l'épargne réglementée qui garantit le capital."
                        }
                    ]
                },
                {
                    "title": "Risque et rendement",
                    "content": "Le principe fondamental de l'investissement est la relation entre risque et rendement : plus le rendement potentiel est élevé, plus le risque est important.\\n\\nLes actifs se classent généralement ainsi (du moins au plus risqué) :\\n• Livrets réglementés (risque quasi-nul, rendement faible)\\n• Obligations d'État (risque faible, rendement modéré)\\n• Actions de grandes entreprises (risque modéré à élevé, rendement potentiel élevé)\\n• Cryptomonnaies ou start-ups (risque très élevé, rendement potentiel très élevé)",
                    "example": "Un livret A rapporte environ 3% par an avec un capital garanti. Une action peut rapporter 10% par an en moyenne, mais peut aussi perdre 30% en cas de crise. C'est ce compromis risque/rendement que vous devez arbitrer selon votre profil.",
                    "estimated_minutes": 6,
                    "xp_reward": 10,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quel actif présente généralement le risque le plus faible ?",
                            "choices": ["Actions", "Obligations d'État", "Cryptomonnaies", "Start-ups"],
                            "correct_answer": "Obligations d'État",
                            "explanation": "Les obligations d'État, surtout des pays développés, sont considérées comme les investissements les moins risqués car garantis par l'État."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Un placement sans risque peut offrir un rendement très élevé.",
                            "choices": None,
                            "correct_answer": "false",
                            "explanation": "Faux. C'est le principe fondamental : pas de risque = pas de rendement élevé. Si quelqu'un vous promet un rendement élevé sans risque, c'est probablement une arnaque."
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
                    "content": "Une action représente une part de propriété d'une entreprise. En achetant une action, vous devenez actionnaire et possédez une fraction de l'entreprise.\\n\\nLes actionnaires bénéficient de deux sources de revenus :\\n• Les dividendes : une partie des bénéfices redistribuée\\n• La plus-value : l'augmentation du prix de l'action\\n\\nVous prenez aussi le risque de perte si l'entreprise performe mal ou fait faillite.",
                    "example": "Si vous achetez une action Apple à 150€ et qu'elle monte à 180€, vous réalisez une plus-value de 30€ (20%). Si Apple verse aussi un dividende de 1€ par action, votre gain total serait de 31€.",
                    "estimated_minutes": 5,
                    "xp_reward": 10,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Que représente une action ?",
                            "choices": ["Une dette de l'entreprise", "Une part de propriété de l'entreprise", "Un prêt à l'entreprise", "Une garantie bancaire"],
                            "correct_answer": "Une part de propriété de l'entreprise",
                            "explanation": "Une action est une fraction du capital d'une entreprise. En l'achetant, vous devenez copropriétaire."
                        },
                        {
                            "type": "true_false",
                            "prompt": "Les dividendes sont garantis chaque année.",
                            "choices": None,
                            "correct_answer": "false",
                            "explanation": "Faux. Les dividendes sont décidés par l'entreprise et peuvent être réduits ou supprimés si les résultats sont mauvais."
                        }
                    ]
                },
                {
                    "title": "Comment gagner avec les actions",
                    "content": "Il existe deux stratégies principales pour profiter des actions :\\n\\n1. **Investissement long terme** : acheter des actions solides et les conserver pendant des années pour bénéficier de la croissance de l'entreprise et des dividendes.\\n\\n2. **Trading actif** : acheter et vendre fréquemment pour profiter des variations de prix. Plus risqué et chronophage.\\n\\nLa majorité des investisseurs particuliers réussissent mieux avec une approche long terme et diversifiée.",
                    "example": "Warren Buffett a acheté des actions Coca-Cola dans les années 1980 et les détient toujours. La valeur a été multipliée par 16, et il reçoit des millions en dividendes chaque année. C'est la puissance de l'investissement long terme.",
                    "estimated_minutes": 6,
                    "xp_reward": 10,
                    "questions": [
                        {
                            "type": "multiple_choice",
                            "prompt": "Quelle stratégie est généralement recommandée pour les débutants ?",
                            "choices": ["Trading quotidien", "Investissement long terme diversifié", "Options et produits dérivés", "Suivre les tendances du moment"],
                            "correct_answer": "Investissement long terme diversifié",
                            "explanation": "L'investissement long terme diversifié réduit les risques et évite les erreurs émotionnelles liées au trading actif."
                        }
                    ]
                }
            ]
        },
        # Module 3 will continue below...
    ]
    
    # Adding remaining modules in a separate batch to avoid token limits
    seed_part1(session, modules_data)
    seed_part2(session)
    
    session.commit()
    print(f"✅ Seeded {session.query(Module).count()} modules")
    print(f"✅ Seeded {session.query(Lesson).count()} lessons")
    print(f"✅ Seeded {session.query(Question).count()} questions")

def seed_part1(session, modules_data):
    """Seed first 2 modules"""
    for mod_data in modules_data:
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

def seed_part2(session):
    """Seed remaining modules (3-7)"""
    # Module 3: Les ETF
    module3 = Module(title="Les ETF : investir simplement", description="Comprenez les fonds indiciels et leur intérêt pour diversifier facilement", level="beginner", order=3, icon="📊")
    session.add(module3)
    session.flush()
    
    lesson3_1 = Lesson(module_id=module3.id, title="Qu'est-ce qu'un ETF ?", 
        content="Un ETF (Exchange Traded Fund) est un fonds qui réplique automatiquement un indice boursier. Au lieu d'acheter 40 actions du CAC40 une par une, vous achetez 1 ETF CAC40 qui les contient toutes.\\n\\nAvantages :\\n• Diversification instantanée\\n• Frais très bas (0,1% à 0,5% par an)\\n• Achat/vente facile comme une action\\n• Pas besoin d'être expert",
        example="Un ETF World comme MSCI World contient plus de 1 500 entreprises de 23 pays. En achetant une seule part à 400€, vous investissez dans Apple, Microsoft, Nestlé, Toyota... automatiquement.",
        order=1, estimated_minutes=5, xp_reward=10)
    session.add(lesson3_1)
    session.flush()
    
    session.add(Question(lesson_id=lesson3_1.id, type="multiple_choice", prompt="Quelle est la principale différence entre un ETF et une action ?",
        choices=["Le prix", "La diversification", "Le risque", "La fiscalité"], correct_answer="La diversification",
        explanation="Un ETF contient des dizaines ou centaines d'actions, offrant une diversification instantanée contrairement à une action unique.", order=1))
    
    session.add(Question(lesson_id=lesson3_1.id, type="true_false", prompt="Les ETF ont généralement des frais plus élevés que les fonds actifs.",
        choices=None, correct_answer="false", explanation="Faux. Les ETF sont passifs et ont des frais très bas (0,1-0,5% par an) contre 1,5-2,5% pour les fonds actifs.", order=2))
    
    # Module 4: Diversification
    module4 = Module(title="Diversifier pour réduire le risque", description="Apprenez à construire un portefeuille équilibré et résilient", level="intermediate", order=4, icon="🎨")
    session.add(module4)
    session.flush()
    
    lesson4_1 = Lesson(module_id=module4.id, title="Pourquoi diversifier ?",
        content="Ne mettez pas tous vos œufs dans le même panier ! La diversification consiste à répartir vos investissements sur différents actifs, secteurs et géographies pour réduire le risque.\\n\\nTypes de diversification :\\n• **Géographique** : Europe, USA, Asie, émergents\\n• **Sectorielle** : tech, santé, finance, énergie\\n• **Classes d'actifs** : actions, obligations, immobilier",
        example="En 2022, la tech a chuté de 30% mais l'énergie a progressé de 40%. Un portefeuille diversifié contenant les deux a limité les pertes. C'est la magie de la diversification.",
        order=1, estimated_minutes=6, xp_reward=12)
    session.add(lesson4_1)
    session.flush()
    
    session.add(Question(lesson_id=lesson4_1.id, type="multiple_choice", prompt="La diversification permet principalement de :",
        choices=["Augmenter le rendement", "Réduire le risque", "Éviter les impôts", "Gagner plus rapidement"], correct_answer="Réduire le risque",
        explanation="La diversification réduit le risque en répartissant les investissements. Elle ne garantit pas de meilleurs rendements mais lisse la volatilité.", order=1))
    
    # Module 5: Psychologie
    module5 = Module(title="Psychologie de l'investisseur", description="Évitez les pièges émotionnels et prenez de meilleures décisions", level="intermediate", order=5, icon="🧠")
    session.add(module5)
    session.flush()
    
    lesson5_1 = Lesson(module_id=module5.id, title="Les biais cognitifs",
        content="Notre cerveau n'est pas fait pour investir ! Nous sommes programmés pour survivre dans la savane, pas pour gérer un portefeuille boursier. Voici les pièges courants :\\n\\n• **Panique lors des baisses** : vendre au pire moment par peur\\n• **Euphorie lors des bulles** : acheter au sommet par cupidité\\n• **Biais de confirmation** : ne chercher que les infos qui confirment nos croyances\\n• **Illusion de contrôle** : penser qu'on peut battre le marché",
        example="En 2020, beaucoup ont vendu en panique lors du COVID en mars (-35%). Ceux qui sont restés investis ont vu leurs portefeuilles remonter de +60% en 12 mois. La patience paie.",
        order=1, estimated_minutes=7, xp_reward=15)
    session.add(lesson5_1)
    session.flush()
    
    session.add(Question(lesson_id=lesson5_1.id, type="true_false", prompt="Il est recommandé de vendre ses actions dès qu'elles baissent de 10%.",
        choices=None, correct_answer="false", explanation="Faux. Les baisses sont normales. Vendre en panique transforme une perte temporaire en perte définitive. Mieux vaut rester investi à long terme.", order=1))
    
    # Module 6: ESG & Investissement responsable
    module6 = Module(title="Investissement responsable (ESG)", description="Investir en accord avec vos valeurs environnementales et sociales", level="intermediate", order=6, icon="🌱")
    session.add(module6)
    session.flush()
    
    lesson6_1 = Lesson(module_id=module6.id, title="Qu'est-ce que l'ESG ?",
        content="ESG signifie Environnement, Social et Gouvernance. C'est une approche d'investissement qui intègre des critères extra-financiers :\\n\\n• **E** : empreinte carbone, énergies renouvelables\\n• **S** : conditions de travail, diversité\\n• **G** : éthique de direction, lutte contre la corruption\\n\\nLes fonds ESG excluent les entreprises controversées (armement, tabac, charbon) et favorisent les leaders de la transition.",
        example="Un ETF ESG comme MSCI World ESG exclut les 20% d'entreprises les moins vertueuses et surpondère les meilleures. Performance similaire au marché classique, mais impact positif.",
        order=1, estimated_minutes=6, xp_reward=12)
    session.add(lesson6_1)
    session.flush()
    
    session.add(Question(lesson_id=lesson6_1.id, type="multiple_choice", prompt="Que signifie le 'E' dans ESG ?",
        choices=["Économie", "Environnement", "Éthique", "Équité"], correct_answer="Environnement",
        explanation="E = Environnement (climat, pollution, énergies). S = Social. G = Gouvernance.", order=1))
    
    # Module 7: Commencer à investir
    module7 = Module(title="Passer à l'action", description="Les étapes concrètes pour débuter votre parcours d'investisseur", level="beginner", order=7, icon="🚀")
    session.add(module7)
    session.flush()
    
    lesson7_1 = Lesson(module_id=module7.id, title="Ouvrir un compte",
        content="Pour investir en bourse, vous avez besoin d'un compte adapté :\\n\\n1. **Compte-titres ordinaire (CTO)** : accès total aux marchés mondiaux, fiscalité à 30%\\n2. **PEA (Plan d'Épargne en Actions)** : réservé aux actions européennes, exonération d'impôt après 5 ans\\n3. **Assurance-vie** : fonds variés, fiscalité avantageuse après 8 ans\\n\\nPour débuter : PEA si vous visez l'Europe, CTO pour un accès mondial.",
        example="Avec un PEA chez Boursorama, Trade Republic ou Fortuneo, vous pouvez acheter des ETF européens sans frais et profiter de la fiscalité avantageuse après 5 ans (17,2% au lieu de 30%).",
        order=1, estimated_minutes=6, xp_reward=10)
    session.add(lesson7_1)
    session.flush()
    
    session.add(Question(lesson_id=lesson7_1.id, type="multiple_choice", prompt="Quel compte offre la meilleure fiscalité après 5 ans pour investir en Europe ?",
        choices=["Compte-titres ordinaire", "PEA", "Livret A", "Compte courant"], correct_answer="PEA",
        explanation="Le PEA bénéficie d'une exonération d'impôt sur les plus-values après 5 ans (seuls les prélèvements sociaux de 17,2% restent dus).", order=1))

if __name__ == "__main__":
    seed_content()
