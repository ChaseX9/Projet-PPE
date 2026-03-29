# CapInvest — Robo-advisor pédagogique

CapInvest est un robo-advisor pédagogique développé dans le cadre d'un projet de fin d'études. Il s'agit d'une application web permettant à des investisseurs particuliers d'obtenir des recommandations de portefeuille personnalisées, tout en développant leurs connaissances financières à travers un parcours éducatif intégré.

---

## Objectif

Le projet vise à rendre l'investissement financier accessible à des profils non initiés, en combinant deux dimensions complémentaires : la recommandation algorithmique de portefeuilles et la formation à la finance personnelle. CapInvest s'inscrit dans une démarche de démocratisation de la gestion de patrimoine, en s'appuyant sur des méthodes quantitatives rigoureuses.

---

## Fonctionnalités principales

- **Profilage investisseur** : questionnaire adaptatif permettant de déterminer le profil de risque de l'utilisateur (prudent, équilibré, dynamique), son horizon de placement et son niveau d'expertise.
- **Recommandation de portefeuille** : génération automatique d'un portefeuille optimisé à partir d'un univers d'actifs diversifié (ETF, actions internationales), reposant sur l'optimisation de Markowitz et le modèle Black-Litterman.
- **Académie CapInvest** : parcours de formation structuré en modules progressifs couvrant les fondamentaux de l'investissement, avec quiz interactifs et suivi de progression.
- **Espace personnel** : gestion du compte, sauvegarde des portefeuilles générés, consultation de l'historique et paramètres RGPD.
- **Explorateur de marché** : visualisation des données historiques des actifs disponibles dans l'univers d'investissement.

---

## Positionnement

CapInvest s'adresse à des particuliers souhaitant s'initier à l'investissement ou structurer leur épargne, sans nécessiter de connaissances financières préalables. Il se distingue des solutions existantes par l'intégration d'un volet éducatif au cœur de l'expérience utilisateur, favorisant une appropriation progressive des concepts financiers.

L'approche est résolument pédagogique : chaque recommandation est accompagnée d'explications adaptées au niveau de l'utilisateur, et le contenu éducatif est conçu pour progresser en parallèle de sa pratique.

---

## Architecture globale

L'application repose sur une architecture client-serveur classique. Le backend est développé en Python avec le framework FastAPI, et expose une API REST consommée par un frontend en HTML/CSS/JavaScript. Les données sont persistées dans une base SQLite locale. Les données financières sont récupérées dynamiquement depuis Yahoo Finance.

Le système d'authentification gère les comptes utilisateurs avec vérification par email. L'application respecte les exigences du RGPD, notamment via la gestion du consentement et des droits d'accès aux données personnelles.

---

## Auteur

Projet réalisé par **Maël Vaudin** dans le cadre du PPE (Projet Professionnel Encadré) — 2025/2026.
