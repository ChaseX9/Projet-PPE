"""
Script de génération de l'étude de faisabilité au format Word.
Projet : Robo-Advisor (CapInvest)
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.style import WD_STYLE_TYPE
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "Etude_Faisabilite_RoboAdvisor.docx")

def set_cell_background(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    run = p.runs[0]
    if level == 1:
        run.font.color.rgb = RGBColor(0x1A, 0x2E, 0x5A)
        run.font.size = Pt(16)
    elif level == 2:
        run.font.color.rgb = RGBColor(0x1F, 0x6E, 0xB4)
        run.font.size = Pt(13)
    elif level == 3:
        run.font.color.rgb = RGBColor(0x2E, 0x86, 0xAB)
        run.font.size = Pt(12)
    return p

def add_paragraph(doc, text, bold=False, italic=False, size=11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p

def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    p.paragraph_format.left_indent = Inches(level * 0.25)
    return p

def add_telos_table(doc, rows_data):
    """rows_data: list of (dimension, question, analyse, verdict)"""
    table = doc.add_table(rows=1 + len(rows_data), cols=4)
    table.style = 'Table Grid'
    # Header
    headers = ["Dimension", "Question clé", "Analyse réelle", "Verdict"]
    header_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        header_cells[i].text = h
        set_cell_background(header_cells[i], '1A2E5A')
        run = header_cells[i].paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(10)
        header_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    colors = {
        "✅ Favorable": "D4EDDA",
        "⚠️ Partiel": "FFF3CD",
        "❌ Risque": "F8D7DA",
    }

    for i, (dim, question, analyse, verdict) in enumerate(rows_data):
        row_cells = table.rows[i + 1].cells
        row_cells[0].text = dim
        row_cells[1].text = question
        row_cells[2].text = analyse
        row_cells[3].text = verdict

        # Color verdict cell
        bg = "FFFFFF"
        for key, col in colors.items():
            if key in verdict:
                bg = col
                break
        set_cell_background(row_cells[3], bg)

        for cell in row_cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9)
        
        # Alternate row
        if i % 2 == 0:
            for j in range(3):
                set_cell_background(row_cells[j], 'F2F6FC')
    
    return table

doc = Document()

# ── Page margins ──
for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(3)
    section.right_margin = Cm(3)

# ─────────────────────────────────────────────
# PAGE DE TITRE
# ─────────────────────────────────────────────
doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("ÉTUDE DE FAISABILITÉ")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = RGBColor(0x1A, 0x2E, 0x5A)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = subtitle.add_run("Projet PPE — Robo-Advisor « CapInvest »")
r2.font.size = Pt(16)
r2.font.color.rgb = RGBColor(0x1F, 0x6E, 0xB4)

doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
meta.add_run("Date : Février 2026\n")
meta.add_run("Équipe : Maël Vaudin\n")
meta.add_run("Méthode : TELOS\n")
for r in meta.runs:
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

doc.add_page_break()

# ─────────────────────────────────────────────
# 1. INTRODUCTION
# ─────────────────────────────────────────────
add_heading(doc, "1. Introduction", level=1)

add_heading(doc, "1.1 Contexte du projet", level=2)
add_paragraph(doc,
    "Le projet PPE (Projet Personnel Encadré) consiste en la conception et le développement d'un "
    "Robo-Advisor nommé « CapInvest ». L'objectif est de démocratiser la gestion de portefeuille "
    "financier en offrant à des utilisateurs non-experts un outil automatisé, transparent et conforme "
    "aux réglementations financières européennes (MiFID II)."
)
add_paragraph(doc,
    "L'application est une plateforme web full-stack développée intégralement en Python, proposant "
    "un questionnaire de profilage, une optimisation mathématique de portefeuille (Markowitz et Black-Litterman), "
    "une section éducative (CapInvest Academy) et une gestion des données utilisateurs conforme au RGPD."
)

add_heading(doc, "1.2 Objectifs de l'étude", level=2)
for obj in [
    "Vérifier que le projet est réalisable et viable dans le contexte d'un PPE étudiant.",
    "Identifier les freins et risques potentiels rencontrés ou anticipés.",
    "Justifier les choix technologiques avec des éléments factuels issus du code produit.",
    "Formuler des recommandations claires pour la suite du projet.",
]:
    add_bullet(doc, obj)

add_heading(doc, "1.3 Périmètre de l'étude", level=2)
add_paragraph(doc, "L'étude porte sur l'ensemble des composants réalisés :")
for scope in [
    "Backend API REST (Python / FastAPI)",
    "Base de données locale (SQLite / SQLAlchemy)",
    "Moteur d'optimisation financière (Markowitz, Black-Litterman)",
    "Système d'authentification et de sécurité (JWT, bcrypt)",
    "Interface utilisateur (HTML / CSS / Vanilla JS)",
    "Module éducatif : CapInvest Academy (leçons, quiz, XP)",
    "Conformité réglementaire (RGPD, MiFID II)",
]:
    add_bullet(doc, scope)

add_paragraph(doc, "\nSont exclus du périmètre : le déploiement en production sur serveur distant, "
    "les tests de charge à grande échelle et l'intégration d'un vrai courtier financier.", italic=True)

doc.add_paragraph()

# ─────────────────────────────────────────────
# 2. MÉTHODOLOGIE
# ─────────────────────────────────────────────
add_heading(doc, "2. Méthodologie", level=1)

add_paragraph(doc,
    "L'analyse de faisabilité s'appuie sur la méthode TELOS (Technique, Économique, Légal, "
    "Organisationnel, Scheduling). Les données utilisées proviennent exclusivement du travail réellement "
    "accompli dans le code source du projet :"
)
for source in [
    "Lecture du code source (dossiers src/, scripts/, templates/)",
    "Documentation du projet (README.md, PROJECT_HANDOVER.md)",
    "Requirements techniques listés dans requirements.txt",
    "Documentation officielle des bibliothèques utilisées (FastAPI, SQLAlchemy, yfinance, PyPortfolioOpt)",
    "Référentiel réglementaire MiFID II (Directive européenne sur les marchés financiers)",
    "Règlement général sur la protection des données (RGPD – Règlement UE 2016/679)",
]:
    add_bullet(doc, source)

doc.add_paragraph()

# ─────────────────────────────────────────────
# 3. ANALYSE TELOS
# ─────────────────────────────────────────────
add_heading(doc, "3. Analyse TELOS", level=1)

# ── 3.1 Technique ──
add_heading(doc, "3.1 Technique (T)", level=2)
add_paragraph(doc,
    "La dimension technique évalue si les technologies, compétences et ressources matérielles "
    "disponibles sont suffisantes pour réaliser le projet."
)

add_heading(doc, "Technologies effectivement utilisées", level=3)
tech_table_data = [
    ("FastAPI", "Framework Python pour l'API REST", "Utilisé comme cœur du backend ; gère 15+ endpoints (auth, portefeuille, RGPD, academy)", "✅ Maîtrisé"),
    ("SQLite + SQLAlchemy", "SGBD local + ORM Python", "5 modèles ORM : User, SavedProfile, SavedPortfolio, Lesson, UserLessonProgress ; migrations gérées par scripts", "✅ Fonctionnel"),
    ("yfinance", "API gratuite Yahoo Finance", "Récupération des prix historiques de 154 actifs (ETFs + Actions) ; cache 7 jours dans universe.csv", "✅ Intégré"),
    ("PyPortfolioOpt + NumPy", "Optimisation Markowitz", "Modèle Mean-Variance Optimization implémenté dans optimizer.py avec contraintes (2–10 actifs, concentration 30–50%)", "✅ Opérationnel"),
    ("Black-Litterman", "Optimisation avancée", "Implémenté et réservé aux profils « Expert » avec gating strict (verrouillage automatique si profil novice)", "✅ Implémenté"),
    ("JWT + bcrypt", "Authentification sécurisée", "Tokens JWT via python-jose, mots de passe hachés via passlib[bcrypt], sessions sécurisées", "✅ Sécurisé"),
    ("HTML/CSS/Vanilla JS", "Frontend", "13 templates HTML (login, questionnaire, suivi, academy, RGPD…), fichiers JS séparés (smart-suggestions.js)", "✅ Fonctionnel"),
    ("scikit-learn", "Machine Learning", "Présent dans requirements.txt pour des traitements de données potentiels", "⚠️ Partiel"),
]

table = doc.add_table(rows=1 + len(tech_table_data), cols=4)
table.style = 'Table Grid'
for i, h in enumerate(["Technologie", "Rôle", "Usage réel dans le projet", "Statut"]):
    c = table.rows[0].cells[i]
    c.text = h
    set_cell_background(c, '1F6EB4')
    run = c.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(9)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for i, (tech, role, usage, status) in enumerate(tech_table_data):
    row = table.rows[i + 1].cells
    row[0].text = tech
    row[1].text = role
    row[2].text = usage
    row[3].text = status
    if i % 2 == 0:
        for j in range(3):
            set_cell_background(row[j], 'EFF4FB')
    if "✅" in status:
        set_cell_background(row[3], 'D4EDDA')
    elif "⚠️" in status:
        set_cell_background(row[3], 'FFF3CD')
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9)

doc.add_paragraph()
add_paragraph(doc,
    "Le projet a été entièrement développé sur machine locale (Mac) sans infrastructure cloud. "
    "Toutes les bibliothèques sont open-source, gratuites, et disponibles via pip. La complexité "
    "technique réside principalement dans l'implémentation correcte des modèles financiers (Markowitz, "
    "Black-Litterman) et dans la logique métier du questionnaire de profilage (Safety-First, gating).",
    italic=True
)

add_paragraph(doc, "\nConclusion Technique : ", bold=True)
add_paragraph(doc,
    "Le projet est techniquement faisable. L'ensemble de la stack est disponible, documentation "
    "accessible, et les compétences nécessaires ont été acquises en cours de développement. "
    "Le seul risque résiduel concerne la fiabilité de l'API Yahoo Finance (externe, non garantie)."
)

doc.add_paragraph()

# ── 3.2 Économique ──
add_heading(doc, "3.2 Économique (E)", level=2)
add_paragraph(doc,
    "La dimension économique évalue la soutenabilité financière du projet, notamment les coûts "
    "de développement, d'exploitation et de maintenance."
)

econ_data = [
    ("Serveur / Hébergement", "0 €", "Application run en local (localhost:8000). Aucun serveur externe utilisé."),
    ("Base de données", "0 €", "SQLite : inclus dans Python, aucune licence requise."),
    ("Données financières", "0 €", "Yahoo Finance via yfinance (API gratuite). 154 actifs chargés sans abonnement."),
    ("Bibliothèques Python", "0 €", "Open-source : FastAPI, SQLAlchemy, PyPortfolioOpt, scikit-learn, etc."),
    ("Outils de développement", "0 €", "VS Code (gratuit), terminal macOS, Git (gratuit)."),
    ("Matériel informatique", "Existant", "MacBook personnel — aucun achat matériel requis."),
    ("TOTAL", "0 €", "Projet 100% gratuit dans sa phase de développement et de démo."),
]

table2 = doc.add_table(rows=1 + len(econ_data), cols=3)
table2.style = 'Table Grid'
for i, h in enumerate(["Poste de coût", "Montant", "Justification"]):
    c = table2.rows[0].cells[i]
    c.text = h
    set_cell_background(c, '1F6EB4')
    run = c.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(9)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for i, (poste, montant, justif) in enumerate(econ_data):
    row = table2.rows[i + 1].cells
    row[0].text = poste
    row[1].text = montant
    row[2].text = justif
    if i % 2 == 0:
        set_cell_background(row[0], 'EFF4FB')
        set_cell_background(row[2], 'EFF4FB')
    if i == len(econ_data) - 1:
        for j in range(3):
            set_cell_background(row[j], 'D4EDDA')
            row[j].paragraphs[0].runs[0].bold = True
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9)

doc.add_paragraph()
add_paragraph(doc,
    "En cas de déploiement réel (post-PPE), des coûts apparaîtraient : hébergement cloud (5–20€/mois), "
    "abonnement à une API financière professionnelle (Bloomberg, Refinitiv), et éventuellement un agrément "
    "AMF. Ces coûts dépassent le cadre du PPE actuel.",
    italic=True
)
add_paragraph(doc, "\nConclusion Économique : ", bold=True)
add_paragraph(doc,
    "Le projet est économiquement viable dans son périmètre académique. Le coût de développement "
    "est nul grâce à l'utilisation exclusive de technologies gratuites et open-source."
)

doc.add_paragraph()

# ── 3.3 Légal ──
add_heading(doc, "3.3 Légal (L)", level=2)
add_paragraph(doc,
    "La dimension légale examine les contraintes réglementaires applicables au projet."
)

add_heading(doc, "Réglementation MiFID II", level=3)
add_paragraph(doc,
    "MiFID II (Markets in Financial Instruments Directive II) est la directive européenne encadrant "
    "les services d'investissement. Elle impose notamment l'évaluation du profil de risque des clients "
    "avant toute recommandation."
)
add_paragraph(doc, "Éléments MiFID II effectivement implémentés dans le code :", bold=True)
for item in [
    "Questionnaire de profilage obligatoire : collecte des objectifs, horizon, tolérance au risque, capacité de perte et niveau de connaissance (src/profile/suggestion_rules.py).",
    "Logique Safety-First : la capacité de perte prime toujours sur l'objectif de performance (règle Tier 1 vs Tier 2). Un utilisateur déclarant \"aucune capacité de perte\" se voit systématiquement orienter vers un profil Prudent.",
    "Verrouillage des fonctionnalités expert : Black-Litterman (modèle de views de marché) réservé aux profils « Expert ». Passage en mode novice = désactivation automatique.",
    "Transparence : chaque actif du portefeuille est accompagné d'une explication textuelle en français de son rôle (Core, Diversification, Fiabilité) générée par explainer.py.",
    "Absence de boîte noire (no black-box) : toutes les décisions d'allocation sont traçables et expliquées.",
]:
    add_bullet(doc, item)

add_heading(doc, "Réglementation RGPD", level=3)
add_paragraph(doc,
    "Le Règlement Général sur la Protection des Données (RGPD – UE 2016/679) impose des obligations "
    "strictes sur la collecte, le traitement et la suppression des données personnelles."
)
add_paragraph(doc, "Éléments RGPD effectivement implémentés :", bold=True)
for item in [
    "Modèle User avec champs de consentement explicites (privacy_policy_accepted_at, cookies_consent, marketing_consent) dans src/database/models.py.",
    "Endpoints RGPD dédiés dans src/api/gdpr_endpoints.py : export des données personnelles, suppression du compte.",
    "Page de gestion des données utilisateur (templates/gestion_donnees.html) et politique de confidentialité (templates/politique_confidentialite.html).",
    "Mentions légales disponibles (templates/mentions_legales.html).",
    "Mots de passe hachés avec bcrypt — aucun mot de passe en clair stocké.",
    "Tokens JWT avec expiration pour l'authentification (python-jose).",
]:
    add_bullet(doc, item)

add_paragraph(doc, "\nConclusion Légale : ", bold=True)
add_paragraph(doc,
    "Le projet démontre une prise en compte sérieuse des contraintes réglementaires. "
    "Les exigences MiFID II et RGPD ont été intégrées dès la conception (privacy by design). "
    "Le projet reste dans un cadre pédagogique et n'est pas soumis à un agrément AMF réel, "
    "mais l'architecture respecte les principes fondamentaux qui seraient requis en production."
)

doc.add_paragraph()

# ── 3.4 Organisationnel ──
add_heading(doc, "3.4 Organisationnel (O)", level=2)
add_paragraph(doc,
    "La dimension organisationnelle évalue les ressources humaines, la logistique et la gestion "
    "du projet au sein de l'équipe."
)

add_heading(doc, "Structure de l'équipe et répartition du travail", level=3)
add_paragraph(doc,
    "Le projet a été développé par un seul développeur (Maël Vaudin) avec l'assistance d'un "
    "assistant IA pour la génération et le débogage du code. Cette organisation présente des défis "
    "organisationnels spécifiques :"
)
for item in [
    "Gestion en solo : toutes les décisions techniques, de conception et de priorité ont été prises par une seule personne.",
    "Développement itératif par phases : le projet a été découpé en 11 phases successives (Phase 1 : modèle mathématique → Phase 11 : conformité et gating), permettant des livraisons progressives et testables.",
    "Documentation interne : un fichier PROJECT_HANDOVER.md a été maintenu pour suivre l'état du projet et faciliter la continuité entre sessions.",
    "Scripts de maintenance : des scripts utilitaires dans le dossier scripts/ (seeding de la base, migration, debug) structurent les opérations récurrentes.",
    "Tests automatisés : un dossier tests/ est présent avec des tests via pytest et httpx.",
]:
    add_bullet(doc, item)

add_heading(doc, "Architecture technique bien structurée", level=3)
for item in [
    "src/api/ : endpoints API (auth, portfolio, academy, RGPD)",
    "src/portfolio/ : logique d'optimisation financière (optimizer, recommender, explainer, filters)",
    "src/database/ : modèles et base de données",
    "src/profile/ : règles de profilage",
    "templates/ : 13 pages HTML",
    "static/ : CSS et JS",
    "scripts/ : 24 scripts utilitaires",
]:
    add_bullet(doc, item)

add_paragraph(doc, "\nConclusion Organisationnelle : ", bold=True)
add_paragraph(doc,
    "La structure du projet est solide et bien organisée malgré un développement en solo. "
    "La décomposition en phases claires, la documentation soignée et la séparation des responsabilités "
    "(API, base de données, moteur financier, frontend) témoignent d'une rigueur organisationnelle "
    "adaptée au contexte d'un projet étudiant individuel."
)

doc.add_paragraph()

# ── 3.5 Scheduling ──
add_heading(doc, "3.5 Scheduling — Calendrier (S)", level=2)
add_paragraph(doc,
    "La dimension Scheduling évalue si le projet a pu être réalisé dans le temps disponible "
    "et si les phases ont été correctement priorisées."
)

sched_data = [
    ("Phase 1–2", "Déc. 2025", "Moteur mathématique (Markowitz) + plateforme web de base (FastAPI, SQLite, authentification JWT)", "✅ Livré"),
    ("Phase 3–4", "Janv. 2026", "Black-Litterman + raffinement UX (explications, profil utilisateur)", "✅ Livré"),
    ("Phase 5–6", "Janv.–Fév. 2026", "Contraintes réalistes (2–10 actifs), cycle de vie du portefeuille (accepter/refuser)", "✅ Livré"),
    ("Phase 7–9", "Fév. 2026", "Transparence (rôle des actifs), moteur de suggestions temps réel, logique Safety-First, conformité MiFID II", "✅ Livré"),
    ("Phase 10–11", "Fév. 2026", "Expansion univers (154 actifs), classification dynamique, verrouillage Black-Litterman, RGPD complet", "✅ Livré"),
    ("Academy", "Fév. 2026", "Modules pédagogiques, leçons, quiz, système XP et progression, gamification", "✅ Livré"),
]

table3 = doc.add_table(rows=1 + len(sched_data), cols=4)
table3.style = 'Table Grid'
for i, h in enumerate(["Phase", "Période", "Contenu livré", "Statut"]):
    c = table3.rows[0].cells[i]
    c.text = h
    set_cell_background(c, '1F6EB4')
    run = c.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(9)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for i, (phase, period, content, status) in enumerate(sched_data):
    row = table3.rows[i + 1].cells
    row[0].text = phase
    row[1].text = period
    row[2].text = content
    row[3].text = status
    if i % 2 == 0:
        for j in range(3):
            set_cell_background(row[j], 'EFF4FB')
    set_cell_background(row[3], 'D4EDDA')
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9)

doc.add_paragraph()
add_paragraph(doc, "\nConclusion Scheduling : ", bold=True)
add_paragraph(doc,
    "Le calendrier a été respecté. Les 11 phases de développement ont été réalisées en environ "
    "2 mois (décembre 2025 – février 2026), avec une progression cohérente du MVP vers un produit "
    "plus complet. La principale contrainte de temps pédagogique (délai de livraison du PPE) "
    "a été anticipée par le découpage en phases livrables indépendamment."
)

doc.add_paragraph()

# ─────────────────────────────────────────────
# 4. CONCLUSIONS ET RECOMMANDATIONS
# ─────────────────────────────────────────────
add_heading(doc, "4. Conclusions et recommandations", level=1)

add_heading(doc, "4.1 Synthèse TELOS", level=2)

synth_data = [
    ("T – Technique", "Stack open-source maîtrisée. Markowitz + Black-Litterman implémentés. yfinance externe (risque limité).", "✅ Favorable"),
    ("E – Économique", "Coût zéro en phase académique. Technologies entièrement gratuites et open-source.", "✅ Favorable"),
    ("L – Légal", "MiFID II et RGPD intégrés by design. Consentements, export, suppression données, Safety-First.", "✅ Favorable"),
    ("O – Organisationnel", "Projet en solo bien structuré (11 phases, docs, séparation des couches).", "⚠️ Partiel"),
    ("S – Scheduling", "11 phases livrées en 2 mois. Calendrier respecté, progression maîtrisée.", "✅ Favorable"),
]

table4 = doc.add_table(rows=1 + len(synth_data), cols=3)
table4.style = 'Table Grid'
for i, h in enumerate(["Dimension", "Résumé", "Verdict global"]):
    c = table4.rows[0].cells[i]
    c.text = h
    set_cell_background(c, '1A2E5A')
    run = c.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(10)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

for i, (dim, resume, verdict) in enumerate(synth_data):
    row = table4.rows[i + 1].cells
    row[0].text = dim
    row[1].text = resume
    row[2].text = verdict
    if i % 2 == 0:
        for j in range(2):
            set_cell_background(row[j], 'EFF4FB')
    if "✅" in verdict:
        set_cell_background(row[2], 'D4EDDA')
    elif "⚠️" in verdict:
        set_cell_background(row[2], 'FFF3CD')
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(10)

doc.add_paragraph()

add_heading(doc, "4.2 Faisabilité globale", level=2)
add_paragraph(doc,
    "Le projet CapInvest Robo-Advisor est globalement faisable et a été réalisé avec succès dans "
    "le cadre du PPE. 4 dimensions sur 5 sont entièrement favorables. La dimension organisationnelle "
    "est jugée partiellement favorable en raison du développement en solo, ce qui représente une "
    "charge importante mais qui a été gérée efficacement grâce à un découpage rigoureux en phases."
)

add_heading(doc, "4.3 Risques identifiés et mitigation", level=2)
risk_data = [
    ("Dépendance à Yahoo Finance", "Moyen", "L'API yfinance est gratuite mais non garantie (rate limits, données manquantes)", "Cache local 7 jours (universe.csv) + script de refresh manuel"),
    ("Développement en solo", "Moyen", "Pas de revue de code par des pairs, risque d'angles morts", "Documentation rigoureuse (PROJECT_HANDOVER.md), découpage en phases testables"),
    ("Non-déploiement en production", "Faible", "Application tourne uniquement en local (127.0.0.1:8000)", "Scripts de lancement simplifiés (lancer_app_mac.sh, .bat)"),
    ("Agrément AMF non détenu", "Faible (PPE)", "En conditions réelles, un agrément serait requis pour conseil en investissement", "Périmètre académique clairement défini. Conformité MiFID II démontrable"),
    ("scikit-learn sous-utilisé", "Faible", "Présent dans requirements mais usage limité dans le code actuel", "Aucun impact fonctionnel. Peut être retiré ou étendu en Phase 12"),
],

for row in risk_data[0]:
    pass

table5 = doc.add_table(rows=1 + len(risk_data[0]), cols=4)
table5.style = 'Table Grid'
for i, h in enumerate(["Risque", "Probabilité", "Impact potentiel", "Mitigation"]):
    c = table5.rows[0].cells[i]
    c.text = h
    set_cell_background(c, '1A2E5A')
    run = c.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(9)
    c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

prob_colors = {"Moyen": "FFF3CD", "Faible": "D4EDDA", "Faible (PPE)": "D4EDDA"}
for i, (risque, prob, impact, miti) in enumerate(risk_data[0]):
    row = table5.rows[i + 1].cells
    row[0].text = risque
    row[1].text = prob
    row[2].text = impact
    row[3].text = miti
    set_cell_background(row[1], prob_colors.get(prob, 'FFFFFF'))
    if i % 2 == 0:
        set_cell_background(row[0], 'EFF4FB')
        set_cell_background(row[2], 'EFF4FB')
        set_cell_background(row[3], 'EFF4FB')
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9)

doc.add_paragraph()

add_heading(doc, "4.4 Recommandations pour la suite", level=2)
for rec in [
    "Déployer l'application sur un hébergement cloud gratuit (ex. Railway, Render) pour la rendre accessible à des testeurs extérieurs.",
    "Remplacer yfinance par une API financière plus robuste (ex. Alpha Vantage en tier gratuit) pour garantir la fiabilité des données.",
    "Compléter la couverture de tests (pytest) pour les cas limites du questionnaire et de l'optimiseur.",
    "Envisager la migration vers PostgreSQL si plusieurs utilisateurs simultanés doivent être supportés (SQLite non recommandé en multi-utilisateurs).",
    "Approfondir l'utilisation de scikit-learn pour des fonctionnalités de recommandation ou de classification des profils.",
]:
    add_bullet(doc, rec)

doc.add_paragraph()

# ─────────────────────────────────────────────
# 5. ANNEXES
# ─────────────────────────────────────────────
add_heading(doc, "5. Annexes", level=1)

add_heading(doc, "Annexe A — Structure du projet (arborescence simplifiée)", level=2)
tree_para = doc.add_paragraph()
tree_para.style = doc.styles['No Spacing']
run = tree_para.add_run(
"""Projet PPE/
├── src/
│   ├── api/
│   │   ├── main.py                    ← Point d'entrée FastAPI
│   │   ├── endpoints.py               ← Routes principales (portfolio, profil)
│   │   ├── auth_endpoints.py          ← Inscription, connexion, JWT
│   │   ├── portfolio_endpoints.py     ← Gestion cycle de vie portefeuille
│   │   ├── training_endpoints.py      ← Academy (modules, leçons, quiz)
│   │   └── gdpr_endpoints.py          ← Export et suppression données RGPD
│   ├── portfolio/
│   │   ├── optimizer.py               ← Markowitz + Black-Litterman
│   │   ├── recommender.py             ← Sélection et filtrage des actifs
│   │   └── explainer.py               ← Génération des explications textuelles
│   ├── database/
│   │   └── models.py                  ← 7 modèles SQLAlchemy
│   └── profile/
│       └── suggestion_rules.py        ← Logique Safety-First MiFID II
├── templates/                         ← 13 fichiers HTML
├── static/                            ← CSS + JS (smart-suggestions.js)
├── scripts/                           ← 24 scripts utilitaires
├── data/
│   └── universe.csv                   ← 154 actifs (cache Yahoo Finance)
└── requirements.txt                   ← 19 dépendances Python"""
)
run.font.name = 'Courier New'
run.font.size = Pt(8.5)
run.font.color.rgb = RGBColor(0x1A, 0x2E, 0x5A)

doc.add_paragraph()

add_heading(doc, "Annexe B — Dépendances Python utilisées", level=2)
deps = [
    ("fastapi>=0.104.0", "Framework API REST"),
    ("uvicorn[standard]>=0.24.0", "Serveur ASGI"),
    ("pydantic[email]>=2.0.0", "Validation des données"),
    ("yfinance>=0.2.32", "Récupération données financières (Yahoo Finance)"),
    ("pandas>=2.0.0", "Manipulation de données"),
    ("numpy>=1.24.0", "Calculs matriciels"),
    ("PyPortfolioOpt>=1.5.5", "Optimisation Markowitz"),
    ("scikit-learn>=1.3.0", "Machine Learning"),
    ("pytest>=7.4.0", "Tests automatisés"),
    ("httpx>=0.25.0", "Client HTTP pour tests"),
    ("sqlalchemy>=2.0.0", "ORM base de données"),
    ("passlib[bcrypt]>=1.7.4", "Hachage des mots de passe"),
    ("python-jose[cryptography]>=3.3.0", "Tokens JWT"),
    ("python-multipart>=0.0.6", "Formulaires HTTP"),
    ("aiofiles>=23.2.1", "Fichiers asynchrones"),
    ("email-validator>=2.1.0", "Validation emails"),
    ("bcrypt>=4.2.0", "Chiffrement"),
]

table6 = doc.add_table(rows=1 + len(deps), cols=2)
table6.style = 'Table Grid'
for i, h in enumerate(["Package (requirements.txt)", "Usage"]):
    c = table6.rows[0].cells[i]
    c.text = h
    set_cell_background(c, '1F6EB4')
    run = c.paragraphs[0].runs[0]
    run.bold = True
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(9)

for i, (pkg, usage) in enumerate(deps):
    row = table6.rows[i + 1].cells
    row[0].text = pkg
    row[1].text = usage
    if i % 2 == 0:
        set_cell_background(row[0], 'EFF4FB')
        set_cell_background(row[1], 'EFF4FB')
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9)
                run.font.name = 'Courier New' if cell == row[0] else run.font.name

doc.add_paragraph()
doc.add_page_break()

# Final note
final = doc.add_paragraph()
final.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = final.add_run("— Fin de l'étude de faisabilité —")
r.italic = True
r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
r.font.size = Pt(10)

doc.save(OUTPUT_PATH)
print(f"✅ Document Word généré : {OUTPUT_PATH}")
